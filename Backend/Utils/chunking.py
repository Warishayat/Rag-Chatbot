from langchain_text_splitters import RecursiveCharacterTextSplitter
from Services.parser import load_documents


def split_documents(documents):
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1200,
      chunk_overlap=250
  )
  chunks = text_splitter.split_documents(documents)
  return chunks



if __name__ == "__main__":
    documents = load_documents(r"C:\Users\HP\OneDrive\Desktop\Rag-Chatbot\Rag-Chatbot\Backend\data\9.-Nineteen-Eighty-Four-Author-George-Orwell (2).pdf")
    chunks = split_documents(documents)
    print(f"Total Chunks: {len(chunks)}")
    print(f"Chunk Size: {len(chunks[0].page_content)}")
