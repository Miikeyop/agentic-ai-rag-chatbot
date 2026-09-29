from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel

from langgraph_flow import graph


app = FastAPI(
    title="Agentic AI RAG Chatbot",
    description="RAG chatbot grounded in the Agentic AI eBook",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
def health():
    return {
        "message": "Agentic AI RAG API is working"
    }


@app.get("/pdf")
def view_pdf():
    return FileResponse(
        path="data/Ebook-Agentic-AI.pdf",
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            'inline; filename="Agentic-AI.pdf"'
        }
    )


@app.get("/pdf/download")
def download_pdf():
    return FileResponse(
        path="data/Ebook-Agentic-AI.pdf",
        media_type="application/pdf",
        filename="Agentic-AI.pdf"
    )


@app.post("/chat")
def chat(data: ChatRequest):
    result = graph.invoke({
        "question": data.question
    })

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "context": result["context"]
    }