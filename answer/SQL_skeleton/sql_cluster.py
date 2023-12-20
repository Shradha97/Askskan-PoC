# import tensorflow_hub as hub
from collections import Counter
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os
import numpy as np
os.environ["TOKENIZERS_PARALLELISM"] = "false"
class sql_clustering():
    def __init__(self):

        self.node_feature_vectors={}#at a particular node say 'n' what are the feature vector of sql queries present
        self.node_index_dict={}#at a particular node say 'n' what are the index of query present
        self.node_child_dict={}
        self.leaf_node_index_list_dict={}
        self.node_kmeans_centroids_max_min_distance_dict={}
        self.inf=1000000000

    
    def get_silhouette_score(self,feature_matrix,labels):
        return silhouette_score(feature_matrix,labels)

    def optimal_cluster(self,feature_vector_matrix):
        mx_score=0
        optimal_cluster=0
        for no_of_cluster in range(2,min(int(len(feature_vector_matrix)/2),15)):
            clustering = KMeans(n_clusters=no_of_cluster).fit(feature_vector_matrix)
            if len(Counter(clustering.labels_))>1:
                silhouette_score=self.get_silhouette_score(feature_vector_matrix,clustering.labels_)
            
                if silhouette_score>mx_score:
                    mx_score=silhouette_score
                    optimal_cluster=no_of_cluster
        return mx_score,optimal_cluster

    def top_down_tree(self,node,default_silhouette_score,max_node_depth,current_node_depth):
        if len(self.node_index_dict[node])<=4 or current_node_depth>=max_node_depth:
            self.leaf_node_index_list_dict.update({node:self.node_index_dict[node]})
            return 
        if node=='n':
            feature_vector_matrix=self.node_feature_vectors[node]
            # distance_matrix=1-cosine_similarity_matrix
            sil_score,optimal_no_of_cluster=self.optimal_cluster(feature_vector_matrix)
            clustering = KMeans(n_clusters=optimal_no_of_cluster).fit(feature_vector_matrix)
            cluster_labels=clustering.labels_
            cluster_centroids=clustering.cluster_centers_

            #initializing centroids for max min distance
            distinct_labels=Counter(cluster_labels)
            for label in distinct_labels:
                child_node=node+'.'+str(label)
                #node -> centroid, min_distance, max_distance
                self.node_kmeans_centroids_max_min_distance_dict.update({child_node:([],self.inf,0)})
            
            
            node_childrens=[]
            for index in range(0,len(cluster_labels)):
                
                label=cluster_labels[index]
                #child
                child_node=node+'.'+str(label)#0 based child node indexing
                
                #feature vector
                feature_vector=self.node_feature_vectors[node][index]

                current_sql_list=[]
                current_feature_vector_list=[]
                current_index=[]
                
                if child_node not in node_childrens:
                    node_childrens.append(child_node)

                if child_node in self.node_index_dict:
                    current_index=self.node_index_dict[child_node]
                    current_feature_vector_list=self.node_feature_vectors[child_node]
                
                #current cluster centroid , max min distance 
                current_centroid_max_min=([],self.inf,0)
                if child_node in self.node_kmeans_centroids_max_min_distance_dict:
                    current_centroid_max_min=self.node_kmeans_centroids_max_min_distance_dict[child_node]
                #square of euclidean distance from centroid
                distance_from_centroid= np.sqrt(np.sum(np.square(cluster_centroids[int(label)] - feature_vector)))
                self.node_kmeans_centroids_max_min_distance_dict.update({child_node:(cluster_centroids[int(label)],min(current_centroid_max_min[1],distance_from_centroid),max(current_centroid_max_min[2],distance_from_centroid))})
                
                current_index.append(self.node_index_dict[node][index])
                current_feature_vector_list.append(self.node_feature_vectors[node][index])
                self.node_index_dict.update({child_node:current_index})
                self.node_feature_vectors.update({child_node:current_feature_vector_list})  
            self.node_child_dict.update({node:node_childrens}) 


            #calling its childrens
            for child_node in node_childrens:
                self.top_down_tree(child_node,default_silhouette_score,max_node_depth,current_node_depth+1)     

        else:
            
            if len(self.node_index_dict[node])<=5:
                self.leaf_node_index_list_dict.update({node:self.node_index_dict[node]})
                return 
            
            feature_vector_matrix=self.node_feature_vectors[node]
            # distance_matrix=1-cosine_similarity_matrix
            sil_score,optimal_no_of_cluster=self.optimal_cluster(feature_vector_matrix)
            
            if sil_score>default_silhouette_score or optimal_no_of_cluster==0:
                self.leaf_node_index_list_dict.update({node:self.node_index_dict[node]})
                return
            
            clustering = KMeans(n_clusters=optimal_no_of_cluster).fit(feature_vector_matrix)
            cluster_labels=clustering.labels_
            cluster_centroids=clustering.cluster_centers_

            #initializing centroids for max min distance
            distinct_labels=Counter(cluster_labels)
            for label in distinct_labels:
                child_node=node+'.'+str(label)
                #node -> centroid, min_distance, max_distance
                self.node_kmeans_centroids_max_min_distance_dict.update({child_node:([],self.inf,0)})
            
            node_childrens=[]
            for index in range(0,len(cluster_labels)):
                label=cluster_labels[index]
                #child
                child_node=node+'.'+str(label)#0 based child node indexing
                
                #feature vector
                feature_vector=self.node_feature_vectors[node][index]

                current_sql_list=[]
                current_feature_vector_list=[]
                current_index=[]
                
                if child_node not in node_childrens:
                    node_childrens.append(child_node)

                if child_node in self.node_index_dict:
                    current_index=self.node_index_dict[child_node]
                    current_feature_vector_list=self.node_feature_vectors[child_node]
                #current cluster centroid , max min distance 
                current_centroid_max_min=([],self.inf,0)
                if child_node in self.node_kmeans_centroids_max_min_distance_dict:
                    current_centroid_max_min=self.node_kmeans_centroids_max_min_distance_dict[child_node]
                #square of euclidean distance from centroid
                distance_from_centroid= np.sqrt(np.sum(np.square(cluster_centroids[int(label)] - feature_vector)))
                self.node_kmeans_centroids_max_min_distance_dict.update({child_node:(cluster_centroids[int(label)],min(current_centroid_max_min[1],distance_from_centroid),max(current_centroid_max_min[2],distance_from_centroid))})
                
                current_index.append(self.node_index_dict[node][index])
                current_feature_vector_list.append(self.node_feature_vectors[node][index])
                self.node_index_dict.update({child_node:current_index})
                self.node_feature_vectors.update({child_node:current_feature_vector_list})  
            self.node_child_dict.update({node:node_childrens})   

            #calling its childrens
            for child_node in node_childrens:
                self.top_down_tree(child_node,default_silhouette_score,max_node_depth,current_node_depth+1)
    
        
    def initialize_clustering(self,index_list,default_silhouette_score,max_node_depth,feature_matrix):
        root_node='n'
        self.node_index_dict.update({root_node:index_list})

        self.node_feature_vectors.update({root_node:feature_matrix})
        current_node_depth=1
        self.top_down_tree(root_node,default_silhouette_score,max_node_depth,current_node_depth)
        return
    def get_answer(self):
        return self.node_kmeans_centroids_max_min_distance_dict,self.node_child_dict,self.node_index_dict,self.leaf_node_index_list_dict
