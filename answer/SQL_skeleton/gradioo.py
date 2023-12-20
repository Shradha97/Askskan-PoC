import gradio as gr
import pandas as pd
from sql_cluster import sql_clustering
import re
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import random
from sentence_transformers import SentenceTransformer
import warnings
import numpy as np
from collections import Counter
from scipy.spatial import distance_matrix
import operator
import nltk
import spacy
from sklearn.decomposition import PCA
# import tensorflow_hub as hub
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import umap
from sklearn.metrics.cluster import rand_score
import argparse
warnings.filterwarnings("ignore", category=DeprecationWarning)


max_output=100
global_barplot_dataframe=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]})
global_scatterplot_dataframe=pd.DataFrame({"X": [0,1,2],"Y": [0,0,0],"label":[0,0,0]})
Response_csv_path=''
Centroid_csv_path=''

maximum_node_depth=-1
#state- 0 for initialize or calculate whole csv, 1 for adding only 1 query
def pca_reduction(feature_matrix):
    scaling=StandardScaler()
 
    # Use fit and transform method
    scaling.fit(feature_matrix)
    Scaled_data=scaling.transform(feature_matrix)
    pca = PCA(n_components=2)
    pca.fit(Scaled_data)
    data_pca = pd.DataFrame(pca.transform(Scaled_data),columns=['X','Y'])
    return data_pca


def embedding_model_1(full_query_list):
    model_1=SentenceTransformer('all-mpnet-base-v2')
    return model_1.encode(full_query_list)

def embedding_model_2(full_query_list):
    model_2 = SentenceTransformer('all-MiniLM-L6-v2')
    return model_2.encode(full_query_list)

def embedding_model_3(full_query_list):
    model_3 = SentenceTransformer('paraphrase-mpnet-base-v2')
    return model_3.encode(full_query_list)
def embedding_model_4(full_query_list):
    model_4=SentenceTransformer('distilbert-base-nli-mean-tokens')
    return model_4.encode(full_query_list)
# def embedding_model_5(full_query_list):
#     module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
#     model_5 = hub.load(module_url)
#     embeddings = model_5(full_query_list)
#     embeddings=embeddings.numpy()
#     return embeddings
    

def get_new_clusters_for_remaining_list(feature_matrix):
    
   
    
    #checking if there is only one cluster
    #label,centroid
    if len(feature_matrix)==1:
        return [0],[(feature_matrix[0],0,1)]
    
    
    if len(feature_matrix)==2:
        if np.sqrt(np.sum(np.square(feature_matrix[0] - feature_matrix[1])))<1:
            return [0,0],[((feature_matrix[0]-feature_matrix[1])/2,0,1),((feature_matrix[0]-feature_matrix[1])/2,0,1)]
        else:
            return [0,1],[(feature_matrix[0],0,1),(feature_matrix[1],0,1)]
    

            



    max_distance=0
    min_distance=1000
    feature_matrix=np.array(feature_matrix)
    centroid=feature_matrix.mean(axis=0)

    for feature_vector in feature_matrix:
        dist=np.sqrt(np.sum(np.square(centroid - feature_vector)))
        max_distance=max(max_distance,dist)
        min_distance=min(min_distance,dist)

    
    #if all datapoints are close enough
    if max_distance-min_distance<1:
        return [0 for index in feature_matrix],[(centroid,min_distance,max_distance) for index in feature_matrix]
    
    
    if len(feature_matrix)<=4:

        cluster=KMeans(n_clusters=2).fit(feature_matrix)
        sil_score1=silhouette_score(feature_matrix,cluster.labels_)
        label_1=cluster.labels_
        centroid_1=cluster.cluster_centers_
        mn_1=[100000 for index in label_1]
        mx_1=[0 for index in label_1]
        for index  in range(0,len(label_1)):
            mn_1[index]=min(mn_1[index],np.sqrt(np.sum(np.square(centroid_1[label_1[index]] - feature_matrix[index]))))
        for index  in range(0,len(label_1)):
            mx_1[index]=max(mx_1[index],np.sqrt(np.sum(np.square(centroid_1[label_1[index]] - feature_matrix[index]))))
        if len(feature_matrix)==3:
            return label_1,[(centroid_1[label_1[index]],mn_1[index],mx_1[index]) for index in range(0,len(label_1))]

        

        cluster=KMeans(n_clusters=3).fit(feature_matrix)
        sil_score2=silhouette_score(feature_matrix,cluster.labels_)
        label_2=cluster.labels_
        centroid_2=cluster.cluster_centers_
        mn_2=[100000 for index in label_2]
        mx_2=[0 for index in label_2]
        for index  in range(0,len(label_2)):
            mn_2[index]=min(mn_2[index],np.sqrt(np.sum(np.square(centroid_2[label_2[index]] - feature_matrix[index]))))
        for index  in range(0,len(label_2)):
            mx_2[index]=max(mx_2[index],np.sqrt(np.sum(np.square(centroid_2[label_2[index]] - feature_matrix[index]))))
        if sil_score1>sil_score2:

            return label_1,[(centroid_1[label_1[index]],mn_1[index],mx_1[index]) for index in range(0,len(label_1))]
        return label_2,[(centroid_2[label_2[index]],mn_2[index],mx_2[index]) for index in range(0,len(label_2))]
    # print("final")   
    cluster_quality=0.8
    max_node_depth=2+len(feature_matrix)/50
    cluster=sql_clustering()
    index_list=[index for index in range(0,len(feature_matrix))]
    cluster.initialize_clustering(index_list,cluster_quality,max_node_depth,feature_matrix)
    node_centroid_max_min_dict,node_children_dict,node_index_dict,leaf_node_index_list=cluster.get_answer()
    indexes_list=[-1 for index in feature_matrix]
    centroid_list=[-1 for index in feature_matrix]
    cluster_id=0
    for leaf_node,index_list in leaf_node_index_list.items():
        centroid_min_max=node_centroid_max_min_dict[leaf_node]
        for index in index_list:
            indexes_list[index]=cluster_id
            centroid_list[index]=(centroid_min_max[0],centroid_min_max[1],centroid_min_max[2])

        cluster_id+=1
    
    return indexes_list,centroid_list


