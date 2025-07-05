from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.inference import generate_response

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

# ✅ Handler sukses & error seragam
def custom_response(status_code: int, message: str, detail: dict | None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "detail": detail
        }
    )

# ✅ Endpoint utama
@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        return custom_response(
            status_code=400,
            message="Pertanyaan tidak boleh kosong!",
            detail=None
        )

    try:
        answer = generate_response(question)

        if answer.lower().startswith("maaf"):
            return custom_response(
                status_code=422,
                message="Model tidak dapat memproses pertanyaan ini.",
                detail=None
            )

        return custom_response(
            status_code=200,
            message="Success Request!",
            detail={
                "question": question,
                "answer": answer
            }
        )

    except Exception as e:
        return custom_response(
            status_code=500,
            message=f"Terjadi kesalahan pada server: {str(e)}",
            detail=None
        )
