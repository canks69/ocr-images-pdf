FROM python:3.9-slim

# Install Tesseract dan dependensi
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev

# Atur working directory di dalam container
WORKDIR /app


# Salin file requirements.txt ke dalam container
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Atur variabel lingkungan jika diperlukan
# ENV MY_VARIABLE=value

RUN chmod -R 777 ./

# Expose port yang digunakan oleh FastAPI
EXPOSE 8081

# Perintah untuk menjalankan aplikasi FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
