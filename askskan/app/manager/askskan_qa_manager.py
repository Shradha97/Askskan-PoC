from databricks import sql
import os
import json
from app.configurations.development.config_parser import args
from app.engine.query_generation_engine import QueryGenerationEngine
from app.engine.memory_engine import MemoryEngine
from app.engine.prompts_engine import PromptsEngine
from app.engine.postprocessing_engine import PostProcessingEngine
from app.engine.sessions_manager_engine import SessionsManagerEngine
from app.engine.document_retrieval_engine import DocumentRetrievalEngine
from app.engine.table_selection_engine import TableSelectionEngine
from app.configurations.development.settings import (
    FALLBACK_MESSAGE,
    SERVER_OVERLOAD_MESSAGE,
    TEMPERATURE,
    SCHEMA_COLS_PATTERN,
)
from utils.callbacks.logging_callback_handler import LoggingCallbackHandler


class AskSkanQAManager:
    def __init__(
        self,
        memory_engine: MemoryEngine,
        document_retrieval_engine: DocumentRetrievalEngine,
        prompts_engine: PromptsEngine,
        query_generation_engine: QueryGenerationEngine,
        table_selection_engine: TableSelectionEngine,
        post_processing_engine: PostProcessingEngine,
        sessions_manager_engine: SessionsManagerEngine,
        logging_callback_handler: LoggingCallbackHandler = LoggingCallbackHandler(),
    ):
        self.memory_engine = memory_engine
        self.document_retrieval_engine = document_retrieval_engine
        self.prompts_engine = prompts_engine
        self.query_generation_engine = query_generation_engine
        self.table_selection_engine = table_selection_engine
        self.postprocessing_engine = post_processing_engine
        self.sessions_manager_engine = sessions_manager_engine
        self.logging_callback_handler = logging_callback_handler

        self.retriever = None

    def _execute_pyspark_query(self, query, logger):
        DBWS_HOST = os.getenv("dbws_host_domain")
        DBWS_HTTP_PATH = os.getenv("dbws_host_path")
        DBWS_PAT = os.getenv("dbws_pat")

        result_rows = []

        with sql.connect(
            server_hostname=DBWS_HOST, http_path=DBWS_HTTP_PATH, access_token=DBWS_PAT
        ) as conn:
            with conn.cursor() as cursor:
                logger.logger.debug("Executing query on the datalake server...")
                cursor.execute(query)
                result = cursor.fetchall()
                logger.logger.debug("Query executed successfully and results fetched!")

                for row in result:
                    result_rows.append(row)
        if len(result_rows) == 1:
            return result_rows[0]

        return result_rows

    def get_qa_chain(self, chat_history, model_verbose=False):
        self.retriever = (
            self.document_retrieval_engine.get_vectorstore_data().as_retriever()
        )
        combine_docs_chain_kwargs = self.query_generation_engine.get_chain_type_kwargs(
            instruction_prompt=self.prompts_engine.get_qa_prompt()
        )

        question_gen_llm = self.query_generation_engine.get_question_generation_llm()
        combine_docs_llm = self.query_generation_engine.get_combine_doc_llm(
            streaming=True, temperature=args.temperature
        )
        buffer_memory = self.memory_engine.get_buffer_memory(chat_history)

        qa_chain = self.query_generation_engine.get_query_generation_chain(
            memory=buffer_memory,
            combine_doc_llm=combine_docs_llm,
            retriever=self.retriever,
            question_generation_llm=question_gen_llm,
            combine_docs_chain_kwargs=combine_docs_chain_kwargs,
            verbose=model_verbose,
            tracing=False,
        )

        return qa_chain, buffer_memory

    def get_table_selection_chain(self, model_verbose=False):
        table_selection_prompt = self.prompts_engine.get_table_selection_prompt()
        table_selection_llm = self.table_selection_engine.get_table_selection_llm(
            temperature=args.temperature, verbose=model_verbose
        )

        table_selection_chain = self.table_selection_engine.get_table_selection_chain(
            table_selection_llm=table_selection_llm,
            table_selection_prompt=table_selection_prompt,
            verbose=model_verbose,
        )

        return table_selection_chain

    def combine_responses_from_llm_chains(
        self, user_input, qa_chain, logger, model_verbose=False
    ):
        selected_tables_dict = None
        if not args.no_multitable:
            logger.logger.debug("Entering table selection chain...")
            table_selection_chain = self.get_table_selection_chain(model_verbose)
            selected_table_string = table_selection_chain.predict(question=user_input)
            selected_tables_dict = json.loads(selected_table_string)

            logger.logger.debug(
                "Finished table selection chain, obtained selected tables as a dictionary"
            )

            # print("Tables:", selected_tables_dict)
            logger.logger.info("TABLES: {}".format(selected_tables_dict))
            if selected_tables_dict == FALLBACK_MESSAGE:
                logger.logger.debug(
                    "Exception occurred during extraction of selected tables from the dict response"
                )
                return FALLBACK_MESSAGE
        qa_chain_input = self.query_generation_engine.query_generation_chain_input(
            user_input, selected_tables_dict
        )
        logger.logger.debug("Entering QA retrieval chain...")
        result = qa_chain(qa_chain_input)
        logger.logger.debug("Finished model reponse retrieval")

        return result["answer"].strip()

    def get_answer(self, user_input, qa_chain, logger):
        # Add a case when the previous doubt and the current doubt are the same, sometimes the model gets stuck. \
        #    -> rerun the chain.
        # other case would be of continual learning.

        generated_query = None
        debugging_query = None

        try:
            # Added logging for QA retrieval chain
            generated_output = self.combine_responses_from_llm_chains(
                user_input, qa_chain, logger
            )
        except Exception:
            logger.logger.exception("Failed to retrieve model response")
            generated_output = SERVER_OVERLOAD_MESSAGE

        try:
            # Added logging for postprocessing for extracting SQL query
            logger.logger.debug("Extracting SQL query from JSON reponse...")
            generated_query, is_query = self.postprocessing_engine.extract_sql_query(
                generated_output
            )

            debugging_query = generated_query

            if not is_query:
                bot_response = generated_query
                logger.logger.debug("Not a SQL query, returning statement as is")
            else:
                logger.logger.debug("Finished extracting SQL query")
                (
                    columns,
                    friendly_response,
                ) = self.postprocessing_engine.extract_extra_fields()
                logger.logger.info("JSON_QRY: {}".format(generated_query))
                logger.logger.info("JSON_COL: {}".format(columns))
                logger.logger.info("JSON_BOT: {}".format(friendly_response))

                # if want only sql query
                if args.sql and not args.query_result and not args.full_result:
                    return (
                        generated_query,
                        debugging_query,
                    )

                # Added logging for query execution
                logger.logger.debug("Executing SQL query...")
                query_result = self._execute_pyspark_query(generated_query, logger)
                logger.logger.debug("QUERY_RESULT: {}".format(query_result))

                # Added logging for postprocessing for obtaining final bot response
                logger.logger.debug("Formatting final response...")
                (
                    bot_response,
                    result_list,
                ) = self.postprocessing_engine.get_final_bot_response_from_sql(
                    query_result, friendly_response, columns
                )
                logger.logger.debug("Finished formatting final response")

        except Exception as e:
            debugging_query = str(e)
            if generated_output == SERVER_OVERLOAD_MESSAGE:
                bot_response = SERVER_OVERLOAD_MESSAGE
            else:
                # logger.exception("Failed processing generated SQL query")
                logger.logger.exception(
                    "Exception occurred during processing: {}".format(str(e))
                )
                bot_response = FALLBACK_MESSAGE

        logger.logger.info(f"SKANBOT : {bot_response}")

        if args.sql:
            return {
                "Query": generated_query,
                "Result": bot_response,
            }
        return (
            bot_response,
            debugging_query,
        )