def get_labels_for_new_query_list(new_added_queries_index_list,cluster_id_centroid_min_max_dict,cluster_id_index_list_dict,feature_matrix):
    
   
    new_cluster_centroid_dict=cluster_id_centroid_min_max_dict.copy()
    new_cluster_id_index_dict=cluster_id_index_list_dict.copy()
    new_query_cluster_label=[-1 for query in new_added_queries_index_list]
    for index in range(0,len(new_added_queries_index_list)):
        feature_vector = feature_matrix[new_added_queries_index_list[index]]
        distance_of_point_from_centroids=[]
        for cluster_id,(centroid_corrdinate,min_distance_from_centroid,max_distance_from_centroid) in cluster_id_centroid_min_max_dict.items():
            distance_of_point_from_centroids.append((np.sqrt(np.sum(np.square(centroid_corrdinate - feature_vector))),cluster_id))
        
        distance_of_point_from_centroids.sort()
        # print(distance_of_point_from_centroids)
        if len(distance_of_point_from_centroids)>0 and cluster_id_centroid_min_max_dict[distance_of_point_from_centroids[0][1]][2]+(cluster_id_centroid_min_max_dict[distance_of_point_from_centroids[0][1]][2]-cluster_id_centroid_min_max_dict[distance_of_point_from_centroids[0][1]][1])/4 >= distance_of_point_from_centroids[0][0]:
            # print(distance_of_point_from_centroids[0][1])
            new_cluster_centroid_dict.update({distance_of_point_from_centroids[0][1]:(cluster_id_centroid_min_max_dict[distance_of_point_from_centroids[0][1]][0],min(distance_of_point_from_centroids[0][0],cluster_id_centroid_min_max_dict[distance_of_point_from_centroids[0][1]][1]),max(distance_of_point_from_centroids[0][1],cluster_id_centroid_min_max_dict[distance_of_point_from_centroids[0][1]][2]))})
            current=new_cluster_id_index_dict[distance_of_point_from_centroids[0][1]]
            current.append(new_added_queries_index_list[index])
            new_cluster_id_index_dict.update({distance_of_point_from_centroids[0][1]:current})
            new_query_cluster_label[index]=distance_of_point_from_centroids[0][1]

            
        
        

                
    current_total_cluster=len(new_cluster_id_index_dict)
    if -1 in new_query_cluster_label:
        remaining_feature_matrix=[]
        remaining_index_list=[]

        for index in range(0,len(new_query_cluster_label)):
            if new_query_cluster_label[index]==-1:
                remaining_feature_matrix.append(feature_matrix[new_added_queries_index_list[index]])
                remaining_index_list.append(new_added_queries_index_list[index])
                # feature_vector = feature_matrix[new_added_queries_index_list[index]]
                # new_cluster_centroid_dict.update({current_total_cluster:(feature_vector,0,1)})
                # current=[]
                # current.append(new_added_queries_index_list[index])
                # new_cluster_id_index_dict.update({current_total_cluster:current})
                # current_total_cluster+=1
        indexes_list,centroid_list=get_new_clusters_for_remaining_list(remaining_feature_matrix)
        for index in range(0,len(indexes_list)):
            cluster_id=indexes_list[index]+current_total_cluster
            current_index_list=[]
            if cluster_id in new_cluster_id_index_dict:
                current_index_list=new_cluster_id_index_dict[cluster_id]
            current_index_list.append(remaining_index_list[index])
            new_cluster_id_index_dict.update({cluster_id:current_index_list})
        
            if cluster_id not in new_cluster_centroid_dict:
                new_cluster_centroid_dict.update({cluster_id:centroid_list[index]})


    
                    
    # print("size of new ",len(new_cluster_id_index_dict))
    return new_cluster_id_index_dict,new_cluster_centroid_dict

