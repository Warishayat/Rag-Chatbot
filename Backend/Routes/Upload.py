import os
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/api", tags=["Upload"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
    allowed_extensions = ["pdf", "docx", "txt"]
    ext = file.filename.split(".")[-1].lower()
    
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)
        
    return {"message": "File uploaded successfully", "filename": file.filename}
