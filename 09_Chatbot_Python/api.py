# api.py
import os
from functools import lru_cache
from fastapi import FastAPI
from pydantic import BaseModel
from bot_core import Chatbot

@lru_cache()
def get_bot():
    # make relative paths (models/, data/) resolve
    base = os.path.dirname(__file__)
    return Chatbot(base_dir=base)

app = FastAPI(title="PyPI & Python FAQ Chatbot API")

class Query(BaseModel):
    query: str

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/chat")
def chat(q: Query):
    bot = get_bot()
    return {"answer": bot.get_answer(q.query)}

# optional: warm up on start so first request isn’t slow
@app.on_event("startup")
def warmup():
    get_bot()

