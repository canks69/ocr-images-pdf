from fastapi import HTTPException
from PIL import Image
from extraction import from_image, from_pdf
from correction import auto_correction

def get_text(file):
    if file.content_type.startswith("image"):
        # Image file
        image = Image.open(file.file)
        text = from_image(image)
    elif file.content_type.startswith("application/pdf"):
        # PDF file
        text = from_pdf(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload an image or a PDF.")

    return text