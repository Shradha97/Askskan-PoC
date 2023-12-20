import warnings
from app.configurations.development.config_parser import args
from app.configurations.development.settings import (
    USERNAME,
    PASSWORD,
    HOST_NAME,
    VERSION,
)
from utils.UI.gradio import gradio_ui
from utils.logger import Logger


from app.engine.document_retrieval_engine import DocumentRetrievalEngine
from app.engine.prompts_engine import PromptsEngine
from app.engine.query_generation_engine import QueryGenerationEngine
from app.engine.table_selection_engine import TableSelectionEngine
from app.engine.memory_engine import MemoryEngine
from app.engine.postprocessing_engine import PostProcessingEngine
from app.engine.sessions_manager_engine import SessionsManagerEngine
from app.manager.askskan_qa_manager import AskSkanQAManager

warnings.filterwarnings("ignore")


def get_askskan_qa_manager(logger, persona_id, start_date, end_date):
    document_retrieval_engine = DocumentRetrievalEngine()
    prompts_engine = PromptsEngine(
        document_retrieval_engine, start_date, end_date, persona_id
    )

    logger.logger.info(f"QUERY START DATE: {start_date}")
    logger.logger.info(f"QUERY END DATE: {end_date}")
    logger.logger.info(f"PERSONA ID: {persona_id}")

    askskan_qa_manager = AskSkanQAManager(
        memory_engine=MemoryEngine(),
        query_generation_engine=QueryGenerationEngine(),
        table_selection_engine=TableSelectionEngine(),
        post_processing_engine=PostProcessingEngine(),
        sessions_manager_engine=SessionsManagerEngine(logger.logger),
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
    askskan_qa_manager,
    askskan_bot,
    buffer_memory,
    logger,
    user_id,
    session_id,
):
    bot_response, _ = askskan_qa_manager.get_answer(user_input, askskan_bot, logger)

    # updating the session history and saving the session
    askskan_qa_manager.sessions_manager_engine.update_session(
        user_id, session_id, chat_history=buffer_memory.chat_memory, save_session=True
    )
    return bot_response
    # FIXME: This print gets considered as you in the next iteration.


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

    # taking persona_id, end_date and start_date as input from UI filters
    (
        persona_id,
        start_date,
        end_date,
    ) = get_input_filters()

    logger_obj = Logger(user_id, session_id, log_file=log_file)
    logger_obj.logger.info(f"Starting service... ({VERSION})")

    # initializing the required objects
    askskan_qa_manager = get_askskan_qa_manager(
        logger_obj, persona_id, start_date, end_date
    )

    # cleaning the vectorstore and the sessions
    if clean:
        askskan_qa_manager.document_retrieval_engine.delete_vectorstore_file
        askskan_qa_manager.sessions_manager_engine.delete_sessions_file
        logger_obj.logger.debug(f"Removed previous sessions and vectorstore files")

    session_chat_history = (
        askskan_qa_manager.sessions_manager_engine.get_session_history(
            user_id, session_id
        )
    )

    # setting the chat history for the session
    askskan_bot, buffer_memory = askskan_qa_manager.get_qa_chain(
        session_chat_history, model_verbose
    )

    # running the job through cli or gradio
    if question != "":
        result = cli_ui(
            args.question,
            askskan_qa_manager,
            askskan_bot,
            buffer_memory,
            logger_obj,
            user_id,
            session_id,
        )

        if args.verbose == False:
            print(result)
    elif bot_format:
        while True:
            user_input = input("You: ")
            bot_response = cli_ui(
                user_input,
                askskan_qa_manager,
                askskan_bot,
                buffer_memory,
                logger_obj,
                user_id,
                session_id,
            )
            print("Bot: ", bot_response)
    else:
        demo = gradio_ui(
            askskan_qa_manager,
            askskan_bot,
            buffer_memory,
            logger_obj,
            user_id,
            session_id,
        )
        if args.auth:
            demo.launch(
                root_path=args.rootpath,
                auth=(USERNAME, PASSWORD),
                server_name=HOST_NAME,
            )
        else:
            demo.launch(
                root_path=args.rootpath, share=False, debug=True, server_name=HOST_NAME
            )
