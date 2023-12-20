import re
import ast
import argparse
import pandas as pd
from app.configurations.development.settings import TOP_K_DEFAULT_EMBEDS, SCHEMA_FILE


def search_missing_columns(missing_cols_list, embeds_rank_df, question_num):
    """
    Search the rank and similarity scores of the missing columns which are present as the index
    in the dataframe and return the corresponding ranks and similarities.
    """
    ranks = []
    similarities = []
    rank_sim_col = "rank_sim_" + str(question_num)
    embed_rank_csv[rank_sim_col] = embed_rank_csv[rank_sim_col].map(ast.literal_eval)

    for col in missing_cols_list:
        if col in embeds_rank_df.index.values.tolist():
            ranks.append(embeds_rank_df.loc[col][rank_sim_col][0])
            similarities.append(embeds_rank_df.loc[col][rank_sim_col][1])
        else:
            ranks.append("N/A")
            similarities.append("N/A")

    return ranks, similarities


def get_missing_columns(sql_query, column_list, valid_column_names):
    # Extract column names from the SELECT statement using regex

    pattern = r"SELECT\s+(.+?)\s+FROM"
    match = re.search(pattern, sql_query, re.IGNORECASE)
    selected_columns = match.group(1).split(",")

    # Process each selected column
    valid_columns = []
    for col in selected_columns:
        # Handle functions and aliases using regex
        col = re.sub(r"\s+AS\s+\w+", "", col, flags=re.IGNORECASE).strip()
        col = re.sub(r"[^()\s]*\(", "", col).strip()  # Remove functions if present
        col = col.strip("()")  # Remove parentheses if present
        col = re.sub(
            r"^\s*DISTINCT\s+", "", col, flags=re.IGNORECASE
        )  # Remove DISTINCT if present

        if col.strip() not in ["*", "'EEEE'", "12", "2", "'%W'"]:
            valid_columns.append(col.strip())

    missing_columns = [col for col in valid_columns if col not in column_list]
    return valid_columns, missing_columns, 1 if missing_columns else 0


def select_top_k_embeds(embeds_df, df_col_name, top_k=TOP_K_DEFAULT_EMBEDS):
    """
    Embeds_df is a dataframe with columns represented by rank_sim_i where i is the question number.
    rank_sim_i is a list of tuples of the form (rank, similarity score) for each column.
    Select the top 10 index values in the data frame based on the top 10 ranks in a given column rank_sim_i
    Use pandas operations.
    """
    df_temp = embeds_df.copy()
    df_temp["Rank"] = df_temp[df_col_name].apply(lambda x: ast.literal_eval(x)[0])
    df_temp.sort_values(by="Rank", inplace=True)
    top_k_selected_schema_cols = df_temp.index[:top_k]

    return top_k_selected_schema_cols.values.tolist()


def modified_select_top_k_embeds(embeds_df, df_col_name, not_included_columns):
    top_k = TOP_K_DEFAULT_EMBEDS
    col_list = list(embeds_df.index)
    temp_list = [
        (int(ast.literal_eval(embeds_df[df_col_name][i])[0]), col_list[i])
        for i in range(len(embeds_df))
    ]
    temp_list.sort()

    final_embedded_col_list = []
    for rank_sim, column_name in temp_list:
        if column_name in not_included_columns:
            continue
        final_embedded_col_list.append(column_name)

    return final_embedded_col_list[0 : min(len(final_embedded_col_list), top_k)]


def modified_search_missing_columns(
    missing_cols_list, embeds_rank_df, question_num, not_included_columns
):
    ranks = []
    similarities = []
    rank_sim_col = "rank_sim_" + str(question_num)
    schema_columns = embeds_rank_df.index.values.tolist()
    temp_list = [
        (
            (
                int(ast.literal_eval(embed_rank_csv[rank_sim_col][i])[0]),
                float(ast.literal_eval(embed_rank_csv[rank_sim_col][i])[1]),
            ),
            schema_columns[i],
        )
        for i in range(len(embeds_rank_df))
    ]
    temp_list.sort()

    column_name_rank_dict = {}
    rank = 1
    for (r, sim), column_name in temp_list:
        if column_name in not_included_columns:
            continue

        column_name_rank_dict.update({column_name: (rank, sim)})
        rank += 1

    for col in missing_cols_list:
        if col in embeds_rank_df.index.values.tolist():
            ranks.append(column_name_rank_dict[col][0])
            similarities.append(column_name_rank_dict[col][1])
        else:
            ranks.append("N/A")
            similarities.append("N/A")

    return ranks, similarities


def modified_missing_columns(
    sql_query, column_list, column_names_from_schema, not_included_columns
):
    valid_char = [" ", "(", ")", ","]

    valid_columns = []
    for col_name in column_names_from_schema:
        index_list = re.finditer(pattern=col_name, string=sql_query)
        index_list = [index.start() for index in index_list]
        for index in index_list:
            flag = 1
            if index > 0 and sql_query[index - 1] not in valid_char:
                flag = 0
            if (
                index + len(col_name) < len(index_list)
                and sql_query[index + len(col_name)] not in valid_char
            ):
                flag = 0

            if flag and col_name not in not_included_columns:
                valid_columns.append(col_name)
                break

    missing_columns = [col for col in valid_columns if col not in column_list]
    return valid_columns, missing_columns, 1 if missing_columns else 0


