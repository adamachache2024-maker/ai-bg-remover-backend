from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# إنشاء جلسة باستخدام نموذج سريع وخفيف (u2netp) لتفادي البطء والتعليق
session = new_session('u2netp')

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        input_bytes = await file.read()
        # استخدام الجلسة السريعة
        output_bytes = remove(input_bytes, session=session)
        return Response(content=output_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
