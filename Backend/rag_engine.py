import os
from dotenv import load_dotenv
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.embeddings = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=os.getenv("HF_TOKEN")
        )
        
        self.llm = ChatGroq(
            temperature=0.1,  
            model_name="openai/gpt-oss-20b",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        self.vector_store = PineconeVectorStore(
            index_name=self.index_name, 
            embedding=self.embeddings
        )
        
        self.refresh_pipeline()

    def refresh_pipeline(self):
        """Dynamic retrieval layers setup."""
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        self._build_rag_chain()

    def process_file(self, file_path: str, file_type: str):
        """
        CRITICAL ISOLATION RULE: 
        Har nayi upload par purana data wipeout hoga aur sirf naye document ke vectors save honge.
        """
        try:
            print(f"[PINECONE]: Flushing existing vectors from index '{self.index_name}'...")
            index_instance = self.pc.Index(self.index_name)
            index_instance.delete(delete_all=True)
            print("[PINECONE]: Index successfully cleared.")
        except Exception as e:
            print(f"[WARNING]: Could not clear index (maybe it was already empty): {str(e)}")

        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type == "docx":
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        docs = loader.load()
        chunks = self.text_splitter.split_documents(docs)
        
        self.vector_store.add_documents(chunks)
        
        self.refresh_pipeline()

    def _build_rag_chain(self):
        """Builds a history-aware conversational RAG pipeline using modern LCEL syntax."""
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, just reformulate it."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        
        self.contextualize_chain = contextualize_q_prompt | self.llm | StrOutputParser()

        system_prompt = (
            "You are an expert assistant. Answer the user's question using EXCLUSIVELY "
            "the provided retrieved context from Pinecone. Do NOT use any external knowledge. "
            "If the answer is not explicitly mentioned in the context, reply with: "
            "'I cannot find the answer in the currently uploaded document.'\n\n"
            "Context:\n{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])

        self.rag_chain = (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(self.retriever.invoke(x["standalone_question"]))
            )
            | qa_prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, question: str, chat_history: list) -> str:
        """Runs the standalone reformulation followed by the strict RAG context block."""
        try:
            if not isinstance(chat_history, list):
                chat_history = []

            if len(chat_history) > 0:
                standalone_question = self.contextualize_chain.invoke({
                    "input": question,
                    "chat_history": chat_history
                })
            else:
                standalone_question = question

            if not isinstance(standalone_question, str):
                standalone_question = str(standalone_question)

            response = self.rag_chain.invoke({
                "input": question,
                "standalone_question": standalone_question,
                "chat_history": chat_history
            })
            
            return response

        except Exception as e:
            print(f"\n[CRITICAL REG-ENGINE ERROR]: {str(e)}\n")
            raise e

rag_backend = RAGEngine()