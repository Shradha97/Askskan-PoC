import sys
import random
import asyncio

import gradio as gr
from app.configurations.development.settings import VERSION, CHANGELOG


def log_review_fn(review, logger):
    logger.logger.info(f"REVIEW: {review}")


def hide_fn():
    return gr.Textbox.update(visible=False)


def show_fn():
    return gr.Textbox.update(visible=True)


def gradio_ui(
    askskan_qa_manager, askskan_bot, buffer_memory, logger, user_id, session_id
):
    # Front end web app
    with gr.Blocks(title="Ask Skan") as demo:
        user_id_gradio = gr.Number(value=user_id, visible=False, label="User ID")
        session_id_gradio = gr.Number(
            value=session_id, visible=False, label="Session ID"
        )
        username_string_gradio = gr.Textbox(
            show_label=False, interactive=True, visible=False
        )

        with gr.Row():
            with gr.Column(scale=2.5):
                with gr.Accordion("Please enter your username first!", Open=True):
                    username = gr.Textbox(
                        show_label=False,
                        lines=1,
                        placeholder="Type your username here",
                        interactive=True,
                    ).style(container=False)
                    submit_user = gr.Button(value="Enter")

                with gr.Accordion("Dubugging Window", open=False):
                    debug_textbox = gr.Textbox(
                        show_label=False,
                        lines=10,
                        value="",
                        placeholder="Debugging message will appear here",
                        interactive=True,
                    ).style(container=False)

                    # Show/Hide buttons
                    with gr.Row():
                        show_debug = gr.Button(value="Show Message")
                        hide_debug = gr.Button(value="Hide Message")

                with gr.Accordion("Have feedback on the answer?", Open=True):
                    feedback = gr.Textbox(
                        show_label=False,
                        lines=1,
                        placeholder="Type your feedback here",
                        interactive=True,
                    ).style(container=False)

                    submit_feedback = gr.Button(value="Submit")
                gr.Markdown(f"{VERSION}")

                with gr.Row():
                    gr.Dropdown(
                        ["2023-04-01"],
                        label="Start Date",
                        allow_custom_value=True,
                        value="2023-04-01",
                        info="Select the start date for the results. You can also type in a custom date.",
                    ),
                    gr.Dropdown(
                        ["2023-04-30"],
                        label="End Date",
                        allow_custom_value=True,
                        value="2023-04-30",
                        info="Select the end date for the results. You can also type in a custom date.",
                    ),
                    gr.Dropdown(
                        ["LES", "CES", "ES", "Do not Use", "TEST", None],
                        label="Persona",
                        allow_custom_value=True,
                        value=None,
                        info="Select the persona you want the results for. You can also type in a custom persona.",
                    ),

            with gr.Column(scale=6.5):
                skanbot = gr.Chatbot()
                question = gr.Textbox(
                    show_label=False,
                    lines=1,
                    placeholder="Type a question and press ENTER",
                ).style(container=False)

                with gr.Row():
                    upvote = gr.Button(
                        "\U0001F44D Upvote",
                        label="Click to upvote!",
                        scale=0,
                    )
                    downvote = gr.Button(
                        "\U0001F44E Downvote",
                        label="Click to downvote!",
                        scale=0,
                    )
                    flag = gr.Button(
                        "\u26A0 Report",
                        label="Click to flag it!",
                        scale=0,
                    )

                    regenerate_response = gr.Button("\U0001F504 Regenerate")
                    clear_history = gr.Button("\U0001F5D1 Clear History")

        def enter_username_fn(username_string):
            debug_textbox.value = ""

            user_id = random.randint(1, sys.maxsize)
            buffer_memory.chat_memory = (
                askskan_qa_manager.sessions_manager_engine.create_new_session(
                    user_id,
                    session_id_gradio.value,
                    username=username_string,
                )
            )
            user_id_gradio.value = user_id
            session_id_gradio.value = session_id
            username_string_gradio.value = username_string
            logger.update_logger_session(user_id, session_id)
            logger.logger.debug(f"A new user entered, created new session")
            logger.logger.info(f"USERNAME: {username_string_gradio.value}")
            # clear_history_fn()
            return gr.update(value="")

        def clear_history_fn():
            debug_textbox.value = ""

            askskan_qa_manager.document_retrieval_engine.delete_vectorstore_file
            askskan_qa_manager.sessions_manager_engine.delete_sessions_file
            logger.logger.debug(
                f"Cleared vectorstore and sessions file on clicking clear history button"
            )

            buffer_memory.chat_memory.clear()
            session_id_updated = (
                askskan_qa_manager.sessions_manager_engine.create_new_session_id(
                    user_id_gradio.value, session_id_gradio.value
                )
            )
            session_id_gradio.value = session_id_updated
            logger.update_logger_session(user_id_gradio.value, session_id_updated)
            logger.logger.debug(
                f"Cleared chat screen history, created new session for USERNAME: {username_string_gradio.value}"
            )

            return gr.update(value="")

        def regenerate_response_fn(history):
            debug_textbox.value = ""

            logger.logger.debug(f"Regenerating new response...")
            history[-1][1] = None
            return history

        def log_feedback_fn(feedback_message):
            global feedback_logged
            logger.logger.info(f"FEEDBACK: {feedback_message}")
            return gr.update(value="")

        def show_debug_msg_fn():
            return gr.update(value=debug_textbox.value)

        def bot(history):
            user_message = history[-1][0]

            response, debugging_msg = askskan_qa_manager.get_answer(
                user_message, askskan_bot, logger
            )

            debug_textbox.value = debugging_msg

            # FIXME: write this in a better way, saving after every run-> not optimal
            askskan_qa_manager.sessions_manager_engine.update_session(
                user_id,
                # session_id,
                session_id_gradio.value,
                chat_history=buffer_memory.chat_memory,
                save_session=True,
            )
            history[-1][1] = response

            return history

        def user(user_message, history):
            logger.logger.info(f"QUESTION: {user_message}")
            return gr.update(value=""), history + [[user_message, None]]

        question.submit(
            user, [question, skanbot], [question, skanbot], queue=False
        ).then(bot, skanbot, skanbot, queue=False)

        # clear the screen and create a new session
        clear_history.click(
            clear_history_fn,
            outputs=skanbot,
            queue=False,
        )

        regenerate_response.click(regenerate_response_fn, skanbot, skanbot).then(
            bot, skanbot, skanbot, queue=False
        )

        # attach click method for submit feedback button
        submit_user.click(
            enter_username_fn,
            username,
            username,
            queue=False,
        )

        # attach click methods for review buttons
        upvote.click(lambda: log_review_fn("upvote", logger), queue=False)
        downvote.click(lambda: log_review_fn("downvote", logger), queue=False)
        flag.click(lambda: log_review_fn("report", logger), queue=False)

        submit_feedback.click(
            log_feedback_fn,
            feedback,
            feedback,
            queue=False,
        )

        # Show/Hide buttons
        hide_debug.click(hide_fn, outputs=[debug_textbox])
        show_debug.click(show_fn, outputs=[debug_textbox])

        demo.load(
            show_debug_msg_fn,
            inputs=None,
            outputs=[debug_textbox],
            every=1,  # units in seconds)
        )
    return demo.queue()