def update(Question,sql_query,analysis,initialized_node_depth):
    
    if Question!='' or sql_query!='':
        csv=pd.read_csv(Response_csv_path)
        Question=Question.upper() 
        sql_query=sql_query.upper()
        
        row= {'Question':Question ,'modified_Question': modify_question(Question),'Query': sql_query,'is_Question_added_to_cluster':'no','is_Query_added_to_cluster':'no','Query_clusters':'','Question_clusters':'','user_added_query':'yes'}
        csv.loc[len(csv)] =row
        
        csv.to_csv(Response_csv_path,index=False,header=True)

    #if analysis choice is not provided 
    
    if analysis=='':
        curr_box=[]
        curr_box.append(gr.Textbox.update(value=''))
        curr_box.append(gr.Textbox.update(value=''))
        curr_box.append(gr.Textbox.update(value='Select choice from analysis dropbox',visible=True))
        curr_box.append(gr.Textbox.update(visible=False))
        curr_box.append(gr.BarPlot.update(value=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]}),x='cluster_id',y='total_no_of_clusters',visible=False))
        curr_box.append(gr.ScatterPlot.update(value=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]}),x='cluster_id',y='total_no_of_clusters',visible=False,scale=10))
        for index in range(0,max_output):
            curr_box.append(gr.Textbox.update(visible=False))
            curr_box.append(gr.Textbox.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Button.update(visible=False))
            curr_box.append(gr.Button.update(visible=False))
            curr_box.append(gr.Button.update(visible=False))
        
        return curr_box
     
    response_csv=pd.read_csv(Response_csv_path)
    centroid_csv=pd.read_csv(Centroid_csv_path)
    
    #response csv columns
    column_names_of_response_csv=response_csv.columns

    #list of column names of response csv that are not included in details of cluster 
    not_included_columns_in_show_more_details=['is_Question_added_to_cluster','is_Query_added_to_cluster','Query_clusters','Question_clusters','user_added_query','modified_Question']

    #decoding column name of response csv that need to be analysed 
    analysis_column_name=analysis.replace('By ','')
    is_added_cluster_column='is_'+analysis_column_name+'_added_to_cluster'
    cluster_id_index_mapping_column_name=analysis_column_name+'_clusters'
    modified_analysis_column_name='modified_'+analysis_column_name
    
    centroids_column_name=analysis_column_name+'_centroids'

    # print(analysis)
    # print(analysis_column_name)
    # print(is_added_cluster_column)


    #retain old clusters if present
    
    cluster_id_index_list_dict={}
    index_cluster_id_mapping_dict={}
    for index in range(0,response_csv.shape[0]):
        
        if response_csv[is_added_cluster_column][index] =='yes':
            
            
            #cluster_id,cluster_index_from_csv
            cluster_id,cluster_index=int(response_csv[cluster_id_index_mapping_column_name][index]),int(index)
            index_cluster_id_mapping_dict.update({cluster_index:cluster_id})
            #cluster members index
            current_index_list=[]
            if cluster_id in cluster_id_index_list_dict:
                current_index_list=cluster_id_index_list_dict[cluster_id]
            current_index_list.append(cluster_index)
            cluster_id_index_list_dict.update({cluster_id:current_index_list})

    cluster_id_centroid_min_max_dict={}
    
    for index in range(0,centroid_csv.shape[0]):
        
        if '@' in centroid_csv[centroids_column_name][index]:
            cluster_id,cluster_centroid_string,min_distance_from_centroid,max_distance_from_centroid=str(centroid_csv[centroids_column_name][index]).split('@')
            cluster_id=int(cluster_id)
            
            cluster_centroid=[]
            for coordinate in cluster_centroid_string.split('$'):
                coordinate=float(coordinate)
                cluster_centroid.append(coordinate)
            
            if cluster_id not in cluster_id_centroid_min_max_dict:
                cluster_id_centroid_min_max_dict.update({cluster_id:(cluster_centroid,float(min_distance_from_centroid),float(max_distance_from_centroid))})

    #query list containing both evaluated and not evaluated queries
    full_query_list=[]

    #modified query list only for questions for now
    modified_full_query_list=[]
    #new queries list queres that are newly added 
    new_added_queries_list=[]
    #indexes(w.r.t to response csv) of newly added queries 
    new_added_queries_index_list=[]    
    #queries that are already evaluated 
    evaluated_query_list=[]

    
    for index in range(0,response_csv.shape[0]):
        query_1=str(response_csv[analysis_column_name][index])
        if query_1.isspace()==True or query_1=='' or query_1=='nan':
            # print("sfngoruenbgjoerb")
            continue
        query_1=query_1.upper()
        # print(query_1)

        #if new query
        if response_csv[is_added_cluster_column][index]=='no':
            new_added_queries_list.append(query_1)
            new_added_queries_index_list.append(index)
        else:
            evaluated_query_list.append(query_1)

        full_query_list.append(query_1)
        if analysis_column_name=='Question':
            modified_full_query_list.append(str(response_csv[modified_analysis_column_name][index]))
    
    cluster_id_representative_dict={}
    cluster_id_queries_list_dict={}
    cluster_id_show_more_info_dict={}
    #response csv index cluster id mapping
    global global_barplot_dataframe
    global global_scatterplot_dataframe

    
    #reading response csv and centroid csv
    
    #empty response csv

    if len(full_query_list)==0:
        curr_box=[]
        curr_box.append(gr.Textbox.update(value=''))
        curr_box.append(gr.Textbox.update(value=''))
        curr_box.append(gr.Textbox.update(value='Empty Responses',visible=True))
        curr_box.append(gr.Textbox.update(visible=False))
        curr_box.append(gr.BarPlot.update(value=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]}),x='cluster_id',y='total_no_of_clusters',visible=False))
        curr_box.append(gr.ScatterPlot.update(value=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]}),x='cluster_id',y='total_no_of_clusters',visible=False))

        for index in range(0,max_output):
            curr_box.append(gr.Textbox.update(visible=False))
            curr_box.append(gr.Textbox.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Button.update(visible=False))
            curr_box.append(gr.Button.update(visible=False))
            curr_box.append(gr.Button.update(visible=False))
        
        return curr_box
    
    
    
   
    #no new query added
    if len(new_added_queries_index_list)==0:
        summary='No '+analysis_column_name+' are added. Current diffenent type of structure are '+str(len(cluster_id_index_list_dict))+' from '+str(len(full_query_list))
        
        for cluster_id,index_list in cluster_id_index_list_dict.items():

            #current cluster  centroid, min,max
            cluster_centroid_,min_distance_from_centroid_,max_distance_from_centroid_=cluster_id_centroid_min_max_dict[cluster_id]
            rand_idx = random.randrange(len(index_list))

            cluster_id_representative_dict.update({cluster_id:response_csv[analysis_column_name][index_list[rand_idx]]})

            
            current_cluster_members_list=[] 
            current_more_details_list=[]  
            for index in index_list:
                
                #updating show details, show clusters information
                

                current_cluster_members_list.append(response_csv[analysis_column_name][index])
                current_list=[]
                for column_name in column_names_of_response_csv:
                    if column_name not in  not_included_columns_in_show_more_details:
                        current_list.append(str(response_csv[column_name][index]))
                
                current_more_details_list.append(current_list)
            

            cluster_id_queries_list_dict.update({cluster_id:current_cluster_members_list}) 
            cluster_id_show_more_info_dict.update({cluster_id:current_more_details_list})  
        
        
        encoded_full_query_list=full_query_list

        # if analysis_column_name=='Question':
        #     encoded_full_query_list=[modify_question(question) for question in full_query_list]
        
        #feature martrix
        feature_matrix=embedding_model_4(full_query_list)
        if analysis_column_name=='Question':
            feature_matrix=embedding_model_4(modified_full_query_list)

        

        #umap
        clusterable_embedding = umap.UMAP(
            n_neighbors=10,
            min_dist=0.0,
            n_components=2,
            random_state=42,
        ).fit_transform(feature_matrix)
        scatterplot_dataframe=pd.DataFrame({"X": clusterable_embedding[:,0],"Y": clusterable_embedding[:,1],'label':[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()]})
        # reduced_feature_matrix=pca_reduction(feature_matrix)
        # scatterplot_dataframe=pd.DataFrame({"X": [index for index in reduced_feature_matrix['X']],"Y": [index for index in reduced_feature_matrix['Y']],'label':[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()]})
        barplot_dataframe = pd.DataFrame({"cluster_id": [cluster_id for cluster_id in range(0,len(cluster_id_representative_dict)) ],"total_no_of_clusters": [len(cluster_id_queries_list_dict[index]) for index in range(0,len(cluster_id_queries_list_dict))]})

        global_barplot_dataframe=barplot_dataframe
        global_scatterplot_dataframe=scatterplot_dataframe

        

        # plt.scatter(clusterable_embedding[:,0], clusterable_embedding[:,1], c=[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()], cmap='viridis')
        # plt.show()

        curr_box=[]
        #Question textbox
        curr_box.append(gr.Textbox.update(value=''))
        #Query textbox
        curr_box.append(gr.Textbox.update(value=''))
        #summary box
        curr_box.append(gr.Textbox.update(value=summary,visible=True))
        #plotting
        curr_box.append(gr.BarPlot.update(barplot_dataframe,visible=True,x='cluster_id',y='total_no_of_clusters'))
        curr_box.append(gr.ScatterPlot.update(scatterplot_dataframe,visible=True,x='X',y='Y',color='label'))

        for cluster_id in range(0,max_output):
                if cluster_id<len(cluster_id_representative_dict):
                    curr_box.append(gr.Textbox.update(value=cluster_id_representative_dict[cluster_id],visible=True))
                    curr_box.append(gr.Textbox.update(value=len(cluster_id_queries_list_dict[cluster_id]),visible=True))
                    curr_box.append(gr.Dataframe.update(value=[[query_list] for query_list in cluster_id_queries_list_dict[cluster_id]],visible=False))
                    curr_box.append(gr.Dataframe.update(value=pd.DataFrame(cluster_id_show_more_info_dict[cluster_id]),visible=False))
                    
                    curr_box.append(gr.Button.update(visible=True))
                    curr_box.append(gr.Button.update(visible=True))
                    curr_box.append(gr.Button.update(visible=True))
                else:
                    curr_box.append(gr.Textbox.update(visible=False))
                    curr_box.append(gr.Textbox.update(visible=False))
                    curr_box.append(gr.Dataframe.update(visible=False))
                    curr_box.append(gr.Dataframe.update(visible=False))
                    curr_box.append(gr.Button.update(visible=False))
                    curr_box.append(gr.Button.update(visible=False))
                    curr_box.append(gr.Button.update(visible=False))


        return curr_box 

    
    #if no query inside response csv is clustered or evaluated
    if len(full_query_list)==len(new_added_queries_index_list):

        #if not given max node name 
        if initialized_node_depth=='':
            initialized_node_depth=2+int((response_csv.shape[0])/100)
        
        cluster_quality=0.8
        max_node_depth=int(initialized_node_depth)
        cluster=sql_clustering()
        index_list=[index for index in range(0,len(full_query_list))]


        #feature matrix
        feature_matrix=embedding_model_4(full_query_list)

        if analysis_column_name=='Question':
            feature_matrix=embedding_model_4(modified_full_query_list)
        
        

        
        
        # print(len(feature_matrix[0]))

        cluster.initialize_clustering(index_list,cluster_quality,max_node_depth,feature_matrix)

        node_centroid_max_min_dict,node_children_dict,node_index_dict,leaf_nodes_index_list_dict=cluster.get_answer()
        
        #two columns that need to ne updated in response csv
        is_query_added_to_cluster_column=['no' for index in range(0,len(response_csv))]  
        cluster_id_index_mapping_column=['' for index in range(0,len(response_csv))]  
        cluster_id_centroid_mapping_dict={} 
        

        cluster_id=0
        for leaf_node,index_list in leaf_nodes_index_list_dict.items():

            #current cluster  centroid, min,max
            cluster_centroid_,min_distance_from_centroid_,max_distance_from_centroid_=node_centroid_max_min_dict[leaf_node]
            rand_idx = random.randrange(len(index_list))

            cluster_id_representative_dict.update({cluster_id:response_csv[analysis_column_name][index_list[rand_idx]]})

            
            current_cluster_members_list=[] 
            current_more_details_list=[]  
            for index in index_list:
                #updating response csv
                is_query_added_to_cluster_column[index]='yes'
                cluster_id_index_mapping_column[index]=cluster_id

                #response csv cluster id mapping
                index_cluster_id_mapping_dict.update({index:cluster_id})

                #updating centroid csv
                cluster_centroid_string_=''
                for index2 in range(0,len(cluster_centroid_)):
                    if index2==len(cluster_centroid_)-1:
                        cluster_centroid_string_+=str(cluster_centroid_[index2])
                    else:
                        cluster_centroid_string_+=str(cluster_centroid_[index2])+'$'
                
                cluster_id_centroid_mapping_dict.update({cluster_id:str(cluster_centroid_string_)+'@'+str(min_distance_from_centroid_)+'@'+str(max_distance_from_centroid_)})

                #updating show details, show clusters information
                

                current_cluster_members_list.append(response_csv[analysis_column_name][index])
                current_list=[]
                for column_name in column_names_of_response_csv:
                    if column_name not in  not_included_columns_in_show_more_details:
                        current_list.append(str(response_csv[column_name][index]))
                
                current_more_details_list.append(current_list)
            

            cluster_id_queries_list_dict.update({cluster_id:current_cluster_members_list}) 
            cluster_id_show_more_info_dict.update({cluster_id:current_more_details_list})  
            #updating cluster id
            cluster_id+=1
                



        #updating response csv
        # print("no")
        response_csv[is_added_cluster_column]=is_query_added_to_cluster_column
        response_csv[cluster_id_index_mapping_column_name]=cluster_id_index_mapping_column
        #updating centroid csv 
        initial_centroid_list=[str(cluster_id)+'@'+str(centroid_mn_mx) for cluster_id,centroid_mn_mx in cluster_id_centroid_mapping_dict.items()]
        while(len(initial_centroid_list)<len(centroid_csv[centroids_column_name])):
            initial_centroid_list.append("empty")
        centroid_csv[centroids_column_name]=initial_centroid_list
        response_csv.to_csv(Response_csv_path,index=False,header=True)
        centroid_csv.to_csv(Centroid_csv_path,index=False,header=True)


        summary= str(len(leaf_nodes_index_list_dict))+' '+ analysis_column_name +' Structure / type are found. There are total '+str(len(leaf_nodes_index_list_dict))+' different ' +analysis_column_name+ ' Structure / type from '+str(len(full_query_list))+' Total '+analysis_column_name
        clusterable_embedding = umap.UMAP(
            n_neighbors=10,
            min_dist=0.0,
            n_components=2,
            random_state=42,
        ).fit_transform(feature_matrix)
        scatterplot_dataframe=pd.DataFrame({"X": clusterable_embedding[:,0],"Y": clusterable_embedding[:,1],'label':[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()]})
        # reduced_feature_matrix=pca_reduction(feature_matrix)
        # scatterplot_dataframe=pd.DataFrame({"X": [index for index in reduced_feature_matrix['X']],"Y": [index for index in reduced_feature_matrix['Y']],'label':[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()]})
        barplot_dataframe = pd.DataFrame({"cluster_id": [cluster_id for cluster_id in range(0,len(cluster_id_representative_dict)) ],"total_no_of_clusters": [len(cluster_id_queries_list_dict[index]) for index in range(0,len(cluster_id_queries_list_dict))]})

        global_barplot_dataframe=barplot_dataframe
        global_scatterplot_dataframe=scatterplot_dataframe

        # #umap
        # clusterable_embedding = umap.UMAP(
        #     n_neighbors=10,
        #     min_dist=0.0,
        #     n_components=2,
        #     random_state=42,
        # ).fit_transform(feature_matrix)

        # plt.scatter(clusterable_embedding[:,0], clusterable_embedding[:,1], c=[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()], cmap='viridis')
        # plt.show()

        curr_box=[]
        #Question textbox
        curr_box.append(gr.Textbox.update(value=''))
        #Query textbox
        curr_box.append(gr.Textbox.update(value=''))
        #summary box
        curr_box.append(gr.Textbox.update(value=summary,visible=True))
        #plotting
        curr_box.append(gr.BarPlot.update(barplot_dataframe,visible=True,x='cluster_id',y='total_no_of_clusters'))
        curr_box.append(gr.ScatterPlot.update(scatterplot_dataframe,visible=True,x='X',y='Y',color='label'))

        for cluster_id in range(0,max_output):
                if cluster_id<len(cluster_id_representative_dict):
                    curr_box.append(gr.Textbox.update(value=cluster_id_representative_dict[cluster_id],visible=True))
                    curr_box.append(gr.Textbox.update(value=len(cluster_id_queries_list_dict[cluster_id]),visible=True))
                    curr_box.append(gr.Dataframe.update(value=[[query_list] for query_list in cluster_id_queries_list_dict[cluster_id]],visible=False))
                    curr_box.append(gr.Dataframe.update(value=pd.DataFrame(cluster_id_show_more_info_dict[cluster_id]),visible=False))
                    
                    curr_box.append(gr.Button.update(visible=True))
                    curr_box.append(gr.Button.update(visible=True))
                    curr_box.append(gr.Button.update(visible=True))
                else:
                    curr_box.append(gr.Textbox.update(visible=False))
                    curr_box.append(gr.Textbox.update(visible=False))
                    curr_box.append(gr.Dataframe.update(visible=False))
                    curr_box.append(gr.Dataframe.update(visible=False))
                    curr_box.append(gr.Button.update(visible=False))
                    curr_box.append(gr.Button.update(visible=False))
                    curr_box.append(gr.Button.update(visible=False))


        return curr_box 

       
            
    #checking added new queries belong to current clusters or not by centroid method, also updating centroid dict
    feature_matrix=embedding_model_4(full_query_list)
    current_total_clusters=len(cluster_id_index_list_dict)

    cluster_id_index_list_dict,cluster_id_centroid_min_max_dict=get_labels_for_new_query_list(new_added_queries_index_list,cluster_id_centroid_min_max_dict,cluster_id_index_list_dict,feature_matrix)
    # print(cluster_id_index_list_dict)
    is_query_added_to_cluster_column=['no' for index in range(0,len(response_csv))]  
    cluster_id_index_mapping_column=['' for index in range(0,len(response_csv))]  
    cluster_id_centroid_mapping_dict={}

    # print("yess")
    # print(current_total_clusters)
    # print(len(cluster_id_index_list_dict))
    for cluster_id,index_list in cluster_id_index_list_dict.items():

        #current cluster  centroid, min,max
        cluster_centroid_,min_distance_from_centroid_,max_distance_from_centroid_=cluster_id_centroid_min_max_dict[cluster_id]
        rand_idx = random.randrange(len(index_list))
        cluster_id_representative_dict.update({cluster_id:response_csv[analysis_column_name][index_list[rand_idx]]})

        
        current_cluster_members_list=[] 
        current_more_details_list=[]  
        for index in index_list:
            #updating response csv
            is_query_added_to_cluster_column[index]='yes'
            cluster_id_index_mapping_column[index]=cluster_id

            #response csv index , cluster_id mapping
            index_cluster_id_mapping_dict.update({index:cluster_id})

            #updating centroid csv
            cluster_centroid_string_=''
            for index2 in range(0,len(cluster_centroid_)):
                if index2==len(cluster_centroid_)-1:
                    cluster_centroid_string_+=str(cluster_centroid_[index2])
                else:
                    cluster_centroid_string_+=str(cluster_centroid_[index2])+'$'
            
            cluster_id_centroid_mapping_dict.update({cluster_id:str(cluster_centroid_string_)+'@'+str(min_distance_from_centroid_)+'@'+str(max_distance_from_centroid_)})

            #updating show details, show clusters information
            

            current_cluster_members_list.append(response_csv[analysis_column_name][index])
            current_list=[]
            for column_name in column_names_of_response_csv:
                if column_name not in  not_included_columns_in_show_more_details:
                    current_list.append(str(response_csv[column_name][index]))
            
            current_more_details_list.append(current_list)
        

        cluster_id_queries_list_dict.update({cluster_id:current_cluster_members_list}) 
        cluster_id_show_more_info_dict.update({cluster_id:current_more_details_list})  
        
            

    
    #updating response csv
    response_csv[is_added_cluster_column]=is_query_added_to_cluster_column
    response_csv[cluster_id_index_mapping_column_name]=cluster_id_index_mapping_column
    #updating centroid csv 
    initial_centroid_list=[str(cluster_id)+'@'+str(centroid_mn_mx) for cluster_id,centroid_mn_mx in cluster_id_centroid_mapping_dict.items()]
    while(len(initial_centroid_list)<len(centroid_csv[centroids_column_name])):
        initial_centroid_list.append("empty")
    centroid_csv[centroids_column_name]=initial_centroid_list
    response_csv.to_csv(Response_csv_path,index=False,header=True)
    centroid_csv.to_csv(Centroid_csv_path,index=False,header=True)

    #summary
    summary=''
    if current_total_clusters==len(cluster_id_index_list_dict):
        summary= 'On Adding query no new Structure are found.'+' There are total '+str(len(cluster_id_index_list_dict))+' different ' +analysis_column_name+ ' Structure / type from '+str(len(full_query_list))+' Total '+analysis_column_name+'. '
    else:
        summary= 'On Adding query '+str(len(cluster_id_index_list_dict)-current_total_clusters) +' new Structure are found.'+' There are total '+str(len(cluster_id_index_list_dict))+' different ' +analysis_column_name+ ' Structure / type from '+str(len(full_query_list))+' Total '+analysis_column_name+'. '


    for index in new_added_queries_index_list:
        summary+='['+response_csv[analysis_column_name][index] +' is added to cluster# '+str(index_cluster_id_mapping_dict[index])+'],' 

    




    clusterable_embedding = umap.UMAP(
            n_neighbors=10,
            min_dist=0.0,
            n_components=2,
            random_state=42,
        ).fit_transform(feature_matrix)
    scatterplot_dataframe=pd.DataFrame({"X": clusterable_embedding[:,0],"Y": clusterable_embedding[:,1],'label':[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()]})
    # reduced_feature_matrix=pca_reduction(feature_matrix)
    # scatterplot_dataframe=pd.DataFrame({"X": [index for index in reduced_feature_matrix['X']],"Y": [index for index in reduced_feature_matrix['Y']],'label':[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()]})
    barplot_dataframe = pd.DataFrame({"cluster_id": [cluster_id for cluster_id in range(0,len(cluster_id_representative_dict)) ],"total_no_of_clusters": [len(cluster_id_queries_list_dict[index]) for index in range(0,len(cluster_id_queries_list_dict))]})

    global_barplot_dataframe=barplot_dataframe
    global_scatterplot_dataframe=scatterplot_dataframe

    # #umap
    # clusterable_embedding = umap.UMAP(
    #     n_neighbors=10,
    #     min_dist=0.0,
    #     n_components=2,
    #     random_state=42,
    # ).fit_transform(feature_matrix)

    # plt.scatter(clusterable_embedding[:,0], clusterable_embedding[:,1], c=[cluster_id for index,cluster_id in index_cluster_id_mapping_dict.items()], cmap='viridis')
    # plt.show()

    curr_box=[]
    #Question textbox
    curr_box.append(gr.Textbox.update(value=''))
    #Query textbox
    curr_box.append(gr.Textbox.update(value=''))
    #summary box
    curr_box.append(gr.Textbox.update(value=summary,visible=True))
    #plotting
    curr_box.append(gr.BarPlot.update(barplot_dataframe,visible=True,x='cluster_id',y='total_no_of_clusters'))
    curr_box.append(gr.ScatterPlot.update(scatterplot_dataframe,visible=True,x='X',y='Y',color='label'))

    for cluster_id in range(0,max_output):
            if cluster_id<len(cluster_id_representative_dict):
                curr_box.append(gr.Textbox.update(value=cluster_id_representative_dict[cluster_id],visible=True))
                curr_box.append(gr.Textbox.update(value=len(cluster_id_queries_list_dict[cluster_id]),visible=True))
                curr_box.append(gr.Dataframe.update(value=[[query_list] for query_list in cluster_id_queries_list_dict[cluster_id]],visible=False))
                curr_box.append(gr.Dataframe.update(value=pd.DataFrame(cluster_id_show_more_info_dict[cluster_id]),visible=False))
                
                curr_box.append(gr.Button.update(visible=True))
                curr_box.append(gr.Button.update(visible=True))
                curr_box.append(gr.Button.update(visible=True))
            else:
                curr_box.append(gr.Textbox.update(visible=False))
                curr_box.append(gr.Textbox.update(visible=False))
                curr_box.append(gr.Dataframe.update(visible=False))
                curr_box.append(gr.Dataframe.update(visible=False))
                curr_box.append(gr.Button.update(visible=False))
                curr_box.append(gr.Button.update(visible=False))
                curr_box.append(gr.Button.update(visible=False))


    return curr_box 



