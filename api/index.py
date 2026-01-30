import os
from fastapi import FastAPI, Request
from langchain_postgres import PostgresChatMessageHistory
from langchain_openai import ChatOpenAI
import psycopg

app = FastAPI()

# Format Vercel's DB URL for SQLAlchemy/LangChain compatibility
DB_URL = os.environ.get("POSTGRES_URL").replace("postgres://", "postgresql://")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default-session")
    user_input = data.get("message")

    # 1. Setup Chat History
    sync_connection = psycopg.connect(DB_URL)
    history = PostgresChatMessageHistory(
        "chat_history", session_id, sync_connection=sync_connection
    )
    
    # 2. Get LLM Response
    llm = ChatOpenAI(model="gpt-5-nano")
    # LangChain automatically injects history if using RunnableWithMessageHistory
    # For a simple version:
    history.add_user_message(user_input)
    ai_msg = llm.invoke(user_input)
    history.add_ai_message(ai_msg.content)

    return {"response": ai_msg.content}

@app.get("/")
def home():
    return {"status": "API is running"}