0.1.13 `October 17, 2023`

- Added embeddings for GPT4.
- Added prompts as text files.
- prompt file can be provided with cli option
- Created a tool/job to test different prompts.

  0.1.12 `October 11, 2023`

- Added functionality for automatic multiple table selection.
- Merged the code for manual multiple table selection.

  0.1.11 `October 3, 2023`

- Added persona_id, start_date, end_date as external filters that can be taken from UI.

  0.1.10 `September 25, 2023`

- Added GPT-4 Azure API token.

  0.1.9 `September 18, 2023`

- Corrected the code for getting embedding columns with the rank and similarities in a csv.
- Corrected the code for obtaining missing embedding columns in an excel file.

  0.1.8 `September 11, 2023`

- The SERVER OVERLOAD ERROR in gradio is fixed.
- The v1 askskan code is stable and fully functional.

  0.1.7 `September 11, 2023`

- Cleaned the codebase for v1 (free of anything related to embedding tests).

  0.1.6 `September 11, 2023`

- Reinstated the v1 askskan gradio.

  0.1.5 `September 11, 2023`

- Reinstated the v1 askskan codebase.

  0.1.4 `September 1, 2023`

- Added code for getting embeddings.
- Added code for visualizing embeddings.

  0.1.3 `August 24, 2023`

- Added code to fetch selected schema columns from embeddings.

  0.1.2 `August 23, 2023`

- Added temperature argument to the CLI.
- Added a new zero shot prompt.

  0.1.1 `August 21, 2023`

- Added v4 CoT prompt that can also take doubts from human (still in progress).
- Separated Reasoning, Doubts and the SQL result sections in the output.
- Added database agent to experiment with selection of different tables.

  0.1.0 `August 16, 2023`

- Added clear vectorstore and session to the gradio
- Separated the prompts into separate files based on one-shot/zero_shot/few_shot technique.

  0.0.20 `August 10, 2023`

- Removed unnecessary files.
- Minor tweaks done to the input prompt and schema.

  0.0.19 `August 4, 2023`

- Removed unnecessary data files.
- Updated schema.csv ordering according to schema.py ordering.
- Updated bot friendly responses to incorporate different kinds of statements.

  0.0.18 `August 3, 2023`

- Added -clean to the docker for cleaning data in every deployment.

  0.0.17 `August 1, 2023`

- Added --model_verbose flag to get the langchain verbose on the terminal.
- Clears debug window on clear history and new user, yet to integrate clear history and new user.

  0.0.16 `August 1, 2023`

- Fully hardcoded the query for getting last and first events for the day.

  0.0.15 `August 1, 2023`

- Fixed bug involving return of sql query also.
- Fixed the last event for the day error.
- Added the clipboard example in the prompt.

  0.0.14 `July 31, 2023`

- changed limit to 10 for some queries.
- Updated average processing time per case example

  0.0.13 `July 31, 2023`

- added clean argument to cli for cleaning previous sessions and vectorstore.
- Now sending SQL query to the debugging window.

  0.0.12 `July 31, 2023`

- added more examples to get better answers(MOHD AZAM)

  0.0.11 `July 28, 2023`

- Removed activity_alias_name from schema.
- Slightly updated prompt instruction to inform about different fields present in the schema csv.
- Updated TaT_event to tat_event.
- Updated case_id_value in definitions.
- Updated utlilization definition.
- Updated case touches in the definition.
- Updated processing time per case example in the prompt.
- Updated activity_id in the prompt examples.

  0.0.10 `July 28, 2023`

- Added username entry and logging.
- Logging username on clear history.

  0.0.9 `July 28, 2023`

- updated prompts and descriptions to improve answers
- Added username request first

  0.0.8 `July 28, 2023`

- Added utilization to definitions file.
- Removed None type feedback and review

- 0.0.7 `July 27, 2023`

_0.0.7_ `July 27, 2023`

- Updated instruction prompts by adding examples for wrong questions.
- Added placeholder for username.
- Log on server start

  0.0.6 `July 26, 2023`

- Updated participant and persona descriptions in the schema and definitions.
- Updated event_time and event_date descriptions in the schema.
- Update other time descriptions in the definition and schema.
- Updated the instruction to generate max 10 rows.
- Made the user_id random.

  0.0.5 `July 26, 2023`

- Added support for --rootpath or -RP

  0.0.4 `July 25, 2023`

- Added functionality for clear history, creating new session
- Added functionality for regenerate response
- Updated README for CLI arguments

  0.0.3 `July 25, 2023`

- Added --streamlog option that will stream logs to console for server logging
- Added --auth or -A option that will read USERNAME and PASSWORD from env for GUI

  0.0.2 `July 24, 2023`

- Fixed the case when the response does not include any query

  0.0.1 `July 24, 2023`

- Added changelog support
- Added verbose option
- Show version number in gradio UI (from first line of this file)
