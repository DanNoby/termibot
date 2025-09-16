from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from google.generativeai import GenerativeModel  # <-- Import GenerativeModel directly
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Configure the Gemini API with the loaded key
genai.configure(api_key=api_key)

# Instantiate the model as a GenerativeModel object
model = GenerativeModel(model_name='gemini-1.5-flash-latest')

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        response = await model.generate_content_async(contents=prompt)
        reply = response.text
        if "```" not in reply:
            reply = f"```\n{reply}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"reply": reply}