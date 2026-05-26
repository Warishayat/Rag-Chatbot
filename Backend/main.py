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

@app.get("/")
async def root():
    return {"message": "Welcome to Enterprise RAG Chatbot"}


@app.post("/upload", status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile = File(...)):

    ext = file.filename.split(".")[-1].lower()

    if ext not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '.{ext}'."
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    try:

        print("=" * 50)
        print("UPLOAD STARTED")
        print("FILE:", file.filename)
        print("EXT:", ext)
        print("PATH:", file_path)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        print("FILE SAVED")

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"File save error: {str(e)}"
        )

    try:

        print("PROCESS FILE STARTED")

        rag_backend.process_file(
            file_path,
            ext
        )

        print("PINECONE SUCCESS")

        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "message":
            f"Successfully processed "
            f"'{file.filename}' "
            f"in Pinecone."
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        print("RAG ERROR:", str(e))

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"RAG Error: {str(e)}"
        )


@app.post("/chat", status_code=status.HTTP_200_OK)
async def chat(payload: ChatRequest):
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