def clear_added_responses():
    csv=pd.read_csv(Response_csv_path)
    
    drop_index=[]
    for index in range(0,len(csv)):
        if csv['user_added_query'][index]=='yes':
            drop_index.append(index)
    csv=csv.drop(csv.index[drop_index])
    
    col=csv.columns
    new_csv=pd.DataFrame(columns=col)

    csv['Query_clusters']=['' for index in range(0,len(csv))]
    csv['Question_clusters']=['' for index in range(0,len(csv))]
    csv['is_Query_added_to_cluster']=['no' for index in range(0,len(csv))]
    csv['is_Question_added_to_cluster']=['no' for index in range(0,len(csv))]
    csv.to_csv(Response_csv_path,index=False,header=True)

    #clear centroid csv
    csv=pd.read_csv(Centroid_csv_path)
    col=csv.columns
    new_csv=pd.DataFrame(columns=col)

    new_csv.to_csv(Centroid_csv_path,index=False,header=True)
    curr_box=[]
    # print("trigger")
    # print(change_index)
    curr_box.append(gr.Textbox.update(value=''))
    curr_box.append(gr.Textbox.update(value=''))
    curr_box.append(gr.Textbox.update(value=''))
    global global_scatterplot_dataframe
    global global_barplot_dataframe
    curr_box.append(gr.BarPlot.update(global_barplot_dataframe,visible=False,x='cluster_id',y='total_no_of_clusters'))
    curr_box.append(gr.ScatterPlot.update(global_scatterplot_dataframe,visible=False,x='X',y='Y',color='label'))


    for index in range(0,max_output):
        curr_box.append(gr.Textbox.update(visible=False))
        curr_box.append(gr.Textbox.update(visible=False))
        if change_index==index:
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))

        else:
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))
        
        curr_box.append(gr.Button.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
    return curr_box


def ReInitialize_Clusters(value):
    global global_barplot_dataframe
    global global_scatterplot_dataframe
    csv=pd.read_csv(Response_csv_path)
    if value=='' or value=='None':
        curr_box=[]
        curr_box.append(gr.Textbox.update(value=''))
        curr_box.append(gr.Textbox.update(value=''))
        curr_box.append(gr.Textbox.update())
        curr_box.append(gr.BarPlot.update(value=global_barplot_dataframe,x='cluster_id',y='total_no_of_clusters',visible=False))
        curr_box.append(gr.ScatterPlot.update(value=global_scatterplot_dataframe,x='X',y='Y',visible=False,color='label'))
        for index in range(0,max_output):
            curr_box.append(gr.Textbox.update())
            curr_box.append(gr.Textbox.update())
            curr_box.append(gr.Dataframe.update())
            curr_box.append(gr.Dataframe.update())
            curr_box.append(gr.Button.update())
            curr_box.append(gr.Button.update())
            curr_box.append(gr.Button.update())
        return curr_box
        
    column_name=value.replace('By ','')
    cluster_column_name=column_name
    is_added_cluster_column='is_'+column_name+'_added_to_cluster'
    column_name_where_cluster_are_stored=column_name+'_clusters'
    summary_name=column_name
    
    csv[is_added_cluster_column]=['no' for sz in range(0,csv.shape[0])]
    csv[column_name_where_cluster_are_stored]=['' for sz in range(0,csv.shape[0])]
    csv.to_csv(Response_csv_path,index=False,header=True)
    csv=pd.read_csv(Centroid_csv_path)
    df=pd.DataFrame(columns=csv.columns)
    for index in range(max_output):
        df.loc[len(df)] =['empty' for index in range(len(csv.columns))]
    df.to_csv(Centroid_csv_path,index=False,header=True)
    curr_box=[]
    curr_box.append(gr.Textbox.update(value=''))
    curr_box.append(gr.Textbox.update(value=''))
    curr_box.append(gr.Textbox.update(visible=False))
    curr_box.append(gr.BarPlot.update(value=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]}),x='cluster_id',y='total_no_of_clusters',visible=False))
    curr_box.append(gr.ScatterPlot.update(value=pd.DataFrame({"cluster_id": [0,1,2],"total_no_of_clusters": [0,0,0]}),x='cluster_id',y='total_no_of_clusters',visible=False))
    for index in range(0,max_output):
        curr_box.append(gr.Textbox.update(visible=False))
        curr_box.append(gr.Textbox.update(visible=False))
        curr_box.append(gr.Dataframe.update(visible=False))
        curr_box.append(gr.Dataframe.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
    
    return curr_box

    

def modify_question(question):
    question=re.sub(' +', ' ', question)

    # question = nltk.word_tokenize(question)
    # result = nltk.pos_tag(question)
    # modified_ques=''
    # updated_ques=[0 for index in range(len(result))]

    updated_ques=[]
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(question)  # Your text here
    for token in doc:
        # print(token.text,token.pos_)
        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            if token.pos_ == "NOUN":
                updated_ques.append("NOUN#")
            else:
                updated_ques.append("PROPNOUN#")

        else:
            updated_ques.append(token.text)
            

    modified_ques=str(updated_ques[0])+' '
    for index in range(1,len(updated_ques)):
        if updated_ques[index]==updated_ques[index-1]:
            continue
        modified_ques+=str(updated_ques[index])+' '
    # print(modified_ques)
    # print()
    return modified_ques






def show_more_details(change_index):
    curr_box=[]
    # print("trigger")
    # print(change_index)
    curr_box.append(gr.Textbox.update())
    curr_box.append(gr.Textbox.update())
    curr_box.append(gr.Textbox.update())
    global global_scatterplot_dataframe
    global global_barplot_dataframe
    curr_box.append(gr.BarPlot.update(global_barplot_dataframe,visible=True,x='cluster_id',y='total_no_of_clusters'))
    curr_box.append(gr.ScatterPlot.update(global_scatterplot_dataframe,visible=True,x='X',y='Y',color='label'))


    for index in range(0,max_output):
        curr_box.append(gr.Textbox.update())
        curr_box.append(gr.Textbox.update())
        if change_index==index:
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=True))

        else:
            curr_box.append(gr.Dataframe.update())
            curr_box.append(gr.Dataframe.update())
        
        curr_box.append(gr.Button.update())
        curr_box.append(gr.Button.update())
        curr_box.append(gr.Button.update())
    return curr_box
