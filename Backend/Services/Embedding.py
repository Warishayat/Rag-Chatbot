from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from Services.parser import load_documents
from Utils.chunking import split_documents


def Embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


if __name__ == "__main__":
   embeddings = Embeddings()
   print(len(embeddings.embed_query("Hello World")))