import pandas as pd
import numpy as np
import sys
sys.path.append(".")
from preprocess import preprocess
from queries import queries
import args
from io import StringIO
import csv
import os
import time
from collections import Counter

[starting_index,ending_index,filepath_of_ques_csv,filepath_output_csv,filepath_of_dataset_csv,column_name]=args.main(['-f', sys.argv[1], '-l', sys.argv[2],'-i',sys.argv[3],'-o',sys.argv[4],'-d','-c'])
starting_index=int(starting_index)
ending_index=int(ending_index)
filepath_of_ques_csv=str(filepath_of_ques_csv)
filepath_of_dataset_csv=str(filepath_of_dataset_csv)

ques_csv= pd.read_csv(filepath_of_ques_csv,index_col=False)
dataset=pd.read_csv(filepath_of_dataset_csv,index_col=False,on_bad_lines='skip')
process=preprocess()
df=process.preprocess_the_data(dataset)
query=queries()

no_of_days=query.get_total_days(df)
month_name=query.get_month(df)
if column_name!='not_provided':
    month_name=column_name

export_csv=ques_csv.copy()
answer_column=['Not Evaluated' for i in range(0,export_csv.shape[0])]
if month_name in export_csv.columns:
    for index in range(0,export_csv.shape[0]):
        answer_column[index]=export_csv.loc[index,month_name]

for index in range(0,export_csv.shape[0]):
    
    id=export_csv['#'][index]
    if id<starting_index or id > ending_index or ques_csv['deprecated'][index]=='yes':
        continue    
    ans=query.get_answer(id,df)
    answer_column[index]=ans

    

if month_name in export_csv.columns:
    for index in range(0,export_csv.shape[0]):
        export_csv.at[index,month_name]=answer_column[index]
else:
    export_csv[month_name]=answer_column

if filepath_output_csv!='not_provided':
    export_csv.to_csv(filepath_output_csv,index=False,header=True)
else:
    export_csv.to_csv(filepath_of_ques_csv,index=False,header=True)




