# Case 1: Straightforward answers
## Prompt 1

You are a SQL code generator.
Perform the following actions:
- Understand the question delimited by <>.
- Understand the schema delimited by <>.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```
**Question: Who has the longest average processing time?**

Output:
```SQL
SELECT participant_id, AVG(processing_time) AS average_processing_time
FROM table_name
GROUP BY participant_id
ORDER BY average_processing_time DESC
LIMIT 1;
```


# Case 2: Wrong answer due to assumption by the model
## Prompt 1
On using the same prompt 1 from case 3 without providing any schema, the model was creating a schema based on the past knowledge and infering knowledge from the input question and then was generating an answer.

## Prompt 2
You are a SQL code generator.

Perform the following actions:
- If schema and/or question is missing, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.
```
Use the following format:
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```

**Question: Name of the participant that uses the most applications on average?**

Output:
```SQL
SELECT participant_id
FROM TaskData
GROUP BY participant_id
ORDER BY AVG(array_length(applications_used, 1)) DESC
LIMIT 1;
```
* The model is assuming a table name for the schema -> avoid any kind of assumptions regarding the schema.

## Prompt 3:
Perform the following actions:
- If schema and/or question is missing, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Do not assume any schema attributes unless stated explicitly.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.
```
Use the following format:
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```

**Question: Name of the participant that uses the most applications on average?**

Output:
```SQL
SELECT participant_id, AVG(array_length(applications_used, 1)) AS avg_applications_used
FROM your_table
GROUP BY participant_id
ORDER BY avg_applications_used DESC
LIMIT 1;
```
* Such a prompt always asks for a schema even if a chat is continued -> change the prompt to ask the user to use the previous schema/question if any.

## Prompt 4
Perform the following actions:
- If schema and/or question is missing:
    * Ask the user if schema and/or question from the previous context should be used.
    * If there is no previous context, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Do not assume any schema attributed unless stated explicitly.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.

```
Use the following format:
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```

**Question: Name of the participant that uses the most applications on average?**

```SQL
SELECT participant_id, AVG(array_length(applications_used, 1)) AS avg_applications_used
FROM your_table
GROUP BY participant_id
ORDER BY avg_applications_used DESC
LIMIT 1;
```
* The model now asks if it needs to use the schema from the previous context before more forward.


# Case 3: Ambiguous user question
*Ambiguity in question can be of many types:*

*- Type 1: Incorrect answer due to confusion in input term and the term used in the schema for the same functionality.*

## Prompt 1
You are a SQL code generator.

Perform the following actions using the same schema and different question:
- Understand the question and schema each delimited by <>.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```

**Question: Who is the most productive participant based on the number of tasks completed?**

