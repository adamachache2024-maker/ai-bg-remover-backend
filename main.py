from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove

app = FastAPI()

# إعداد أذونات CORS الشاملة مع السماح لطلبات OPTIONS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online"}

@app.options("/remove-bg")
async def options_remove_bg():
    return Response(status_code=200)

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        input_image = await file.read()
        output_image = remove(input_image)
        return Response(content=output_image, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
