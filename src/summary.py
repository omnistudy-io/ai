import os
import time
from pinecone import Pinecone, ServerlessSpec, PodSpec 
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings 
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore 
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


class Summarizer:
    def __init__(self):
        """Initialize API Keys, Encoding Model """
        self.pinecone_api_key = None
        self.openai_api_key = None
        self.client = None
        self.MODEL ="text-embedding-ada-002"
        self.index_name = "omnistudy"
        self.initialized = False
        self.rag_chain = None
    def access_key(self):
        # Access the API key
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        self.prompt_template = "Given context: {context}. Answer the question: Tell me about this document"

        # Check user access to api_keys
        if self.pinecone_api_key is None or self.openai_api_key is None:
            return False
        else:
            return True
    def init_index(self):
        use_serverless=False
        #Declare the index
        pc = Pinecone(api_key=self.pinecone_api_key)  
        if use_serverless:  
            spec = ServerlessSpec(cloud='aws', region='us-west-2')  
        else:  
            # if not using a starter index, you should specify a pod_type too  
            spec = PodSpec(environment='gcp-starter')
        index = pc.Index(name=self.index_name)
        #Await index
        while not pc.describe_index(self.index_name).status['ready']:  
            time.sleep(1)  
        return index
    
    def init_llm(self):
        return OpenAI(api_key=self.openai_api_key)

    def init_embeddings(self):
        embeddings = OpenAIEmbeddings(  
            model='text-embedding-ada-002',  
            openai_api_key= self.openai_api_key 
        )  
        return embeddings
    def generate_pages(self,index,text_name,begin_page,end_page):

        query_vector = [0.1] * 1536

        #query the data base for docs within begin and end pages
        data = index.query(
            namespace=text_name,
            vector=query_vector,
            filter={
                "$and": [
                    {"page_num": {"$gte": begin_page}},
                    {"page_num": {"$lte": end_page}}
                ]
            },
            top_k=100,     #top_k is 100, but unless you request a lot of pages, it will give below 100 docs
            include_metadata=True,
        )
        sorted_docs = sorted(data['matches'], key=lambda x: x['metadata']['page_num'])
        relevant_docs = []
        for doc in sorted_docs:
            content = doc['metadata']['text']
            relevant_docs.append(content)
        return relevant_docs
    
    def init_all(self,text_name,length,begin_page,end_page):
        if not self.access_key():
            #Make certain to declare env variables
            raise LookupError("Failure to Access Keys")
        index = self.init_index()
        embeddings = self.init_embeddings()
        relevant_docs = self.generate_pages(index,text_name=text_name,begin_page=begin_page,end_page=end_page)
        
        template = """
            Given the following context: 
            {context}
            Write a summary of the context of length
        """ + str(length) + "words: "
        self.prompt = PromptTemplate.from_template(template=template)  
        self.llm = ChatOpenAI(openai_api_key=self.openai_api_key,model_name="gpt-3.5-turbo", temperature=0)

        
        
        self.initialized = True
    def run(self,text_name,length,begin_page,end_page):
        if not self.initialized:
            self.init_all(text_name,length,begin_page,end_page)
        return self.llm.invoke(self.prompt)
if __name__=="__main__":
    begin_page = 2
    end_page = 5
    length = 200
    summarizer = Summarizer()
    ans = summarizer.run(length,begin_page,end_page,text_name="ClinPhys2")
    print(ans)

    









