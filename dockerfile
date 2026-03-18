FROM python:3.9-slim

# تثبيت Java فقط
RUN apt-get update && apt-get install -y default-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ترقية pip
RUN pip install --upgrade pip setuptools wheel

# تثبيت numpy أولاً (بإصدار متوافق)
RUN pip install numpy==1.21.6

# نسخ requirements وتثبيت الباقي
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]
