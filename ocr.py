from fastapi import HTTPException
from PIL import Image
from extraction import from_image, from_pdf
from correction import auto_correction
import re

def get_text(file):
    if file.content_type.startswith("image"):
        image = Image.open(file.file)
        text = from_image(image)
    elif file.content_type.startswith("application/pdf"):
        text = from_pdf(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload an image or a PDF.")

    return text

def process_text(text):
    pattern = re.compile(r'Transfer Rupiah\D*([-\d.,]+)?\D*(?:BANK MANDIRI)?\n([^0-9]+)?\s*([\d/]+)?')

    # Mencocokkan pola dengan teks
    matches = pattern.findall(text)

    # for match in matches:
    
    return matches
