@@ -1,5 +1,5 @@
@@ -1,19 +1,16 @@

+FROM python:3.10-slim

(tabula ضروري لمكتبة) java تثبيت #+
+RUN apt-get update && apt-get install -y default-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir-r requi
rements.txt

COPY . .

تشغيل البوت #+
CMD ["python", "pdf_to_excel_bot.py"]