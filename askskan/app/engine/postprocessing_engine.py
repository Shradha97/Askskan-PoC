import re
import ast
import json
import pandas as pd


from app.configurations.development.config_parser import args
from app.configurations.development.settings import (
    MODEL_OUTPUT_FIELD,
    MODEL_ANSWER_FIELD,
    MODEL_QUERY_FIELD,
    MODEL_COLUMN_FIELD,
    MODEL_CODE_FIELD,
    MODEL_BOT_RESPONSE_FIELD,
    MODEL_DOUBT_FIELD,
    MODEL_REASONING_FIELD,
    FALLBACK_MESSAGE,
)

JSON_RESULT = None  # FIX ME: Remove this global variable


class PostProcessingEngine:
    def _count_pattern_occurrences(self, statement, pattern):
        occurrences = re.findall(pattern, statement)
        return len(occurrences)

    def _replace_terms(self, statement, terms_list, result_table):
        for term in terms_list:
            placeholder = f"#{term}#"
            if placeholder in statement:
                statement = statement.replace(
                    placeholder, str(result_table.loc[0, term])
                )
        return statement

    def _replace_terms_list(self, statement, terms_list, result_table):
        for term in terms_list:
            placeholder = f"#{term}#"
            if placeholder in statement:
                statement = statement.replace(
                    placeholder, str(result_table[term].tolist())
                )
        return statement

    def _replace_multiple_terms(self, statement, terms_list, result_table):
        for index, row in result_table.iterrows():
            for term in terms_list:
                statement = statement.replace(f"#{term}{index+1}#", str(row[term]))
        return statement

    def _get_json(
        self,
        result,
        model_output_field=MODEL_OUTPUT_FIELD,
    ) -> tuple:
        global JSON_RESULT
        result = result.strip(model_output_field)
        # check if the result is a valid JSON string

        try:
            JSON_RESULT = json.loads(result, strict=False)
        except Exception:
            # Remove invalid escape sequences from the JSON string
            json_string = result.encode("utf-8").decode("unicode_escape")

            try:
                # Convert the modified JSON string to a JSON object
                JSON_RESULT = json.loads(json_string, strict=False)
            except json.JSONDecodeError:
                return result

        return None

    def evaluate_output_from_string(
        self,
        result_string,
        model_output_field=MODEL_OUTPUT_FIELD,
    ):
        pattern = r"\{(.+?)\}"

        # Use regular expression to extract the Output section
        output_section_match = re.search(
            model_output_field + pattern, result_string, re.DOTALL
        )

        if output_section_match:
            output_section = output_section_match.group(0)
            try:
                stripped_output_section = output_section.replace(
                    model_output_field, ""
                ).strip()
                evaluated_string_dict = ast.literal_eval(stripped_output_section)
                return evaluated_string_dict
            except:
                return FALLBACK_MESSAGE
        else:
            return FALLBACK_MESSAGE

    def extract_extra_fields(
        self,
        model_column_field=MODEL_COLUMN_FIELD,
        model_bot_response_field=MODEL_BOT_RESPONSE_FIELD,
    ) -> tuple:
        column = JSON_RESULT[model_column_field]
        bot_response = JSON_RESULT[model_bot_response_field]

        return column, bot_response

    def extract_sql_query(
        self,
        result,
        model_query_field=MODEL_QUERY_FIELD,
    ) -> tuple:
        is_query = True
        non_json_result = self._get_json(result)

        if non_json_result:
            return (non_json_result, not is_query)

        # Extract the "Query" field
        query = JSON_RESULT[model_query_field]

        # Print the extracted query
        return (query, is_query)

    def extract_python_code(
        self,
        result,
        model_code_field=MODEL_CODE_FIELD,
    ) -> str:
        non_json_result = self._get_json(result)

        # Extract the code and bot answer fields
        code = JSON_RESULT[model_code_field]

        # Print the extracted code
        # print(code)

        return code

    def get_final_bot_response_from_sql(
        self, query_result, bot_response, column
    ) -> tuple:
        cols = None
        pattern = r"#(.*?)#"

        if isinstance(query_result, list):
            # Convert the list of Row objects to a dictionary of lists
            cols = list(query_result[0].asDict().keys())
            table_data = {key: [row[key] for row in query_result] for key in cols}
            result_data = list(zip(*table_data.values()))
        else:
            cols = list(query_result.asDict().keys())
            table_data = {key: [query_result[key]] for key in cols}
            result_data = (
                query_result[cols[0]]
                if len(column) == 1
                else tuple(query_result[key] for key in column)
            )

        # Create the DataFrame using pandas
        result_table = pd.DataFrame(table_data, columns=cols)
        result_table_md = "\n" + result_table.to_markdown(index=False) + "\n"

        # if the result is a list, only then convert to table
        if isinstance(result_data, list) and args.tabular_result:
            return result_table_md, result_data
        if args.query_result:
            return str(result_data), result_data

        num_occurences = self._count_pattern_occurrences(bot_response, pattern)

        if isinstance(result_data, list):
            if num_occurences == len(column) * len(result_data):
                bot_response = self._replace_multiple_terms(
                    bot_response, column, result_table
                )
            else:
                # when there is a ## for each column
                bot_response = self._replace_terms_list(
                    bot_response, cols, result_table
                )
        elif num_occurences > 1:
            # if there's a single row in the result but multiple columns to be printed separately
            bot_response = self._replace_terms(bot_response, cols, result_table)
        else:
            # if there's a single hashtag in the bot response
            bot_response = re.sub(pattern, str(result_data), bot_response)

        return bot_response, result_data
