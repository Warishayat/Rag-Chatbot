from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1200,
      chunk_overlap=250
  )
  chunks = text_splitter.split_documents(documents)
  return chunks
