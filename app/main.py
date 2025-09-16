from fastapi import FastAPI, HTTPException, Request
import google.generativeai as genai
from google.generativeai import GenerativeModel
import os
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse  # Correct import

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

@app.post("/chat", response_class=PlainTextResponse)  # Corrected line
async def chat_endpoint(request: Request):
    # Read raw text from request body
    prompt_bytes = await request.body()
    prompt = prompt_bytes.decode("utf-8").strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # Call Gemini API asynchronously
        response = await model.generate_content_async(contents=prompt)
        reply = response.text

        # code formatting
        if "```" not in reply:
            reply = f"```\n{reply}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PlainTextResponse(reply)