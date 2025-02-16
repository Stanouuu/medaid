from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# from sse_starlette.sse import EventSourceResponse
from openai import OpenAI
from pydantic import BaseModel
from loguru import logger
import os

app = FastAPI()

logger.add("logs/app.log", rotation="1 day", retention="7 days", compression="zip")

logger.info("Application has started.")


# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

client = OpenAI(
    base_url="https://api.scaleway.ai/488b2cbb-38e3-4cdb-ac85-7aef7f019264/v1",
    api_key="d67906c0-c6ba-4db9-bbf3-fbc34adf6d21"
)

class ChatRequest(BaseModel):
    message: str
    chat_history: list

@app.get("/")
def read_root():
    logger.info("Loading Home Page.")
    return FileResponse("static/index.html")
    
    
@app.post("/chat")
async def chat(request: ChatRequest):
    logger.info("Posting Chat.")

    if not request.chat_history:
        logger.info("Chatting For the 1st Time.")
        chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    else:
        chat_history = request.chat_history
        chat_history.append({"role": "user", "content": request.message})

    logger.info("Calling llama.")

    # Prepare a generator for streaming the response to the client
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
