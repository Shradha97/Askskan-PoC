import os
import argparse
import warnings
import pandas as pd
import numpy as np
from app.configurations.development.config_parser import args
import time
import sentence_transformers.util as utl
from app.engine.document_retrieval_engine import DocumentRetrievalEngine
from app.engine.prompts_engine import PromptsEngine
from app.engine.query_generation_engine import QueryGenerationEngine
from app.engine.memory_engine import MemoryEngine
from app.engine.postprocessing_engine import PostProcessingEngine
from app.engine.sessions_manager_engine import SessionsManagerEngine
from app.manager.askskan_qa_embed_manager import AskSkanQAEmbedManager
from app.configurations.development.settings import SCHEMA_FILE

warnings.filterwarnings("ignore")

from sentence_transformers import SentenceTransformer


def get_askskan_qa_embed_manager(persona_id, start_date, end_date):
    document_retrieval_engine = DocumentRetrievalEngine()
    prompts_engine = PromptsEngine(
        document_retrieval_engine, start_date, end_date, persona_id
    )

    askskan_qa_manager = AskSkanQAEmbedManager(
        memory_engine=MemoryEngine(),
        query_generation_engine=QueryGenerationEngine(),
        post_processing_engine=PostProcessingEngine(),
        document_retrieval_engine=document_retrieval_engine,
        prompts_engine=prompts_engine,
    )
    return askskan_qa_manager


def get_args():
    log_file = args.log_file
    user_id = args.user_id
    session_id = args.session_id
    question = args.question
    bot = args.bot_format
    clean = args.clean
    model_verbose = args.model_verbose
    return log_file, user_id, session_id, question, bot, clean, model_verbose


def get_input_filters():
    persona_id = args.persona_id
    start_date = args.start_date
    end_date = args.end_date
    return persona_id, start_date, end_date


def cli_ui(
    user_input,
    askskan_qa_embed_manager,
    askskan_qa_chain,
):
    (
        generated_query,
        doc_cols,
        embed_rank_sim,
    ) = askskan_qa_embed_manager.get_qa_embed_docs(
        user_input,
        askskan_qa_chain,
    )

    return generated_query, doc_cols, embed_rank_sim


def create_df_col_names(question_num):
    """
    create a list of column names for the dataframe such that col_name = "rank_sim_" + str(question_num)
    where question_num is a list of question numbers
    """
    return [f"rank_sim_{num}" for num in question_num]


def assign_values(schema_col, rank_sim_list, schema_columns_list):
    """
    Create a function to map values to the correct index of the DataFrame
    """
    return rank_sim_list[schema_columns_list.index(schema_col)]


def create_embed_ranks_df(
    schema_columns_list, rank_sim_list, evaluated_indexes, current_embedded_ranks_csv
):
    """
    Create a dataframe from the columns, ranks and similarities such that
    each column has a corresponding rank and similarity score and the column acts as the index.
    """
    df = pd.DataFrame(current_embedded_ranks_csv)
    for index1 in range(0, len(evaluated_indexes)):
        temp_tuple_list = []
        for index2 in range(len(schema_columns_list[index1])):
            temp_tuple_list.append(
                (schema_columns_list[index1][index2], rank_sim_list[index1][index2])
            )
        temp_tuple_list.sort()
        df[f"rank_sim_{evaluated_indexes[index1]}"] = [
            value for col, value in temp_tuple_list
        ]

    return df


def get_rank_sim(
    questions_df,
    askskan_qa_embed_manager,
    askskan_qa_chain,
    current_embedded_ranks_csv,
    schema_csv_columns,
):
    # Initialize an empty list to store unmatched columns for each row
    doc_cols_list = []
    embed_rank_sim_list = []

    questions_df_len = len(questions_df)
    not_evaluated_indexes = []
    evaluated_indexes = []

    for i in range(questions_df_len):
        question = questions_df["Question"].iloc[i]
        question += " in april 2023"
        if (
            f"rank_sim_{questions_df['#'].iloc[i]}"
            in current_embedded_ranks_csv.columns
        ):
            continue

        # by open ai embedding model
        generated_query, doc_cols, embed_rank_sim = cli_ui(
            question,
            askskan_qa_embed_manager,
            askskan_qa_chain,
        )

        print(f"Question {questions_df['#'].iloc[i]}")
        time.sleep(2)

        if doc_cols == "N/A":
            not_evaluated_indexes.append(questions_df["#"].iloc[i])
            continue
        evaluated_indexes.append(questions_df["#"].iloc[i])

        doc_cols_list.append(doc_cols)
        embed_rank_sim_list.append(embed_rank_sim)

    print("Creating embedding ranks dataframe...")
    embed_ranks_df = create_embed_ranks_df(
        doc_cols_list,
        embed_rank_sim_list,
        evaluated_indexes,
        current_embedded_ranks_csv,
    )

    return embed_ranks_df, evaluated_indexes


def get_new_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        nargs="?",
        help="path of input question csv",
        type=str,
        default="data/embedding_ranks/question.csv",
    )
    parser.add_argument(
        "-o",
        nargs="?",
        help="path of output embedding ranks similarities csv",
        type=str,
        default="data/embedding_ranks/embedding_ranks.csv",
    )

    parsed_args = parser.parse_args()
    return parsed_args.i, parsed_args.o


if __name__ == "__main__":
    # getting the arguments
    (
        log_file,
        user_id,
        session_id,
        question,
        bot_format,
        clean,
        model_verbose,
    ) = get_args()

    (
        persona_id,
        start_date,
        end_date,
    ) = get_input_filters()
    # initializing the required objects
    askskan_qa_embed_manager = get_askskan_qa_embed_manager(
        persona_id,
        start_date,
        end_date,
    )

    # cleaning the vectorestore and the sessions
    if clean:
        askskan_qa_embed_manager.document_retrieval_engine.delete_vectorstore_file

    askskan_qa_chain, buffer_memory = askskan_qa_embed_manager.get_qa_chain(
        model_verbose
    )

    [
        file_path_of_input_questions_csv,
        file_path_of_export_embedding_ranks_csv,
    ] = get_new_args()
    schema_csv = pd.read_csv(SCHEMA_FILE)
    current_embedded_ranks_csv = pd.read_csv(file_path_of_export_embedding_ranks_csv)
    questions_csv = pd.read_csv(file_path_of_input_questions_csv)
    embed_ranks_df, evaluated_index = get_rank_sim(
        questions_csv,
        askskan_qa_embed_manager,
        askskan_qa_chain,
        current_embedded_ranks_csv,
        schema_csv.columns,
    )

    # create_embed_ranks_csv(doc_cols, embed_rank_sim, question_num)
    embed_ranks_df.to_csv(file_path_of_export_embedding_ranks_csv, index=False)