def visualize_embeds(
    generations_df, embed_rank_df, schema_valid_column_names, not_included_columns
):
    # Initialize an empty list to store unmatched columns for each row
    generated_sql_queries = []
    selected_columns = []
    embed_ranks = []
    embed_similarities = []
    missing_columns = []
    is_missing_columns = []
    embed_rank_df_columns = embed_rank_df.columns
    generations_df_len = len(generations_df)
    total_correct = 0
    incorrect = 0
    not_evaluated = 0
    # Process each input string
    for i in range(generations_df_len):
        if (
            generations_df["generated_query"][i] == "not_evaluated"
            or f"rank_sim_{generations_df['#'].iloc[i]}" not in embed_rank_df_columns
        ):
            generated_sql_queries.append("not_evaluated")
            selected_columns.append("not_evaluated")
            missing_columns.append("not_evaluated")
            is_missing_columns.append("not_evaluated")
            embed_ranks.append("not_evaluated")
            embed_similarities.append("not_evaluated")
            not_evaluated += 1

        else:
            input_string = generations_df["generated_query"].iloc[i]
            sql2 = generations_df["correct_query"].iloc[i]
            question_num = generations_df["#"].iloc[i]
            df_col_name = "rank_sim_" + str(question_num)

            print(f"Question id {question_num}")

            # method1

            # # Find the position of the SQL query
            # query = input_string.strip()

            # # Extract the list part
            # selected_embed_list=select_top_k_embeds(embed_rank_df,df_col_name,not_included_columns)
            # # selected_embed_list = select_top_k_embeds(embed_rank_df, df_col_name)
            # print(selected_embed_list)
            # generated_sql_queries.append(query)

            # # Extract missing correct columns from the embedding list
            # _, missing_cols, is_missing = get_missing_columns(sql2, selected_embed_list,schema_valid_column_names)

            # # Search the ranks and similarities of the missing columns from the embedding rank csv
            # embed_ranks_list, embed_similarities_list = search_missing_columns(
            #     missing_cols, embed_rank_df, question_num
            # )

            # method2

            query = input_string.strip()

            # Extract the list part
            selected_embed_list = modified_select_top_k_embeds(
                embed_rank_df, df_col_name, not_included_columns
            )
            # selected_embed_list = select_top_k_embeds(embed_rank_df, df_col_name)
            generated_sql_queries.append(query)

            # Extract missing correct columns from the embedding list
            _, missing_cols, is_missing = modified_missing_columns(
                sql2,
                selected_embed_list,
                schema_valid_column_names,
                not_included_columns,
            )

            # Search the ranks and similarities of the missing columns from the embedding rank csv
            embed_ranks_list, embed_similarities_list = modified_search_missing_columns(
                missing_cols, embed_rank_df, question_num, not_included_columns
            )

            selected_columns.append(selected_embed_list)
            if is_missing == 1:
                incorrect += 1
            if is_missing == 0:
                total_correct += 1
            missing_columns.append(
                missing_cols
            ) if missing_cols else missing_columns.append("None")
            embed_ranks.append(
                embed_ranks_list
            ) if embed_ranks_list else embed_ranks.append("None")
            embed_similarities.append(
                embed_similarities_list
            ) if embed_similarities_list else embed_similarities.append("None")
            is_missing_columns.append(is_missing)
    # print("total_correct",total_correct)
    # print("incorrect",incorrect)
    # print("not_evaluated",not_evaluated)
    generations_df["Embedding_cols"] = selected_columns
    generations_df["Missing_cols"] = missing_columns
    generations_df["Missed_embed_ranks"] = embed_ranks
    generations_df["Missed_embed_similarities"] = embed_similarities
    generations_df["is_missing"] = is_missing_columns

    return generations_df


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-embeds",
        nargs="?",
        help="path of embedding ranks csv",
        type=str,
        default="data/embedding_ranks/embedding_ranks.csv",
    )
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
        help="path of output generations excel",
        type=str,
        default="data/embedding_ranks/generations.csv",
    )

    parsed_args = parser.parse_args()
    return parsed_args.embeds, parsed_args.i, parsed_args.o


if __name__ == "__main__":
    [
        file_path_of_embedding_ranks_csv,
        file_path_of_input_generations_csv,
        file_path_of_export_embeddings_excel,
    ] = get_args()

    schema_csv = pd.read_csv(SCHEMA_FILE)
    schema_valid_column_names = [col_name for col_name in schema_csv["Column Name"]]
    generations_csv = pd.read_csv(file_path_of_input_generations_csv)
    not_included_column_names = [
        "event_date",
        "persona_name",
        "participant_name",
        "event_time",
    ]
    embed_rank_csv = pd.read_csv(file_path_of_embedding_ranks_csv, index_col=0)

    embeds_df = visualize_embeds(
        generations_csv,
        embed_rank_csv,
        schema_valid_column_names,
        not_included_column_names,
    )

    # Save the updated DataFrame to the same Excel file
    embeds_df.to_csv(file_path_of_export_embeddings_excel, index=False)
