from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.engine.document_retrieval_engine import DocumentRetrievalEngine
from app.configurations.development.config_parser import args
import re
from utils.prompts.instruction_prompt_templates.table_selection_prompt_templates import (
    MULTIPLE_TABLES_SELECTION_PROMPT,
)

if args.prompt_file_name:
    from app.configurations.development.settings import PROMPT_FILE

from app.configurations.development.settings import (
    SCHEMA_DEFINITIONS_FILE,
    QUERY_START_DATE,
    QUERY_END_DATE,
    EVENTS_DATA_TABLE_NAME,
    METADATA_FILE,
    WORKTIME_METRICS_SCHEMA_FILE,
    ABSTRACTION_INSTANCES_SCHEMA_FILE,
    EVENTS_SCHEMA_DEFINITIONS_FILE,
    ABSTRACTION_INSTANCES_SCHEMA_DEFINITIONS_FILE,
    WORKTIME_METRICS_SCHEMA_DEFINITIONS_FILE,
)
from app.configurations.development.settings import (
    PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE,
    PROMPT_EXAMPLES_WITH_PERSONA_FILE,
    ADDITIONAL_PROMPT_INSTRUCTIONS_FILE,
    MULTIPLE_TABLE_SELECTION_PROMPT_EXAMPLES_FILE,
    MULTITABLE_PROMPT_EXAMPLES_WITH_PERSONA_FILE,
    MULTITABLE_PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE,
)

if args.no_multitable:
    from utils.prompts.instruction_prompt_templates.query_generation_prompt_templates import (
        QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA,
        QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA,
        QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA,
        QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA,
    )
else:
    from utils.prompts.instruction_prompt_templates.multi_table_query_generation_prompt_templates import (
        QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA,
        QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA,
        QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA,
        QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA,
    )


