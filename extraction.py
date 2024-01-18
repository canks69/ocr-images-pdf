import pytesseract
import pdfplumber

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def from_image(image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text