FROM ubuntu:22.04

# منع التوقف أثناء التثبيت
ENV DEBIAN_FRONTEND=noninteractive

# تثبيت Python وجميع المتطلبات
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    default-jre \
    wget \
    curl \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ترقية pip
RUN pip3 install --upgrade pip

# تثبيت numpy أولاً
RUN pip3 install numpy==1.24.3

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "pdf_to_excel_bot.py"]
