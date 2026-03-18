FROM python:3.9.18-slim-bullseye

# تثبيت Java فقط (بدون تعقيدات)
RUN apt-get update && apt-get install -y default-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ترقية pip
RUN pip install --upgrade pip setuptools wheel

# تثبيت المكتبات بشكل تدريجي
COPY requirements.txt .
RUN pip install --no-cache-dir numpy==1.23.5
RUN pip install --no-cache-dir pandas==2.0.3
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]
