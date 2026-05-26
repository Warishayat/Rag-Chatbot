import os
from langchain_core.output_parsers import StrOutputParser
from Services.VectorStore import get_retriever
from Services.llm import Model
from Utils.Prompt import prompt_templete

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(query: str, file_name: str, session_id: str = "default"):
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    file_path = os.path.join(data_dir, file_name)
    
    if not os.path.exists(file_path):
        return {"answer": f"Error: File {file_name} not found. Please upload it first.", "sources": []}
    
    retriever = get_retriever(file_path)
    docs = retriever.invoke(query)
    context = format_docs(docs)

    prompt = prompt_templete()
    rag_chain = prompt | Model | StrOutputParser()
    
    answer = rag_chain.invoke({"context": context, "question": query})
    
    sources = [doc.metadata for doc in docs]
            
    return {"answer": answer, "sources": sources}
