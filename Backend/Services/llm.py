from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


Model=ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0.3,
)

if __name__ == "__main__":
    Response = Model.invoke("Who is prime minister of pakistan?")
    print(Response.content)
    