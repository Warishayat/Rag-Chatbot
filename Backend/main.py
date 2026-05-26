from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes.Upload import router as upload_router
from Routes.Chat import router as chat_router

app = FastAPI(title="Rag Chat Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
