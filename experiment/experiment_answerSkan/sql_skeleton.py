import sys 
sys.path.append(".")
from llm import LLM
import pandas as pd
import numpy as np
import argparse
from sql_cluster import sql_clustering
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
   
    parser.add_argument(
        '-col',nargs='?',help='sql query column name', type=str,required=True
        )
    
    parser.add_argument(
        '-i',nargs='?' ,help='path of input question csv',type=str, default='answer/in/questions.csv'
        )
    parser.add_argument(
        '-o',nargs='?' ,help='path of output question csv',type=str, default='not_provided'
        )
    parser.add_argument(
        '-res',nargs='?' ,help='name of skeleton column',type=str, default='skeleton'
        )
    
    args = parser.parse_args()
    return [str(args.col),str(args.i),str(args.o),str(args.res)]
def get_prompt(sql_query_list,skeleton_column):
    prompt = f"""
        You are a smart Programmer.\
        your task is to append each query in {sql_query_list} to {skeleton_column} list.   
        
        """   
    return prompt
def get_Generalized_query(query):
    columns=['event_id','sequence_id','event_time','persona_id','persona_name','participant_name','app_name','agent_type','clipboard','title','event_date',
'navigation_key_count','number_key_count','mouse_count','mouse_wheel','alpha_key_count','active_time','idle_time','wait_time','processing_time','tat_event','session_switch',
'app_switch','case_switch','activity_id','activity_abstraction_level_id','activity_abstraction_level_name','activity_discovered_name','activity_instance_id',
'activity_instance_abstraction_level_alias_name','activity_instance_original_end_time','activity_instance_end_time','activity_instance_event_count',
'activity_instance_start_time','case_id_name','case_id_value','url','is_pruned','source','event_control_type']
    modified_query=query
    for col in columns:
        modified_query=modified_query.replace(col,'column')
    
    query_split_in_list=modified_query.split(' ')
    alias_column=[]
    for index in range(0,len(query_split_in_list)):
        if query_split_in_list[index]=='AS' or query_split_in_list[index] =='as':
        
            alias_name=''

            for char in query_split_in_list[index+1]:
                if (char>='a' and char <='z') or (char>='A' and char <='Z') or char=='_':
                    alias_name+=char
                else:
                    break

            
            alias_column.append(alias_name)
    
    for alias_name in alias_column:
        modified_query=modified_query.replace(alias_name,'alias_column_name')
    
    modified_query=modified_query.upper()
    return modified_query
if __name__=="__main__":
    [query_column_name,file_path_of_input_question_csv,file_path_of_export_question_csv,skeleton_column_name]=get_args()

    question_csv=pd.read_csv(file_path_of_input_question_csv)
    export_csv=question_csv.copy()
    skeleton_column=[np.nan for ele in range(0,export_csv.shape[0])]
    if skeleton_column_name in export_csv:
        for index in range(0,export_csv.shape[0]):
            skeleton_column[index]=export_csv.loc[index,skeleton_column_name]
    
    
    sql_query_list=[]
    index_sql_query_mapping={}
    start_index=0
    for index in range(0,len(export_csv)):
        id=export_csv['#'][index]
        if export_csv['deprecated'][index]=='yes':
            continue
        query_1=export_csv[query_column_name][index]
        query_1= query_1.replace("unum_askskan.events_delta_tb", "Dataset")
        modified_query=get_Generalized_query(query_1)
        index_sql_query_mapping.update({start_index:modified_query})
        sql_query_list.append(modified_query)
        start_index+=1
    x_axis=[]
    y_axis=[]

    # for index in range(80,100,2):
    #     threshold=index/100
    #     cluster=sql_clustering()
    #     cluster_ids=cluster.get_clusters(sql_query_list,threshold)
    #     no_of_cluster=len(Counter(cluster_ids))
    #     silhouette_score=cluster.get_silhouette_score()
    #     x_axis.append(no_of_cluster)
    #     y_axis.append(silhouette_score)
    for no_of_cluster in range(4,30):
        cluster=sql_clustering()
        cluster_ids=cluster.get_clusters_by_clustering(sql_query_list,no_of_cluster)
        silhouette_score=cluster.get_silhouette_score()
        x_axis.append(no_of_cluster)
        y_axis.append(silhouette_score)

    print(x_axis)
    print(y_axis)
    plt.plot(x_axis, y_axis)
    plt.show()   



        #printing clusters 

        # cluster_groups={}
        # for index in range(0,len(cluster_ids)):
        #     sql_query=index_sql_query_mapping[index]
        #     cluster_id=cluster_ids[index]
        #     current=[]
        #     if cluster_id in cluster_groups:
        #         current=cluster_groups[cluster_id]
        #     current.append(sql_query)
        #     cluster_groups.update({cluster_id:current})
        # print(len(cluster_groups))
        # for id,clusters in cluster_groups.items():
        #     print("cluster #",end=" ")
        #     print(id,len(clusters))

        # for clus in clusters:
        #     print(clus)
        # print()
        # print()

