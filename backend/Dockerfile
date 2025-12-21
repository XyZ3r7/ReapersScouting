# ============================
# 1. Base image
# ============================
FROM python:3.12-slim

# ============================
# 2. Set working directory
# ============================
WORKDIR /app

# ============================
# 3. Install system dependencies
# ============================
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ============================
# 4. Install Python dependencies
# ============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================
# 5. Copy project files
# ============================
COPY . .

# ============================
# 6. Expose port
# ============================
EXPOSE 8000

# ============================
# 7. Start FastAPI with Uvicorn
# ============================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