def show_clusters(change_index):
    curr_box=[]
    # print("trigger")
    # print(change_index)
    
    
    curr_box.append(gr.Textbox.update())
    curr_box.append(gr.Textbox.update())
    curr_box.append(gr.Textbox.update())
    global global_scatterplot_dataframe
    global global_barplot_dataframe
    curr_box.append(gr.BarPlot.update(global_barplot_dataframe,visible=True,x='cluster_id',y='total_no_of_clusters'))
    curr_box.append(gr.ScatterPlot.update(global_scatterplot_dataframe,visible=True,x='X',y='Y',color='label'))


    for index in range(0,max_output):
        curr_box.append(gr.Textbox.update())
        curr_box.append(gr.Textbox.update())
        if change_index==index:
            curr_box.append(gr.Dataframe.update(visible=True))
            curr_box.append(gr.Dataframe.update(visible=False))

        else:
            curr_box.append(gr.Dataframe.update())
            curr_box.append(gr.Dataframe.update())
        
        curr_box.append(gr.Button.update())
        curr_box.append(gr.Button.update())
        curr_box.append(gr.Button.update())
    return curr_box


def hide_clusters(change_index):
    curr_box=[]
    # print("trigger")
    # print(change_index)
    curr_box.append(gr.Textbox.update())
    curr_box.append(gr.Textbox.update())
    curr_box.append(gr.Textbox.update())
    global global_scatterplot_dataframe
    global global_barplot_dataframe
    curr_box.append(gr.BarPlot.update(global_barplot_dataframe,visible=True,x='cluster_id',y='total_no_of_clusters'))
    curr_box.append(gr.ScatterPlot.update(global_scatterplot_dataframe,visible=True,x='X',y='Y',color='label'))


    for index in range(0,max_output):
        curr_box.append(gr.Textbox.update())
        curr_box.append(gr.Textbox.update())
        if change_index==index:
            curr_box.append(gr.Dataframe.update(visible=False))
            curr_box.append(gr.Dataframe.update(visible=False))

        else:
            curr_box.append(gr.Dataframe.update())
            curr_box.append(gr.Dataframe.update())
        
        curr_box.append(gr.Button.update())
        curr_box.append(gr.Button.update())
        curr_box.append(gr.Button.update())
    return curr_box

