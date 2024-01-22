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
    # Membuat pola regular expression untuk menangkap informasi yang diinginkan
    pattern = re.compile(r'\) Transfer Rupiah.*?([+-]?)Rp ([\d.,]+)”\nTransfer (?:ke|dari) (BANK [^\n]+)\n(.*?) (\d+)')
    # Mencocokkan pola dengan string dan mendapatkan hasil
    matches = pattern.findall(text)
    # Membuat list untuk menyimpan hasil parsing
    results = []

    # Iterasi melalui hasil dan menyusunnya dalam format yang diinginkan
    for match in matches:
        result = {
            "name": match[3],
            "amount": match[1],
            "bank": match[2],
            "rekening": match[4]
        }
        results.append(result)

    return results

def generate_transacrion(text):
    # Pola regex untuk mengekstrak informasi yang diperlukan
    pattern = re.compile(r'Transfer Rupiah\D*([\d.,]+)\D*BANK (MANDIRI?)\n([^0-9]+)\s*([\d/]+)')

    # Mencocokkan pola dengan teks
    matches = pattern.findall(text)

    results = []
    for match in matches:
        result = {
            "name": match[2],
            "amount": match[0],
            "bank": match[1],
            "rekening": match[3]
        }
        results.append(result)
    # result = [(match[0].replace('.', ''), match[1].strip(), match[2].strip(), match[3].strip()) for match in matches]
    
    return results