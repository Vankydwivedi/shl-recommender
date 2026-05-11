"""
SHL Assessment Recommender — FastAPI service.

Endpoints:
  GET  /health  → {"status": "ok"}
  POST /chat    → ChatResponse
"""

import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

from agent import Agent
from models import ChatRequest, ChatResponse
from retrieval import CatalogRetriever

_retriever = CatalogRetriever()
_agent: Agent | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _agent
    loop = asyncio.get_event_loop()
    # Load retriever in thread pool to avoid blocking the event loop
    await loop.run_in_executor(None, _retriever.load)
    _agent = Agent(_retriever)
    print("Service ready.")
    yield


app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0",
    lifespan=lifespan,
)

_static = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=_static), name="static")


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(_static / "index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if _agent is None:
        raise HTTPException(status_code=503, detail="Service initializing, retry shortly")

    loop = asyncio.get_event_loop()
    try:
        response = await asyncio.wait_for(
            loop.run_in_executor(None, _agent.chat, request.messages),
            timeout=28.0,  # Leave 2s buffer from the 30s evaluator timeout
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Response generation timed out. Please retry.",
        )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
