# 🤖 Conversational RAG Chatbot

A production-ready, memory-efficient Retrieval-Augmented Generation (RAG) chatbot application. It features a lightweight **FastAPI** backend integrated with **Pinecone Cloud Vector Store** and **Groq** using serverless cloud embeddings, alongside an intuitive **Streamlit** frontend.

---

## 📁 Project Structure

```text
Rag-Chatbot/
├── Backend/
│   ├── main.py            # FastAPI Server & Routes
│   ├── rag_engine.py      # Core RAG Pipeline & Pinecone Integration
│   └── requirements.txt   # Memory-optimized Backend Dependencies (No Torch)
└── Frontend/
    ├── app.py             # Streamlit UI Configuration
    └── requirements.txt   # Frontend UI Dependencies

```

---

## ⚡ Setup & Local Run

### 1. Backend Setup

1. Create a `.env` file inside the `Backend/` directory:
```env
GROQ_API_KEY="your_groq_api_key"
PINECONE_API_KEY="your_pinecone_api_key"
PINECONE_INDEX_NAME="database"
HF_TOKEN="your_huggingface_token"

```


2. Start the local FastAPI server:
```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

```



### 2. Frontend Setup

1. Ensure your `Frontend/requirements.txt` contains:
```text
streamlit
requests

```


2. Launch the Streamlit interface in a new terminal window:
```bash
cd Frontend
pip install -r requirements.txt
streamlit run app.py

```



---

## 🚀 Cloud Deployment Configurations

### Backend (Render)

* **Deployment Type:** Web Service
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
* **Live API Endpoint:** `https://rag-chatbot-2-ejse.onrender.com`

### Frontend (Streamlit Cloud)

* Connect your GitHub repository to Streamlit Cloud.
* Set the main file path to `Frontend/app.py` and deploy.

```

```
