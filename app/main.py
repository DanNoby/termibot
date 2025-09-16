from fastapi import FastAPI, HTTPException, Request
import google.generativeai as genai
from google.generativeai import GenerativeModel
import os, re
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Configure the Gemini API with the loaded key
genai.configure(api_key=api_key)



# Formatting text
def clean_markdown(text: str) -> str:
    # Remove code fences ```
    text = re.sub(r"```.*?```", lambda m: m.group(0).strip("`"), text, flags=re.S)
    text = text.replace("```", "")

    # Remove bold/italic markers
    text = text.replace("**", "").replace("*", "").replace("_", "")

    # Remove Markdown headings (#, ##, etc.)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)

    # Remove links but keep link text [text](url) → text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    return text.strip()


# Instantiate the model
model = GenerativeModel(model_name="gemini-1.5-flash-latest")

app = FastAPI()

@app.post("/", response_class=PlainTextResponse)
async def chat_endpoint(request: Request):
    # Read raw text from request body
    prompt_bytes = await request.body()
    prompt = prompt_bytes.decode("utf-8").strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # Call Gemini API asynchronously
        response = await model.generate_content_async(contents=prompt)
        reply = response.text or ""
        reply = clean_markdown(reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return reply
