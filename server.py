from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel
import os

app = FastAPI()

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


client = OpenAI(
    base_url="https://api.scaleway.ai/488b2cbb-38e3-4cdb-ac85-7aef7f019264/v1",
    api_key="d67906c0-c6ba-4db9-bbf3-fbc34adf6d21"
)

class ChatRequest(BaseModel):
    message: str
    chat_history: list

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(request: ChatRequest):
    chat_history = request.chat_history
    chat_history.append({"role": "user", "content": request.message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-instruct",
        messages=chat_history,
        max_tokens=2048,
        temperature=0.7,
        top_p=0.7,
        presence_penalty=0,
        stream=False,
    )

    bot_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": bot_response})

    return {"response": bot_response, "chat_history": chat_history}

# Run the API
# Start the server with: uvicorn server:app --reload
