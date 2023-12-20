This project involves working with a LangChain based LLM model for Question Answering to understand and work with the underlying data.

#### Setup

1. Run `pip install -r requirements.txt` to make sure all the required libraries are up.

#### How to run

Navigate to the askskan folder and set path

```
cd askskan
export PYTHONPATH=`pwd`
```

This can also be set in the VSCode explicitly, make sure the path should have askskan folder in it.

Make sure the current working directory is in the PATH. E.g. add the following to your .zshrc file

```
export PATH=.:$PATH
```

make the askskan exectuble

```
chmod +x askskan
```

Now you can run the code with

```
$ askskan
```

#### Inputs to the code

1. The code expects `user_id` and `session_id` as the arguments to run the code for generating different sessions of the chat.

- If the `user_id` is missing then the code assumes that it is a guest user and assigns `user_id=0`.
- If the `session_id` is missing then the code creates a new unique session_id for each run of the code.

#### Arguments to run the code

1. Run `python3 jobs/askskan_qa_job.py -h` or `python3 jobs/askskan_qa_job.py --help` for an exhaustive list of arguments supported by the code.
2. Following is the list of commands for the desired behaviour.

| Type                                           | Argument        | Example Command         | Notes                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------- | --------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gradio UI interaction                          | None            | `askskan`               | Can use without any arguments. It will open the Web UI.                                                                                                                                                                                                                               |
| Input session id                               | `-s`            | `askskan -s SESSION_ID` | The session id is an integer type. If missing then a unique random id would be generated.                                                                                                                                                                                             |
| Input user id                                  | `-u`            | `askskan -u USER_ID`    | The user id is an integer type. If missing then `user_id=0` which is a guest user.                                                                                                                                                                                                    |
| Support table output                           | `-table`        | `askskan -u USER_ID`    | output the result in a tabular form.                                                                                                                                                                                                                                                  |
| Input question                                 | `-q`            | `askskan -q "QUESTION"` | Takes in an user question. This option will just return the result without the interactive chatbot functionality on the terminal. **_Not applicable for Web UI._**                                                                                                                    |
| Interactive chatbot on CLI                     | `-bot`          | `askskan -bot`          | It will stop at `You: ` where you will have to enter your question to obtain the required output on the terminal. **_Not applicable for Web UI._**                                                                                                                                    |
| Want only result from SQL query                | `-short`        | `askskan -short`        | Works with both CLI and Web UI. **_By default it will go to Web UI, to use on CLI use the `-bot` or `-q` flag._**                                                                                                                                                                     |
| Want SQL query for a specific persona id       | `-persona`      | `askskan -persona`      | Works with both CLI and Web UI. **_By default it will go to Web UI, to use on CLI use the `-bot` or `-q` flag._**                                                                                                                                                                     |
| Want SQL query with a specific start date      | `-start_date`   | `askskan -start_date`   | Works with both CLI and Web UI. **_By default it will go to Web UI, to use on CLI use the `-bot` or `-q` flag._**                                                                                                                                                                     |
| Want SQL query with a specific end date        | `-end_date`     | `askskan -end_date`     | Works with both CLI and Web UI. **_By default it will go to Web UI, to use on CLI use the `-bot` or `-q` flag._**                                                                                                                                                                     |
| Want result in friendly tone                   | `-full` or None | `askskan -full`         | Works with both CLI and Web UI. By default it will give the answer i a friendly tone. **_By default it will go to Web UI, to use on CLI use the `-bot` or `-q` flag._**                                                                                                               |
| Want the SQL query                             | `-sql`          | `askskan -sql`          | Gives the SQL query as the output. By default it will just return the SQL query, if result is also needed then also use `-short` or `-full` flag.It will return a dictionary of SQL and the result. **_By default it will go to Web UI, to use on CLI use the `-bot` or `-q` flag._** |
| Use personal API token                         | `-no_azure`     | `askskan -no_azure`     | Uses personal API tokens instead of the global Azure tokens.                                                                                                                                                                                                                          |
| Use personal API token                         | `-gpt_35`       | `askskan -gpt_35`       | Uses API token for GPT-3.5 in Azure (by default used GPT-4 token).                                                                                                                                                                                                                    |
| Clean sessions and vectorstore files           | `-clean`        | `askskan -clean`        | Clean sessions and vectorstore files in the data (default: False)                                                                                                                                                                                                                     |
| Print the prompt and chat history to the model | `-MV`           | `askskan -MV`           | enables verbose for langchain model                                                                                                                                                                                                                                                   |
| Enable Auth on GUI                             | `-A`            | `askskan -A`            | Authenticate web server using USERNAME and PASSWORD in env (default: False)                                                                                                                                                                                                           |
| Stream logs to output                          | `-SL`           | `askskan -SL`           | Enable logs to be streamed on output (default: False)                                                                                                                                                                                                                                 |

#### Alternate way to run the code

The values for all the above arguments can also be defined in the `config.yml` file under the `askskan/jobs` folder. In that case no need to use the corresponding arguments on the command line. Though other instructions remain the same.

#### Gradio port already in use error

In case the port already in use error comes up while running the gradio UI, run the following commands

```
sudo lsof -i :PID
sudo kill -9 PID
```

PID is the process ID running the gradio UI.

#### Files Naming related to a Data Table
For a Table, 
Schema, Defintions, examples, etc files must be named as follows.
```
#schema name = schema.csv
#schema definition name = definitions.txt
#examples with persona file name = examples_with_persona.txt
#examples without persona file name = examples_without_persona.txt
#examples without persona file name = examples_without_persona.txt
#prompt addtional instructions file name = additional_instructions.txt
```

