import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# Request model for chat input
class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama-3.3-70b-versatile"  # Default model

@app.post("/chat")
async def chat_with_groq(request: ChatRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": request.prompt}],
            model=request.model,
        )
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "FastAPI Groq API is running!"}
