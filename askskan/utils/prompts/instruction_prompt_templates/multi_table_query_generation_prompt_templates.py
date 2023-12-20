from langchain.prompts.prompt import PromptTemplate
from utils.prompts.query_generation_prompts.few_shot_prompt import (
    multitable_few_shot_prompt_with_additional_instruction_with_persona,
    multitable_few_shot_prompt_without_additional_instruction_with_persona,
    multitable_few_shot_prompt_with_additional_instruction_without_persona,
    multitable_few_shot_prompt_without_additional_instruction_without_persona,
)

common_input_variables = [
    "context",
    "abstraction_instances_schema",
    "worktime_metrics_schema",
    "events_schema_definitions",
    "abstraction_instances_schema_definitions",
    "worktime_metrics_schema_definitions",
    "data_table_dictionary",
    "question",
    "chat_history",
    "start_date",
    "end_date",
    "examples",
]

QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA = PromptTemplate(
    template=multitable_few_shot_prompt_with_additional_instruction_with_persona,
    input_variables=common_input_variables + ["persona_id", "additional_instructions"],
)

QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA = PromptTemplate(
    template=multitable_few_shot_prompt_with_additional_instruction_without_persona,
    input_variables=common_input_variables + ["additional_instructions"],
)
QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA = PromptTemplate(
    template=multitable_few_shot_prompt_without_additional_instruction_with_persona,
    input_variables=common_input_variables + ["persona_id"],
)

QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA = PromptTemplate(
    template=multitable_few_shot_prompt_without_additional_instruction_without_persona,
    input_variables=common_input_variables,
)
