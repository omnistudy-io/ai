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


class Chat:
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
    def init_all(self,text_name):
        if not self.access_key():
            #Make certain to declare env variables
            raise LookupError("Failure to Access Keys")
        index = self.init_index()
        embeddings = self.init_embeddings()
        
        template = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say "The provided textbook/document doesn't contain information to give you the correct answer". 
        Use three sentences maximum and keep the answer concise.
        Question: {question} 
        Context: {context} 
        Answer:
        """
        prompt = PromptTemplate.from_template(template=template)
        text_field = "text"  
        vectorstore = PineconeVectorStore(  
            index, embeddings, text_field  
        )  
        retriever = vectorstore.as_retriever(filter={"name":text_name},search_kwargs={'k': 3})
        llm = ChatOpenAI(openai_api_key=self.openai_api_key,model_name="gpt-3.5-turbo", temperature=0)
        self.rag_chain = (
            {"context": retriever,  "question": RunnablePassthrough()} 
            | prompt
            | llm
            | StrOutputParser() 
        )
        self.initialized = True
    def run(self,text_name,query):
        if not self.initialized:
            self.init_all(text_name)
        return self.rag_chain.invoke(query)
if __name__=="__main__":
    chat = Chat()
    query = "Whats the percentage of homeless people with schizophrenia?" 
    ans = chat.run(query=query,text_name="ClinPhys2")
    print(ans)

    