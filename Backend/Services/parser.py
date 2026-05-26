from langchain_community.document_loaders import PyMuPDFLoader,Docx2txtLoader,TextLoader



def load_documents(file_path:str):

  extension = file_path.split(".")[-1]
  print("Captured Extension is:", extension)

  if extension == "pdf":
    loader = PyMuPDFLoader(file_path=file_path)
  elif extension == "docx":
    loader = Docx2txtLoader(file_path=file_path)
  elif extension == "txt":
    loader = TextLoader(file_path=file_path,encoding='utf-8')
  else:
    raise ValueError(
            f"Unsupported file type: {extension}"
        )
  return loader.load()