def clean_screen_fun():
    curr_box=[]
    # print("trigger")
    curr_box.append(gr.Textbox.update(value=''))
    curr_box.append(gr.Textbox.update(value=''))
    curr_box.append(gr.Textbox.update(value=''))
    
    global global_scatterplot_dataframe
    global global_barplot_dataframe
    curr_box.append(gr.BarPlot.update(global_barplot_dataframe,visible=False,x='cluster_id',y='total_no_of_clusters'))
    curr_box.append(gr.ScatterPlot.update(global_scatterplot_dataframe,visible=False,x='X',y='Y'))

    for index in range(0,max_output):
        curr_box.append(gr.Textbox.update(visible=False))
        curr_box.append(gr.Textbox.update(visible=False))
        
        curr_box.append(gr.Dataframe.update(visible=False))
        curr_box.append(gr.Dataframe.update(visible=False))
        
        curr_box.append(gr.Button.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
        curr_box.append(gr.Button.update(visible=False))
    return curr_box
def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-res',nargs='?',help='starting index', type=str,required=True
            )
        parser.add_argument(
            
            '-cen',nargs='?' ,help='ending index',type=str, required=True
            )
        
        args = parser.parse_args()
        return [str(args.res),str(args.cen)]    
if __name__=="__main__":
    
    [Response_csv_path,Centroid_csv_path]=get_args()
    # Centroid_csv_path='/Users/mohd.a/Desktop/repo/Prototypes/answer/in/centroid.csv'
    with gr.Blocks() as demo:
        
        with gr.Row():
            Question = gr.Textbox(label="Question",interactive=True,scale=2)
            sql_query = gr.Textbox(label="Sql_Query",interactive=True,scale=2)
            update_button = gr.Button("Update",scale=0,interactive=True)
            clean_added_response=gr.Button('clear added responses',scale=0,interactive=True)
            clean_screen=gr.Button('clean screen',scale=0,interactive=True)
            
        with gr.Row():
            analysis=gr.Dropdown(["By Query", "By Question"], label="Analysis",scale=2)
            initialized_node_depth=gr.Dropdown([2,3,4,5,6], label="Initialized Maximum Node Depth",scale=0)
            
            #for intializing clustering or Re-initializing
            ReInitialize=gr.Dropdown(['None','By Question','By Query'],scale=0,interactive=True,label='Re-Initialize')
            
            
            
        box=[]
        with gr.Column():
            summary = gr.Textbox(label="Summary",interactive=True,visible=False)
        with gr.Row():
            barplot=gr.BarPlot(label='BarPlot',visible=False,scale=10)
            scatterplot=gr.ScatterPlot(label='ScatterPlot',visible=False,scale=10)
        box.append(Question)
        box.append(sql_query)
        box.append(summary)
        box.append(barplot)
        box.append(scatterplot)
        

        for i in range(0,max_output):
            
            with gr.Row():
                cluster_representative='Cluster# '+str(i)+' Representative'
                clusters='Cluster# '+str(i)
                
                t1 = gr.Textbox(label=cluster_representative,visible=False,scale=2)
                t2 = gr.Textbox(label='Cluster# '+str(i)+' Count',visible=False,scale=0)
            with gr.Row():
                t5 = gr.Button("show cluster# "+str(i),visible=False,scale=0)
                t6 = gr.Button("hide# "+str(i),visible=False,scale=0)
                t7 = gr.Button("show more details# "+str(i),visible=False,scale=0)
            with gr.Column():
                t3 = gr.Dataframe(label=clusters,visible=False,col_count=1,scale=0,headers=['#1'],datatype=["str"])
                t4 = gr.Dataframe(label=clusters,visible=False,scale=0)            
            
            box.append(t1)
            box.append(t2)
            box.append(t3)
            box.append(t4)
            box.append(t5)
            box.append(t6)
            box.append(t7)
        
        for index in range(7,len(box)):
            if (index-5)%7==4:
                change_index=gr.Number(int((index-5)/7),visible=False)
                
                box[index].click(fn=show_clusters,inputs=change_index,outputs=box)
            if (index-5)%7==5:
                change_index=gr.Number(int((index-5)/7),visible=False)
                
                box[index].click(fn=hide_clusters,inputs=change_index,outputs=box)
            if (index-5)%7==6:
                change_index=gr.Number(int((index-5)/7),visible=False)
                box[index].click(fn=show_more_details,inputs=change_index,outputs=box)

        
        ReInitialize.change(fn=ReInitialize_Clusters,inputs=ReInitialize,outputs=box)
        
        clean_screen.click(fn=clean_screen_fun,outputs=box)
        update_button.click(fn=update, inputs=[Question,sql_query,analysis,initialized_node_depth], outputs=box)
        clean_added_response.click(fn=clear_added_responses,outputs=box)


        
        
        
    demo.launch()

