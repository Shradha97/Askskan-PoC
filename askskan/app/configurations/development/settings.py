import os
from dotenv import load_dotenv, find_dotenv
from app.configurations.development.config_parser import args
import yaml

_ = load_dotenv(find_dotenv())  # read local .env

# loading configurations
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


# Azure API Keys
AZURE_API_BASE = (
    os.getenv("AZURE_OPENAI_ENDPOINT")
    if args.gpt_35_azure
    else os.getenv("AZURE_OPENAI_GPT4_ENDPOINT")
)
AZURE_API_KEY = (
    os.getenv("AZURE_OPENAI_KEY")
    if args.gpt_35_azure
    else os.getenv("AZURE_OPENAI_GPT4_KEY")
)
AZURE_API_TYPE = "azure"
MODEL_DEPLOYMENT_NAME = (
    os.getenv("AZURE_OPENAI_DNAME")
    if args.gpt_35_azure
    else os.getenv("AZURE_OPENAI_GPT4_DNAME")
)

EMBED_DEPLOYMENT_NAME = (
    os.getenv("AZURE_OPENAI_EMBED_NAME")
    if args.gpt_35_azure
    else os.getenv("AZURE_OPENAI_GPT4_EMBED_NAME")
)
EMBED_API_VERSION = "2022-12-01"
MODEL_API_VERSION = "2023-05-15"

# Personal API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Data
DATA_FILE = "data/sample/data0.csv"
METADATA_FILE = "data/original/metadata/major_tables_metadata.yaml"

EVENTS_DATA_TABLE_NAME = config["table_name_in_dl"]
ACTIVE_SCHEMA_FOLDER = config["active_schema_folder_name"]
MULTIPLE_TABLE_SELECTION_EXAMPLES_FOLDER = config[
    "multiple_table_selection_examples_folder_name"
]

VECTORSTORE_FILE = f"data/vectorstore/vectorstore_{ACTIVE_SCHEMA_FOLDER}.pkl"
SESSIONS_FILE = f"data/sessions/sessions_{ACTIVE_SCHEMA_FOLDER}.pkl"

# Single table selection prompt input files
SCHEMA_FILE = f"data/original/input_tables/{ACTIVE_SCHEMA_FOLDER}/schema.csv"
SCHEMA_DEFINITIONS_FILE = (
    f"data/original/input_tables/{ACTIVE_SCHEMA_FOLDER}/definitions.txt"
)
PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE = (
    f"data/original/input_tables/{ACTIVE_SCHEMA_FOLDER}/examples_without_persona.txt"
)
PROMPT_EXAMPLES_WITH_PERSONA_FILE = (
    f"data/original/input_tables/{ACTIVE_SCHEMA_FOLDER}/examples_with_persona.txt"
)
ADDITIONAL_PROMPT_INSTRUCTIONS_FILE = (
    f"data/original/input_tables/{ACTIVE_SCHEMA_FOLDER}/additional_instructions.txt"
)

# Multiple table selection prompt input files
MULTIPLE_TABLE_SELECTION_PROMPT_EXAMPLES_FILE = f"data/original/{MULTIPLE_TABLE_SELECTION_EXAMPLES_FOLDER}/multiple_table_selection_examples.txt"
MULTITABLE_PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE = (
    f"data/original/input_tables/events/multitable_examples_without_persona.txt"
)
MULTITABLE_PROMPT_EXAMPLES_WITH_PERSONA_FILE = (
    f"data/original/input_tables/events/multitable_examples_with_persona.txt"
)
WORKTIME_METRICS_SCHEMA_FILE = f"data/original/input_tables/worktime_metrics/schema.csv"
ABSTRACTION_INSTANCES_SCHEMA_FILE = (
    f"data/original/input_tables/abstraction_instances/schema.csv"
)
EVENTS_SCHEMA_DEFINITIONS_FILE = f"data/original/input_tables/events/definitions.txt"
ABSTRACTION_INSTANCES_SCHEMA_DEFINITIONS_FILE = (
    f"data/original/input_tables/abstraction_instances/definitions.txt"
)
WORKTIME_METRICS_SCHEMA_DEFINITIONS_FILE = (
    f"data/original/input_tables/worktime_metrics/definitions.txt"
)

# Query Generation Prompt text files
PROMPT_FILE = f"data/original/prompts/{str(args.prompt_file_name)}.txt"
FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA_FILE = "data/original/prompts/query_generation_prompt/few_shot_prompt_with_additional_instruction_with_persona.txt"
FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA_FILE = "data/original/prompts/query_generation_prompt/few_shot_prompt_without_additional_instruction_with_persona.txt"
FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA_FILE = "data/original/prompts/query_generation_prompt/few_shot_prompt_with_additional_instruction_without_persona.txt"
FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA_FILE = "data/original/prompts/query_generation_prompt/few_shot_prompt_without_additional_instruction_without_persona.txt"
MULTITABLE_FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA_FILE = "data/original/prompts/query_generation_prompt/multitable_few_shot_prompt_with_additional_instruction_with_persona.txt"
MULTITABLE_FEW_SHOT_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA_FILE = "data/original/prompts/query_generation_prompt/multitable_few_shot_prompt_with_additional_instruction_without_persona.txt"
MULTITABLE_FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA_FILE = "data/original/prompts/query_generation_prompt/multitable_few_shot_prompt_without_additional_instruction_with_persona.txt"
MULTITABLE_FEW_SHOT_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA_FILE = "data/original/prompts/query_generation_prompt/multitable_few_shot_prompt_without_additional_instruction_without_persona.txt"

# Table selection prompt files
TABLE_SELECTION_PROMPT = (
    "data/original/prompts/table_selection_prompt/table_selection.txt"
)


# Model response sections
MODEL_OUTPUT_FIELD = "Output: "
MODEL_ANSWER_FIELD = "answer"
MODEL_QUERY_FIELD = "Query"
MODEL_COLUMN_FIELD = "Column"
MODEL_CODE_FIELD = "Code"
MODEL_DOUBT_FIELD = "Doubt"
MODEL_REASONING_FIELD = "Reasoning"
MODEL_BOT_RESPONSE_FIELD = "Skan Bot"

# Prompt template filters
QUERY_START_DATE = "2023-04-01"
QUERY_END_DATE = "2023-04-30"

# Model Hyperparameters
TEMPERATURE = 0.2
TOP_K_EMBEDS = 41
TOP_K_DEFAULT_EMBEDS = 7

# Regex patterns
SCHEMA_COLS_PATTERN = r"Column Name:(.*?)(Type:)"

# Error Messages
FALLBACK_MESSAGE = "Sorry, I'm not intelligent enough to answer your question now. Please try again or with a different question!"
SERVER_OVERLOAD_MESSAGE = "Sorry, I'm overloaded with requests. Please try again later!"

# Changelog versioning
CHANGELOG = open("../changelog/Changelog_AskSkan.md", "r").readlines()
VERSION = CHANGELOG[0]

# WebUI server credentials
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST_NAME = "0.0.0.0"
