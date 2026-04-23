from langchain.chat_models import ChatOpenAI
from langchain.chains import create_retrieval_chain,create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate
from config import Config

class LlmService:
    def __init__(self,vector_store):
        self.llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.7,openai_api_key=Config.OPENAI_API_KEY)
        self.memory_retriever=create_history_aware_retriever(vector_store.as_retriever(),k=5)
        self.chain=create_retrieval_chain(self.llm,self.memory_retriever,return_source_documents=True)
    def generate_response(self,query):
        try:
            response=self.chain.run(query)
            return response['answer']
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I couldn't process your request at the moment."

       