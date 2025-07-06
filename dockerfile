# ✅ 1. Gunakan base image Python yang ringan
FROM python:3.10-slim

# ✅ 2. Tentukan direktori kerja di dalam container
WORKDIR /app

# ✅ 3. Salin dan install dependencies dari requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 4. Salin seluruh isi folder project ke dalam container
COPY . .

# ✅ 5. Expose port yang digunakan FastAPI (8000)
EXPOSE 8000

# ✅ 6. Jalankan aplikasi FastAPI dengan uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
