import sys 
sys.path.append(".")
import pandas as pd
import argparse
import time
from sklearn.metrics.pairwise import cosine_similarity
from databricks import sql
import os
import json
import re
import itertools
import numpy as np
import openai
import random

os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

DBWS_HOST = os.getenv("dbws_host_domain")
DBWS_HTTP_PATH = os.getenv("dbws_host_path")
DBWS_PAT = os.getenv("dbws_pat")

def execute_sql_query(query):
    result_rows = []

    with sql.connect(server_hostname = DBWS_HOST,
                    http_path        = DBWS_HTTP_PATH,
                    access_token     = DBWS_PAT) as conn:

        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

            for row in result:
                result_rows.append(row)

    if len(result_rows) == 1:
        return result_rows[0]
    
    return result_rows



class LLM():
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'
        self.deployment_name=os.getenv("AZURE_OPENAI_DNAME")
        
    def get_response(self,prompt):
        messages = [{"role": "assistant", "content": prompt}]
        response = openai.ChatCompletion.create(

        engine=self.deployment_name,
        messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]



def get_prompt_template(Schema,Defination,SAMPLE_QUESTION_SET,SQL_QUERY):
    prompt_template = f"""
    CONTEXT: Their is a SQL database named 'UNUM_ASKSKAN.EVENTS_DELTA_TB' which has this Schema {Schema} and definition {Defination}.\
    
    YOUR TASK: You are a smart assistant designed to make  (Question ,SQL Query, Answer) tuple to test reliability of another LLM model.\
       Given Schema and Definition , you must come up with (Question ,SQL Query, Answer) that can be used to test another LLM model.\
       Come up with 5 HARD (Question ,SQL Query, Answer) tuple that involes nested SQL queries.\
       Take a look at the SAMPLE QUESTIONS {SAMPLE_QUESTION_SET} and their Respected {SQL_QUERY}.
       GENERATE NEW question answer pair DIFFERENT FROM {SAMPLE_QUESTION_SET}
       YOU CAN USE Combination of 4-5 columns,Nested Queries etc For Framing HARD Question \
       When coming up with the (Question ,SQL Query, Answer) tuple You must respond in the following format.\
       [
        {{
           "Question":"$Your Question is here"
           "SQL Query":"$Your SQL Query is here "
           "Answer":"$Your Answer is here"
       }},
       {{
           "Question":"$Your Question is here"
           "SQL Query":"$Your SQL Query is here "
           "Answer":"$Your Answer is here"
       }},

       ]
       You must return the output in JSON list of dictionaries as follows\
       SAMPLE EXAMPLE:
       {{
                "Question":"which is the most used application ?"
                "SQL Query":"SELECT app_name, SUM(active_time) as sum_active_time FROM DATASET WHERE  event_date >= '2023-04-01' AND event_date <= '2023-04-30'  GROUP BY app_name ORDER BY sum_active_time DESC LIMIT 1"
                "Answer":"Most Used application is #variable"
       }}
       
       IMPORTANT INSTRUCTIONS that must be followed while Framing the (Question ,SQL Query, Answer):\
        0. An EVENT cannot be classifed as Nonprocess or process event. Its just an event
        1. In SQL Query Explictly use event_date>='2023-04-01' and  event_date<='2023-04-30' in WHERE clause\
        2. Don't Use the DATASET word in the Question.\
        3. Non Process or Process word/term is ONLY used with application like process applications and non process applications(SEE EXAMPLE 1)\
        4. DON'T use [NESTED_AGGREGATE_FUNCTION] as it will give ERROR.Please use the inner aggregate function in a sub-query\
        5. Don't Assume any column name example on your own,  use example from Example column in Schema as column example\
        6. Frame Questions in such a way that SQL OUTPUT is at max 10 rows (USE LIMIT 10, ASC LIMIT 1 , DESC LIMIT 1 FUNCTIONS)\ 
        7. WHILE FRAMING question use 'Sample Value' column in Schema to take Example for specific 'Column Name'\

       


     """
    

    return prompt_template
def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-sch',nargs='?',help='schema csv path', type=str,required=True
            )
        parser.add_argument(
            
            '-defi',nargs='?' ,help='definition txt path',type=str, required=True
            )
        parser.add_argument(
            
            '-eval',nargs='?' ,help='evaluation_question_set csv path',type=str, required=True
            )

       
        
        
        args = parser.parse_args()
        return [str(args.sch),str(args.defi),str(args.eval)]    


if __name__=="__main__":
    
    #llm model
    [schema_file_path,Definition_file_path,Evaluation_question_set_path]=get_args()
    Schema=pd.read_csv(schema_file_path)
    # print(Schema)
    Evaluation_question_set=pd.read_csv(Evaluation_question_set_path)
    Definition=open(Definition_file_path, "r")
    Definition=Definition.read()


    current_question_set=[question for question in Evaluation_question_set['Question']]
    current_SQL_Query_set=[query for query in Evaluation_question_set['SQL Query']]
    
    
    start=time.time()
    prompt_template=get_prompt_template(Schema,Definition,current_question_set,current_SQL_Query_set)
    llm_model=LLM()
    result=llm_model.get_response(prompt_template)
    # print(result)
    result=(json.loads(result))
    
    df=Evaluation_question_set.copy()
    
    sample_values_dict={}
    # for index in range(1,len(Schema)):
    #     if Schema['Type'][index]=='text':
    #         query="SELECT  DISTINCT "+Schema['Column Name'][index]+" FROM unum_askskan.events_delta_tb WHERE event_date>='2023-04-01' and  event_date<='2023-04-30'"
    #         list=json.loads((json.dumps(execute_sql_query(query), indent=2)))
    #         if "['None']" in list:
    #             list.remove("['None']")
    #         if "[None]" in list:
    #             list.remove("[None]")
    #         print(index)
    #         rand_idx = random.randint(0, len(list)-1)
    #         value=str(list[rand_idx]).replace('[','')
    #         value=value.replace(']','')
    #         value=value.replace("'",'')
    #         sample_values_dict.update({Schema['Column Name'][index]+"_example":value})
    # print(sample_values_dict)
    
    # print(df)
    for index in range(0,len(result)):
        question=str(result[index]['Question']).replace('in the dataset','')
        query=str(result[index]['SQL Query'])
        # for column_name in Schema['Column Name']:
        #     value=column_name+'_example'
        #     if value in question:
        #         question=str(question).replace(value,sample_values_dict[value])
        #     if value in query:
        #         query=str(query).replace(value,sample_values_dict[value])
            
            
        print(query)
        evaluated_answer=''
        try:
            evaluated_answer=str(json.loads(json.dumps(execute_sql_query(query),indent=2)))
           
            
        except:
            # print(index)
            # print("error")
            continue
            
        answer=str(result[index]['Answer']).replace('#variable',evaluated_answer)
        row={'Question':question,'SQL Query':query,'Answer':answer,'Final_answer':evaluated_answer}
        df.loc[len(df)]=row
    df=df.reset_index(drop=True)
    df.to_csv(Evaluation_question_set_path,index=False)    
    # print(time.time()-start)
    
    
    
    
    
     
    