(*In this case the model couldn't infer that the task is considered as a case, hence a followup question had to be asked after evaluating the obtained SQL query.*)

Output:
``` SQL
SELECT participant_id, COUNT(*) AS task_count
FROM table_name
GROUP BY participant_id
ORDER BY task_count DESC
LIMIT 1;
```

* Incorrect Answer generated.
* **Followup prompt:** Tasks are considered as cases. Now look carefully into the schema to decide the appropriate columns to fetch the answer.

Output:
``` SQL
SQL query:
SELECT participant_id
FROM table_name
GROUP BY participant_id
ORDER BY COUNT(DISTINCT case_id) DESC
LIMIT 1;
```

## Prompt 2:
You are a super smart programmer.

Perform the following actions:

- If schema and/or question is missing:
    - Ask the user if schema and/or question from the previous context should be used.
    - If there is no previous context, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Based on the question and the schema, first seek to clarify any ambiguities.
    - Specifically first summarise a list of super short bullets of areas that need clarification.
    - Then pick one clarifying question, and wait for an answer from the user. Once all the questions are clarified, then proceed to the next steps.
- Do not assume any schema attributes unless stated explicitly.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```
*Since the input question and schema are missing in the prompt, the model first asks for both.*

**Question (next prompt): Name of the participant that performs the highest variety of tasks?**

*The model next asks for a few clarifying questions and then outputs the following SQL queries.* 

*Previously the model used to get confused between task and case, now the model first clarifies what exactly the user means by the task variety and then proceeds to generate the code accordingly.*

Output:
```SQL
SELECT participant_id
FROM (
    SELECT participant_id, COUNT(DISTINCT case_type) AS num_distinct_case_types
    FROM YourTableName
    GROUP BY participant_id
) AS subquery
ORDER BY num_distinct_case_types DESC
LIMIT 1;
```

# Case 4: Model hallucinates some definitions from the schema
## Prompt 1
Perform the following actions using the same schema and different question:
- If schema and/or question is missing, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```

Question: Name of the participant that uses the most number of long cut keys on average?

Output:
```SQL
SELECT participant_id
FROM TaskData
GROUP BY participant_id
ORDER BY AVG(no_of_keystrokes - no_of_shortcut_keys) DESC
LIMIT 1;
```

* The model hallucinates here, assumes the definition of longcut keys -> can be avoided by:
    - Asking clarifying questions from the user.
    - Getting the reasoning of the model confirmed by the user.


## Prompt 2: (*Asking clarifying questions from the model*)

You are a super smart programmer.

Perform the following actions:

- If schema and/or question is missing:
    - Ask the user if schema and/or question from the previous context should be used.
    - If there is no previous context, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Based on the question and the schema, first seek to clarify any ambiguities.
    - Specifically first summarise a list of super short bullets of areas that need clarification.
    - Then pick one clarifying question, and wait for an answer from the user. Once all the questions are clarified, then proceed to the next steps.
- Do not assume any schema attributes unless stated explicitly.
- Use the schema to generate SQL query answering the question.
- Output computationally most efficient SQL query.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated SQL query>
Schema: <Schema of the database table to be queried for the given question>
SQL query: <valid SQL query>
```

**Question: Name of the participant that uses the most number of long cut keys on average?**

(*Clarifying questions are asked from the end user next*)

Output:
```SQL
SELECT participant_id
FROM (
  SELECT participant_id, AVG(no_of_keystrokes) AS avg_long_cut_keys
  FROM your_table_name
  WHERE no_of_shortcut_keys = 0
  GROUP BY participant_id
) AS subquery
ORDER BY avg_long_cut_keys DESC
LIMIT 1;
```
(*This reasoning **might not be completely correct** as the participants using shortcut keys can still be using langcut keys. Can be resolved if the model confirms its reasoning with the user.*)

## Prompt 3:
Keep asking clarifying questions from the user.
(*currently asked the model to get confirmation of the reasoning from the user. Doesn't seem to be a really good method.*)--FIX IT.

# Prompting without explicitly specifying a language
## Prompt 1:
You are a super smart programmer.

Perform the following actions:

- If schema and/or question is missing:
    - Ask the user if previously used schema and/or question should be used.
    - If there is no previous context, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Based on the question and the schema, first seek to clarify any ambiguities.
    - Specifically first summarise a list of super short bullets of areas that need clarification.
    - Then pick one clarifying question, and wait for an answer from the user. Once all the questions are clarified, then proceed to the next steps.
- Do not assume any schema attributes unless stated explicitly.
- By looking at the schema, properly decide the language in which the code should be generated.
- Use the schema to generate the code answering the question.
- Output computationally most efficient code.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated code>
Schema: <Schema of the database table to be queried for the given question>
Language: <Language in which the code is generated>
Code: <valid code>
```

**Question: Who has the longest average processing time?**

Output:

Language: Python
```Python
import pandas as pd

# Assuming the data is stored in a pandas DataFrame called 'data'
# Calculate the average processing time for each participant
average_processing_time = data.groupby('participant_id')['processing_time'].mean()

# Find the participant with the longest average processing time
participant_with_longest_time = average_processing_time.idxmax()

participant_with_longest_time
```
*When asked to decide the appropriate language based on the schema, the model outputs code in python.*

*Need to modify the prompt for the model to automatically select SQL as the code generating language.*

## Prompt 2:
You are a super smart programmer.

Perform the following actions:

- If schema and/or question is missing:
    - Ask the user if previously used schema and/or question should be used.
    - If there is no previous context, ask a followup question asking for schema and/or question in the input.
- Understand the question and schema each delimited by <>.
- Based on the question and the schema, first seek to clarify any ambiguities.
    - Specifically first summarise a list of super short bullets of areas that need clarification.
    - Then pick one clarifying question, and wait for an answer from the user. Once all the questions are clarified, then proceed to the next steps.
- Do not assume any schema attributes unless stated explicitly.
- By looking at the schema, decide the best language for fetching the appropriate data from the database. 
- Use the schema to generate the code answering the question.
- Output computationally most efficient code.
- Omit any explanations.

Use the following format:
```
Question: <Question to be answered by the generated code>
Schema: <Schema of the database table to be queried for the given question>
Language: <Language in which the code is generated>
Code: <valid code>
```

**Question: Who has the longest average processing time?**

*This prompt asks the user to specify the prefered language for code generation.* -- DO NOT WANT THE MODEL TO ASK THE USER FOR PREFERED LANGUAGE.

## Prompt 3:



