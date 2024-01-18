from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ocr import get_text
from correction import auto_correction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        ocr_result = get_text(file)

        result = auto_correction(ocr_result)

        return JSONResponse(content={'result': result}, status_code=200)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
