import os
import re
from openai import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec, PodSpec 


class FileUpload:
    def __init__(self):
        self.pinecone_api_key = None
        self.openai_api_key = None
        self.client = None
    def access_key(self):
        # Access the API key
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.openai_api_key = os.getenv("openai_api_key")
        self.MODEL ="text-embedding-ada-002"

        # Check user access to api_keys
        if self.pinecone_api_key is None or self.openai_api_key is None:
            return False
        else:
            return True
    def init_index(self):
        use_serverless=False
        #Index Initialization
        import time  
        # configure client  
        pc = Pinecone(api_key=self.pinecone_api_key)  
        if use_serverless:  
            spec = ServerlessSpec(cloud='aws', region='us-west-2')  
        else:  
            # if not using a starter index, you should specify a pod_type too  
            spec = PodSpec(environment='gcp-starter')
        index_name = 'omnistudy'
        index = pc.Index(name=index_name)
        while not pc.describe_index(index_name).status['ready']:  
            time.sleep(1)  
            
        # # Create the index if it doesn't exist
        # if index_name not in pinecone.list_indexes():
        #     pinecone.create_index(index_name, dimension=1536)
        return index
    def init_llm(self):
        return OpenAI(api_key=self.openai_api_key)
    def preprocess_text(self,text):
    # Replace consecutive spaces, newlines and tabs
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.strip()
        return text
    def process_pdf(self,file_path):
        # create a loader
        loader = PyPDFLoader(file_path)
        # load your data
        data = loader.load()
        # Split your data up into smaller documents with Chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=0)
        documents = text_splitter.split_documents(data)
        return documents
        
    def create_embeddings(self,texts,client):
        embeddings_list = []
        print(len(texts))
        i = 0
        for doc in texts:
            text=doc.page_content
            text = self.preprocess_text(text)
            res = client.embeddings.create(input=[text], model=self.MODEL)
            embedding = res.data[0].embedding
            page_num = doc.metadata['page']
            
            embeddings_list.append({'content': embedding, 'page_num': page_num,"text":text})
            print(i)
            i +=1

            #End early for testing
            if i == 50:
                break
        return embeddings_list
        
    def upsert_embeddings_to_pinecone(self,index, embeddings, id):
        i = 0
        for embedding in embeddings:
            identification = id +"_"+str(i)
            i += 1
            content = embedding['content']
            page_num = embedding['page_num']
            text = embedding['text']
            index.upsert(vectors=[{"id": identification,"values":content,"metadata":{"page_num" : page_num,"name":id,"text":text}}])

    def is_file_path_real(self,file_path):
        return os.path.exists(file_path)

    def upload(self,path,textbook_name):
        if not self.is_file_path_real(path):
           raise ValueError("Invalid Path to File")
        if not self.access_key():
           raise ValueError("Invalid Access to API Key")
        index = self.init_index()
        client = self.init_llm()
        texts = self.process_pdf(file_path)
        embeddings = self.create_embeddings(texts=texts,client=client)
        self.upsert_embeddings_to_pinecone(index, embeddings, id=textbook_name)
        print("Finished Upload")
        



    
if __name__=="__main__":
    file_path = "./Textbooks/ClinicalPsychology.pdf"  #Replace with call to sql eventually
    # create a FileUpload object
    uploader = FileUpload()
    # use the upload method to upload your file to Pinecone
    uploader.upload(file_path,textbook_name="ClinPhys2")
    