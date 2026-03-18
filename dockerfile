FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    default-jre-headless \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install numpy==1.21.6

COPY requirements.txt .

RUN pip install --no-cache-dir --only-binary pandas pandas==1.3.5

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]