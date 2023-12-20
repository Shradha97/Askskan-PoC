class preprocess():
    def __init__(self):
        self.preprocessed_data=[]
        pass
    def preprocess_the_data(self,data):

        columns=data.columns
        data.columns=[i for i in range(0,len(data.columns))]
        for i in range(0,len(columns)):
            if data[i].dtypes=='object':
                most_common=data[i].value_counts().index[0]
            else:
                most_common=data[i].mean()
            data[i]=data[i].fillna(value=most_common)
        data.columns=columns
        return data
    