class PromptsEngine:
    def __init__(
        self,
        document_retrieval_engine: DocumentRetrievalEngine,
        start_date: str,
        end_date: str,
        persona_id: int = None,
    ):
        self.document_retrieval_engine = document_retrieval_engine
        self.persona_id = persona_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_additional_instructions_given = False

    def _prompt_input_variables(self, is_table_selection_prompt: bool = False):
        """
        Returns the input variables for the prompt template that need not be passed to the LLM chain as input
        """
        if is_table_selection_prompt:
            try:
                examples = self.document_retrieval_engine.get_raw_data(
                    MULTIPLE_TABLE_SELECTION_PROMPT_EXAMPLES_FILE, data_type="text"
                )
            except:
                examples = "no examples given"

            return dict(
                table_metadata=self.document_retrieval_engine.get_raw_data(
                    METADATA_FILE, data_type="text"
                ),
                examples=examples,
            )
        elif args.no_multitable:
            try:
                prompt_examples_file = (
                    PROMPT_EXAMPLES_WITH_PERSONA_FILE
                    if self.persona_id
                    else PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE
                )
                examples = self.document_retrieval_engine.get_raw_data(
                    prompt_examples_file, data_type="text"
                )
            except:
                examples = "no examples given"

            return dict(
                schema_definitions=self.document_retrieval_engine.get_raw_data(
                    SCHEMA_DEFINITIONS_FILE, data_type="text"
                ),
                start_date=self.start_date if self.start_date else QUERY_START_DATE,
                end_date=self.end_date if self.end_date else QUERY_END_DATE,
                data_table_name=EVENTS_DATA_TABLE_NAME,
                examples=examples,
            )
        else:
            try:
                prompt_examples_file = (
                    MULTITABLE_PROMPT_EXAMPLES_WITH_PERSONA_FILE
                    if self.persona_id
                    else MULTITABLE_PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE
                )
                examples = self.document_retrieval_engine.get_raw_data(
                    prompt_examples_file, data_type="text"
                )
            except:
                examples = "no examples given"

            return dict(
                events_schema_definitions=self.document_retrieval_engine.get_raw_data(
                    EVENTS_SCHEMA_DEFINITIONS_FILE, data_type="text"
                ),
                abstraction_instances_schema_definitions=self.document_retrieval_engine.get_raw_data(
                    ABSTRACTION_INSTANCES_SCHEMA_DEFINITIONS_FILE, data_type="text"
                ),
                worktime_metrics_schema_definitions=self.document_retrieval_engine.get_raw_data(
                    WORKTIME_METRICS_SCHEMA_DEFINITIONS_FILE, data_type="text"
                ),
                abstraction_instances_schema=self.document_retrieval_engine.get_raw_data(
                    ABSTRACTION_INSTANCES_SCHEMA_FILE, data_type="text"
                ),
                worktime_metrics_schema=self.document_retrieval_engine.get_raw_data(
                    WORKTIME_METRICS_SCHEMA_FILE, data_type="text"
                ),
                data_table_dictionary=self.document_retrieval_engine.get_raw_data(
                    METADATA_FILE, data_type="text"
                ),
                start_date=self.start_date if self.start_date else QUERY_START_DATE,
                end_date=self.end_date if self.end_date else QUERY_END_DATE,
                examples=examples,
            )

    def _partial_prompt(self, is_table_selection_prompt: bool = False):
        """
        Returns the partial prompt template based on whether the persona_id is passed or not and weather additional information is given or not
        """
        if is_table_selection_prompt:
            return MULTIPLE_TABLES_SELECTION_PROMPT
        else:
            if self.is_additional_instructions_given and self.persona_id:
                return QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITH_PERSONA
            if self.is_additional_instructions_given:
                return QUERY_GENERATION_PROMPT_WITH_ADDITIONAL_INS_WITHOUT_PERSONA
            if self.persona_id:
                return QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITH_PERSONA

            return QUERY_GENERATION_PROMPT_WITHOUT_ADDITIONAL_INS_WITHOUT_PERSONA

    def get_prompt_input_variable_dict(self):
        try:
            add_instructions = self.document_retrieval_engine.get_raw_data(
                ADDITIONAL_PROMPT_INSTRUCTIONS_FILE, data_type="text"
            )
        except:
            add_instructions = ""
        try:
            prompt_examples_file = (
                MULTITABLE_PROMPT_EXAMPLES_WITH_PERSONA_FILE
                if self.persona_id
                else MULTITABLE_PROMPT_EXAMPLES_WITHOUT_PERSONA_FILE
            )
            examples = self.document_retrieval_engine.get_raw_data(
                prompt_examples_file, data_type="text"
            )
        except:
            examples = "no examples given"

        return dict(
            schema_definitions=self.document_retrieval_engine.get_raw_data(
                SCHEMA_DEFINITIONS_FILE, data_type="text"
            ),
            events_schema_definitions=self.document_retrieval_engine.get_raw_data(
                EVENTS_SCHEMA_DEFINITIONS_FILE, data_type="text"
            ),
            abstraction_instances_schema_definitions=self.document_retrieval_engine.get_raw_data(
                ABSTRACTION_INSTANCES_SCHEMA_DEFINITIONS_FILE, data_type="text"
            ),
            worktime_metrics_schema_definitions=self.document_retrieval_engine.get_raw_data(
                WORKTIME_METRICS_SCHEMA_DEFINITIONS_FILE, data_type="text"
            ),
            abstraction_instances_schema=self.document_retrieval_engine.get_raw_data(
                ABSTRACTION_INSTANCES_SCHEMA_FILE, data_type="text"
            ),
            worktime_metrics_schema=self.document_retrieval_engine.get_raw_data(
                WORKTIME_METRICS_SCHEMA_FILE, data_type="text"
            ),
            data_table_dictionary=self.document_retrieval_engine.get_raw_data(
                METADATA_FILE, data_type="text"
            ),
            start_date=self.start_date if self.start_date else QUERY_START_DATE,
            end_date=self.end_date if self.end_date else QUERY_END_DATE,
            examples=examples,
            persona_id=self.persona_id,
            additional_instructions=add_instructions,
            data_table_name=EVENTS_DATA_TABLE_NAME,
        )

    def get_input_variable_of_customized_prompt(self, prompt_file):
        regex = "\\{(.*?)\\}"
        matches = re.findall(regex, prompt_file)
        input_variables = []
        for string in matches:
            if string.find(" ") == -1:
                input_variables.append(string)
        return input_variables

    def get_customized_qa_prompt(self):
        prompt_file = open(
            PROMPT_FILE,
            "r",
        )
        customized_prompt = prompt_file.read()
        input_variables_dict = self.get_prompt_input_variable_dict()
        input_variable_in_customized_prompt = (
            self.get_input_variable_of_customized_prompt(customized_prompt)
        )
        CUSTOMIZED_PROMPT = PromptTemplate(
            template=customized_prompt,
            input_variables=input_variable_in_customized_prompt,
        )

        input_variable_value_dict = {}

        for input_variable in input_variable_in_customized_prompt:
            if input_variable in input_variables_dict:
                input_variable_value_dict.update(
                    {input_variable: input_variables_dict[input_variable]}
                )

        final_prompt = CUSTOMIZED_PROMPT.partial(**input_variable_value_dict)
        return final_prompt

    def get_qa_prompt(self) -> PromptTemplate:
        if args.prompt_file_name:
            return self.get_customized_qa_prompt()
        try:
            additional_instructions = self.document_retrieval_engine.get_raw_data(
                ADDITIONAL_PROMPT_INSTRUCTIONS_FILE, data_type="text"
            )
        except:
            additional_instructions = ""

        self.is_additional_instructions_given = True
        if additional_instructions == "" or additional_instructions.isspace():
            self.is_additional_instructions_given = False

        partial_prompt = self._partial_prompt()
        prompt_input_variables = self._prompt_input_variables()

        # Add persona_id, additional_instructions info to the prompt input variables if it exists
        if self.persona_id:
            prompt_input_variables["persona_id"] = self.persona_id

        if self.is_additional_instructions_given:
            prompt_input_variables["additional_instructions"] = additional_instructions

        # Add the prompt input variables to the partial prompt
        prompt = partial_prompt.partial(**prompt_input_variables)

        return prompt

    def get_table_selection_prompt(self) -> PromptTemplate:
        partial_prompt = self._partial_prompt(is_table_selection_prompt=True)
        prompt_input_variables = self._prompt_input_variables(
            is_table_selection_prompt=True
        )
        prompt = partial_prompt.partial(**prompt_input_variables)

        return prompt
