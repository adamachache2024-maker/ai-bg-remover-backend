from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
import logging

# إعداد السجلات للتأكد من تفاصيل العمليات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bg_remover")

app = FastAPI(
    title="AI Background Remover API",
    description="API لتفريغ وخلفيات الصور باستخدام الذكاء الاصطناعي",
    version="1.0.0"
)

# إعدادات CORS الشاملة لضمان الاتصال مع Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """نقطة الفحص الرئيسية للتأكد من عمل السيرفر"""
    return {
        "status": "ok",
        "service": "AI Background Remover API",
        "endpoints": {
            "remove_bg": "/remove-bg [POST]"
        }
    }

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    """استلام الصورة وإزالة الخلفية منها"""
    # التحقق من أن الملف المرفوع صورة
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الملف المرفوع ليس صورة صالحة."
        )

    try:
        logger.info(f"جاري معالجة الصورة: {file.filename}")
        input_image = await file.read()
        
        # معالجة الصورة باستخدام rembg
        output_image = remove(input_image)
        
        return Response(
            content=output_image,
            media_type="image/png",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except Exception as e:
        logger.error(f"حدث خطأ أثناء المعالجة: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "حدث خطأ داخلي أثناء معالجة الصورة."}
        )
