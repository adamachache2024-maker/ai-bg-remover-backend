from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from rembg import remove

# 1. إنشاء تطبيق FastAPI
app = FastAPI(title="AI Background Remover API")

# 2. إضافة إعدادات CORS للسماح للواجهة (index.html) بالاتصال بالسيرفر بدون حظر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. نقطة النهاية لمعالجة وإزالة الخلفية
@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output_bytes = remove(image_bytes)
    return Response(content=output_bytes, media_type="image/png")