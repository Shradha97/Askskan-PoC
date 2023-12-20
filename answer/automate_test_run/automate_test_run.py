import sys
import pandas as pd
sys.path.append(".")
import argparse
from subprocess import run
import time
import subprocess


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
        '-f',nargs='?',help='starting index', type=int,default=1
        )
    parser.add_argument(
        '-l',nargs='?' ,help='ending index',type=int, default=10000
        )
    parser.add_argument(
        '-i',nargs='?' ,help='path of input question csv',type=str, default='/Users/mohd.a/Desktop/repo/Prototypes/test.csv'
        )
    parser.add_argument(
        '-o',nargs='?' ,help='path of output question csv',type=str, default='not_provided'
        )
    parser.add_argument(
        '-path',nargs='?',help='directory path' ,type=str,default='/Users/mohd.a/Desktop/repo/AskSkan/Prototypes/askskan'
        )
    parser.add_argument(
        '-run',nargs='?',help='command to run the file seprated by _' ,type=str, default='askskan_-sql_-q'
        )
    parser.add_argument(
        '-timeout',nargs='?',help='maximum time for getting the responses' ,type=int, default=30
        )
    parser.add_argument(
        '-col',nargs='?',help='result column name' ,type=str, default='test_1'
        )
    parser.add_argument(
        '-delay',nargs='?',help='time delay between two questions' ,type=float, default=1
        )
    args = parser.parse_args()
    return [int(args.f),int(args.l),str(args.i),str(args.o),str(args.path),str(args.run),int(args.timeout),str(args.col),float(args.delay)]

def filter_result(result):
    filtered_result=result.replace('\\n',' ')
    filtered_result=filtered_result.replace('\\r',' ')
    return str(filtered_result)

if __name__=="__main__":
    
    [starting_index,ending_index,file_path_of_input_question_csv,file_path_of_export_question_csv,directory_path,run_command,timeout,result_column_name,delay_time]=get_args()

    question_csv=pd.read_csv(file_path_of_input_question_csv)
    export_question_csv=question_csv.copy()
    columns=export_question_csv.columns
    answer_column=['not_evaluated' for ele in range(0,export_question_csv.shape[0])]    
    
    if result_column_name in export_question_csv:
        for index in range(0,export_question_csv.shape[0]):
            answer_column[index]=export_question_csv.loc[index,result_column_name]
    
    for index in range(0,export_question_csv.shape[0]):
        id=export_question_csv['#'][index]
        #questions that are not evaluated
        if id > ending_index or id <starting_index or export_question_csv['deprecated'][index]=='yes':
            continue
        start=time.time()
        print(id)
        #question need to be evaluated
        question=question_csv['Question'][index] 
        print(question) 
        result=str(call_function(directory_path,question,run_command.replace('_',' '),timeout))
        
        answer_column[index]=filter_result(result[1:])
        print(filter_result(result[1:]))
        print(round(time.time()-start,2))

        time.sleep(delay_time)
    

    export_question_csv[result_column_name]=answer_column

    
        
    if file_path_of_export_question_csv!='not_provided':
        export_question_csv.to_csv(file_path_of_export_question_csv,index=False,header=True)
    else:
        export_question_csv.to_csv(file_path_of_input_question_csv,index=False,header=True)
            

            


#export PYTHONPATH=`pwd`
#export PATH=.:$PATH
# run/usr/local/bin/python3 /Users/mohd.a/Desktop/repo/Prototypes/answer/test/get_sql_queries.py 

        
