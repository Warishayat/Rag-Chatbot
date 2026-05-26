import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from Services.Embedding import Embeddings
from Services.parser import load_documents
from Utils.chunking import split_documents

VECTOR_BASE_PATH = "vector_db"
embeddings = Embeddings()

def get_retriever(path: str):
    file_name = os.path.basename(path)
    file_vector_path = os.path.join(VECTOR_BASE_PATH, file_name)
    bm25_path = os.path.join(file_vector_path, "bm25.pkl")

    if os.path.exists(file_vector_path) and os.path.exists(bm25_path):
        print(f"Loading existing vector db for: {file_name}")
        vector_store = FAISS.load_local(
            file_vector_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        with open(bm25_path, "rb") as f:
            bm25 = pickle.load(f)

    else:
        print(f"Creating vector db for: {file_name}")
        docs = load_documents(file_path=path)
        chunks = split_documents(docs)

        vector_store = FAISS.from_documents(chunks, embeddings)
        os.makedirs(file_vector_path, exist_ok=True)
        vector_store.save_local(file_vector_path)

        bm25 = BM25Retriever.from_documents(chunks)
        bm25.k = 3

        with open(bm25_path, "wb") as f:
            pickle.dump(bm25, f)

    faiss_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    ensemble = EnsembleRetriever(
        retrievers=[bm25, faiss_retriever],
        weights=[0.6, 0.4]
    )

    return ensemble


if __name__ == "__main__":
    path = r"C:\Users\HP\OneDrive\Desktop\Rag-Chatbot\Rag-Chatbot\Backend\data\9.-Nineteen-Eighty-Four-Author-George-Orwell (2).pdf"

    retriever = get_retriever(path)
    while True:
        query = input("\nEnter query: ")
        if query.lower() == "exit":
            break
        result = retriever.invoke(query)

        print("Result is:\n")

        for doc in result:
            print(doc.page_content[:300])
