import tensorflow_hub as hub
from absl import logging
import numpy as np
import random
from sklearn.cluster import DBSCAN
from collections import Counter
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

class sql_clustering():
    def __init__(self):
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.model = hub.load(module_url)
        self.parent=[]
        self.cosine_similarity_matrix=[]
        self.cluster_label=[]

    def encode_sql_query(self,sql_queries_list):
        embeddings = self.model(sql_queries_list)
        return embeddings
    
    def get_clusters_by_clustering(self,sql_queries_list,no_of_cluster):
        feature_vectors=self.encode_sql_query(sql_queries_list)
        self.cosine_similarity_matrix=np.inner(feature_vectors, feature_vectors)
        clustering = KMeans(n_clusters=no_of_cluster).fit(1-self.cosine_similarity_matrix)
        self.cluster_label=clustering.labels_
        print(Counter(clustering.labels_))
        return self.cluster_label
        

    def get_silhouette_score(self):
        return silhouette_score(1-self.cosine_similarity_matrix,self.cluster_label)
    def get_clusters(self,sql_queries_list,threshold):
        feature_vectors=self.encode_sql_query(sql_queries_list)
        self.cosine_similarity_matrix=np.inner(feature_vectors, feature_vectors)

        #let say query name are 0,1,.....,(len(enoded_sql_list)-1)
        # for index in range(0,len(cosine_similarity_matrix)):
        #     self.parent.append(index)
        # print(cosine_similarity_matrix)
    
        # for index1 in range(0,len(cosine_similarity_matrix)):
        #     for index2 in range(index1,len(cosine_similarity_matrix)):
        #         # print(id1,id2)
        #         if index1<index2 and cosine_similarity_matrix[index1][index2]>threshold:
                    
                    
        #             if self.parent[index1]==index1:
        #                 #root
        #                 self.parent[index2]=index1
        #             else:
        #                 #1<--2<---3
        #                 self.parent[index2]=self.parent[index1]
        clusters_dict={}
        self.cluster_label=[i+1 for i in range(0,len(self.cosine_similarity_matrix))]
        for index1 in range(0,len(self.cosine_similarity_matrix)):
            for index2 in range(index1,len(self.cosine_similarity_matrix)):
                if index1<index2 and self.cosine_similarity_matrix[index1][index2]>threshold:
                    member=True
                    for index3 in range(0,len(self.cluster_label)):
                        if self.cluster_label[index3]==self.cluster_label[index1] and self.cosine_similarity_matrix[index2][index3]<threshold:
                            member=False
                    if member==True:
                        self.cluster_label[index2]=self.cluster_label[index1]




        for index1 in range(0,len(self.cosine_similarity_matrix)):
            for index2 in range(index1,len(self.cosine_similarity_matrix)):
                if self.cluster_label[index1]==self.cluster_label[index2] and self.cosine_similarity_matrix[index1][index2]<threshold:
                    print(self.cosine_similarity_matrix[index1][index2]) 
        
        #normalizing labels to 0,1,2,3...
        old_labels=Counter(self.cluster_label)
        cluster_id=0
        mapp={}
        for label in old_labels:
            mapp[label]=cluster_id
            cluster_id+=1

        for index1 in range(0,len(self.cluster_label)):
            self.cluster_label[index1]=mapp[self.cluster_label[index1]]
        
        return self.cluster_label