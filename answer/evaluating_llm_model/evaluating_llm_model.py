import sys
import pandas as pd
sys.path.append(".")
import argparse
from subprocess import run
import time
import subprocess
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from answer.CompareQuery.compare_query import compare_query
def embedding_model_1(full_query_list):
    model_1=SentenceTransformer('distilbert-base-nli-mean-tokens')
    return model_1.encode(full_query_list)

def call_function(directory_path,question,run_command,time_out):
    path='cd '+directory_path+' && '+run_command+' "'+question+'"'
    flag=1
    result=''
    while(flag<4):
        try:
            result=run([path],shell=True,capture_output=True,timeout=time_out)
            
            
        except subprocess.TimeoutExpired:
            flag+=1
        flag=100
    
    return result.stdout
    

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',nargs='?' ,help='file path of evaluation question set',type=str,default='/Users/mohd.a/Desktop/repo/Prototypes/answer/evaluating_llm_model/evaluation_question_set.csv'
        )
    parser.add_argument(
        '-path',nargs='?',help='directory path' ,type=str,default='/Users/mohd.a/Desktop/repo/AskSkan/Prototypes/askskan'
        )
    args = parser.parse_args()
    return [str(args.i),str(args.path)]

def filter_result(result):
    filtered_result=result.replace('\\n',' ')
    filtered_result=filtered_result.replace('\\r',' ')
    return str(filtered_result)


if __name__=="__main__":
    
    [file_path_of_input_question_csv,directory_path]=get_args()
    timeout=50
    delay_time=1
    result_column_name='Result'
    evaluation_question_set_csv=pd.read_csv(file_path_of_input_question_csv)
   
    result_column=[0 for ele in range(0,evaluation_question_set_csv.shape[0])]    
    score=0
    for index in range(0,evaluation_question_set_csv.shape[0]):
        start=time.time()
        question=evaluation_question_set_csv['Question'][index]
        correct_sql_query=evaluation_question_set_csv['SQL Query'][index]
        correct_answer=evaluation_question_set_csv['Answer'][index]
        correct_final_answer=evaluation_question_set_csv['Final_answer'][index]

        sql_query=str(call_function(directory_path,question,'askskan -sql -q',timeout))
        sql_query=filter_result(sql_query[1:])
        # print(sql_query)

        answer=str(call_function(directory_path,question,'askskan -q',timeout))
        answer=filter_result(answer[1:])
        # print(answer)
        final_answer=str(call_function(directory_path,question,'askskan -short -q',timeout))
        final_answer=filter_result(final_answer[1:])
        # print(final_answer)

        answer_similarity=0
        final_answer_similarity=0
        answer_similarity=cosine_similarity(embedding_model_1([answer,correct_answer]))[0][1]
        final_answer_similarity=cosine_similarity(embedding_model_1([final_answer,correct_final_answer]))[0][1]
        # print(answer_similarity)
        # print(final_answer_similarity)
        Compare_query=compare_query()
        result,reason=Compare_query.get_result(correct_sql_query,sql_query)
        print(result)
        print(reason)
        # result='Equivalent'
        

        if result=='Equivalent' and answer_similarity >= 0.7 and final_answer_similarity>=0.5 :
            score+=1
            result_column[index]+=1

        print(round(time.time()-start,2))

        time.sleep(delay_time)
    print(score)
    evaluation_question_set_csv[result_column_name]=result_column
    evaluation_question_set_csv.to_csv(file_path_of_input_question_csv,index=False,header=True)
            

            


# #export PYTHONPATH=`pwd`
# #export PATH=.:$PATH
# # run/usr/local/bin/python3 /Users/mohd.a/Desktop/repo/Prototypes/answer/test/get_sql_queries.py 

        
