import os
import warnings
import sys 
sys.path.append(".")
warnings.filterwarnings("ignore")
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import pandas as pd
#keys


class LLM():
    def __init__(self,timeout,itr):
        _ = load_dotenv(find_dotenv())
        self.timeout=timeout
        self.itr=itr
        self.AZURE_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AZURE_API_KEY = os.getenv("AZURE_OPENAI_KEY")
        self.AZURE_API_TYPE = "azure"
        self.MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DNAME")
        self.MODEL_API_VERSION = "2023-05-15"
        pass
    def get_response(self,prompt):
        llm = AzureChatOpenAI(
                        deployment_name=self.MODEL_DEPLOYMENT_NAME,
                        openai_api_version=self.MODEL_API_VERSION,
                        openai_api_base=self.AZURE_API_BASE,
                        openai_api_key=self.AZURE_API_KEY,
                        request_timeout=self.timeout, 
                        max_retries=self.itr
                    )
        
        return str(llm(
            [
                
                HumanMessage(
                    content=prompt
                )
            ]
        ))
