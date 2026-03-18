FROM python:3.9-slim

RUN apt-get update && apt-get install -y default-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip config set global.index-url https://pypi.douban.com/simple/

RUN pip install --upgrade pip

RUN pip install numpy==1.21.6

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pdf_to_excel_bot.py"]
