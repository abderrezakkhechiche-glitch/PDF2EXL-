FROM python:3.9-slim

# تثبيت Java ومكتبات إضافية ضرورية
RUN apt-get update && apt-get install -y \
    default-jre-headless \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ترقية pip
RUN pip install --upgrade pip

# تثبيت numpy أولاً (لأن pandas يحتاجه)
RUN pip install numpy==1.24.3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]
