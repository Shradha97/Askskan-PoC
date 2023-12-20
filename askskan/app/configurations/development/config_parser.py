import argparse
import yaml
import random
import sys


def get_sys_args():
    arg_names = {}
    for action, option_strings in parser._option_string_actions.items():
        if option_strings.option_strings[1] not in arg_names:
            arg_names[option_strings.option_strings[1]] = option_strings.option_strings[
                0
            ]
    return arg_names


def override_args(arg_names, args, config_data):
    # Arguments given through the command line will override the config file which overrides the default arguments
    for key, value in vars(args).items():
        # override default args by config file
        if key not in config_data:
            config_data[key] = value
        # override config file by command line args
        if "--" + key in sys.argv[1:] or arg_names["--" + key] in sys.argv[1:]:
            config_data[key] = value
    return config_data


parser = argparse.ArgumentParser(
    description="Exhaustive list of available arguments",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

path_arg = parser.add_argument_group("file_paths")
path_arg.add_argument(
    "-conf",
    "--config_file",
    required=False,
    type=str,
    default="jobs/config.yml",
    help="Path to the config yaml file",
)
path_arg.add_argument(
    "-log",
    "--log_file",
    required=False,
    type=str,
    default="logs/logs.log",
    help="Path to the log file",
)

inp_arg = parser.add_argument_group("inputs")
inp_arg.add_argument(
    "-s",
    "--session_id",
    required=False,
    type=int,
    default=random.randint(1, sys.maxsize),
    help="Session id of the chat",
)
inp_arg.add_argument(
    "-u",
    "--user_id",
    required=False,
    type=int,
    default=0,
    help="=User id if not a guest, assign 0 if a guest",
)
inp_arg.add_argument(
    "-q",
    "--question",
    required=False,
    type=str,
    default="",
    help="Question to ask the model, this will automatically lead to cli mode",
)
inp_arg.add_argument(
    "-prompt",
    "--prompt_file_name",
    required=False,
    type=str,
    default=None,
    help="file name of input prompt",
)


inp_arg.add_argument(
    "-qnum",
    "--question_number",
    required=False,
    type=str,
    default="",
    help="Question number to ask the model",
)


inp_arg.add_argument(
    "-persona",
    "--persona_id",
    required=False,
    type=str,
    default=None,
    help="Persona id to use for the chat",
)

inp_arg.add_argument(
    "-start_date",
    "--start_date",
    required=False,
    type=str,
    default="2023-04-01",
    help="Start date of the SQL query",
)

inp_arg.add_argument(
    "-end_date",
    "--end_date",
    required=False,
    type=str,
    default="2023-04-30",
    help="End date of the SQL query",
)

out_arg = parser.add_argument_group("output_format")
out_arg.add_argument(
    "-bot",
    "--bot_format",
    required=False,
    action="store_true",
    default=False,
    help="Interact like a chatbot? This will automatically lead to cli mode",
)
out_arg.add_argument(
    "-sql",
    "--sql",
    required=False,
    action="store_true",
    default=False,
    help="output the generated sql query?",
)
out_arg.add_argument(
    "-selected_tables",
    "--selected_tables",
    required=False,
    action="store_true",
    default=False,
    help="See the tables that have been selected in multitable format?",
)
out_arg.add_argument(
    "-short",
    "--query_result",
    required=False,
    action="store_true",
    default=False,
    help="output only the result of sql query?",
)
out_arg.add_argument(
    "-full",
    "--full_result",
    required=False,
    action="store_true",
    default=False,
    help="output only the result in a friendly tone?",
)
out_arg.add_argument(
    "-table",
    "--tabular_result",
    required=False,
    action="store_true",
    default=False,
    help="output the result in a tabular form?",
)

out_arg.add_argument(
    "-cot",
    "--use_cot",
    required=False,
    action="store_true",
    default=False,
    help="Use the COT prompt for the instructions?",
)

out_arg.add_argument(
    "-v",
    "--verbose",
    required=False,
    action="store_true",
    default=False,
    help="output verbose information",
)

out_arg.add_argument(
    "-MV",
    "--model_verbose",
    required=False,
    action="store_true",
    default=False,
    help="output verbose information from the langchain model",
)

out_arg.add_argument(
    "-A",
    "--auth",
    required=False,
    action="store_true",
    default=False,
    help="Authenticate web server using USERNAME and PASSWORD in env",
)

out_arg.add_argument(
    "-SL",
    "--streamlog",
    required=False,
    action="store_true",
    default=False,
    help="Enable logs to be streamed on output",
)

out_arg.add_argument(
    "-RP",
    "--rootpath",
    required=False,
    type=str,
    default="",
    help="Set root path for web server",
)


token_arg = parser.add_argument_group("api_token")
token_arg.add_argument(
    "-no_azure",
    "--personal_token",
    required=False,
    action="store_true",
    default=False,
    help="Use your personal API token?",
)
token_arg.add_argument(
    "-azure_gpt_35",
    "--gpt_35_azure",
    required=False,
    action="store_true",
    default=False,
    help="Use GPT-3.5 Azure token?",
)

clean_arg = parser.add_argument_group("cleaning")
clean_arg.add_argument(
    "-clean",
    "--clean",
    required=False,
    action="store_true",
    default=False,
    help="Clean the sessions and vectorstore before training?",
)

hyperparam_arg = parser.add_argument_group("hyperparams")
hyperparam_arg.add_argument(
    "-temp",
    "--temperature",
    required=False,
    type=float,
    default=0,
    help="Temperature for the LLM",
)

prompt_type_arg = parser.add_argument_group("prompt type")
prompt_type_arg.add_argument(
    "-no_multitable",
    "--no_multitable",
    required=False,
    action="store_true",
    default=False,
    help="Use the prompt template that is not for auto selection of multiple tables",
)

args, unparsed = parser.parse_known_args()
arg_names = get_sys_args()

with open("config.yml", "r") as file:
    config_data = yaml.safe_load(file)

config_data = override_args(arg_names, args, config_data)
args = argparse.Namespace(**config_data)

# TO DO: Add to logs
# print("conf:", args)
