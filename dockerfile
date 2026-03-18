FROM python:3.9-slim

# تثبيت Java
RUN apt-get update && apt-get install -y default-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]
