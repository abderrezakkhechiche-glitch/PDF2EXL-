FROM python:3.9-slim

# تثبيت Java
RUN apt-get update && apt-get install -y default-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# استخدام مستودع بايثون بديل (ميرور صيني سريع)
RUN pip config set global.index-url https://pypi.douban.com/simple/

# ترقية pip
RUN pip install --upgrade pip

# تثبيت numpy أولاً
RUN pip install numpy==1.21.6

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]
