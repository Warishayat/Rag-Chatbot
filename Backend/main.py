import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# LangChain structured message formats
from langchain_core.messages import HumanMessage, AIMessage
from rag_engine import rag_backend

app = FastAPI(
    title="Enterprise RAG Chatbot Gateway",
    version="1.0.0"
)

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- VALIDATION SCHEMAS ---
class ChatMessageSchema(BaseModel):
    role: str       # user ya assistant
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessageSchema]

# --- ROUTING LOGIC ---

@app.post("/upload", status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Unsupported format '.{ext}'."
        )
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    try:
        rag_backend.process_file(file_path, ext)
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"message": f"Successfully processed and stored '{file.filename}' in Pinecone."}
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", status_code=status.HTTP_200_OK)
async def chat(payload: ChatRequest):
    # Map raw JSON objects to actual LangChain structural entities
    formatted_history = []
    for msg in payload.history:
        if msg.role == "user":
            formatted_history.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            formatted_history.append(AIMessage(content=msg.content))
            
    try:
        answer = rag_backend.query(payload.message, formatted_history)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)