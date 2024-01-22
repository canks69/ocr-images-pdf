from fastapi import FastAPI, File, UploadFile, HTTPException, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ocr import get_text, process_text
import json
from correction import auto_correction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fungsi untuk membaca data dari file JSON
def read_data():
    with open('correction.json') as f:
        data = json.load(f)
    return data

# Fungsi untuk menulis data ke file JSON
def write_data(data):
    with open('correction.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        ocr_result = get_text(file)
        
        correction = auto_correction(ocr_result)

        responses = process_text(correction)

        return JSONResponse(content={'text': correction, 'length': len(responses), 'result': responses}, status_code=200)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/correction')
def read_correction():
    result = {}
    with open('correction.json') as f:
        result = json.load(f)
    
    return JSONResponse(content={'result': result}, status_code=200)

@app.post('/correction', response_model=dict)
async def add_correction(new_data: dict = Body(...)):
    data = read_data()
    data.update(new_data)
    write_data(data)
    return {'result': data}

@app.put('/correction/{index}', response_model=dict)
async def edit_correction(index: str = Path(..., title="Index of the item to edit"), updated_data: dict = Body(...)):
    data = read_data()

    # Memperbarui data pada index yang ditentukan
    if index in data:
        data[index] = updated_data.get("value", data[index])
    else:
        raise HTTPException(status_code=404, detail=f'Index not found: {index}')

    # Menulis data kembali ke file JSON
    write_data(data)

    return {'result': data}

@app.delete('/correction/{index}', response_model=dict)
async def delete_correction(index: str = Path(..., title="Index of the item to delete")):
    data = read_data()

    # Menghapus data pada index yang ditentukan
    if index in data:
        deleted_data = data.pop(index)
    else:
        raise HTTPException(status_code=404, detail=f'Index not found: {index}')

    # Menulis data kembali ke file JSON
    write_data(data)

    return {'deleted_data': deleted_data, 'result': data}