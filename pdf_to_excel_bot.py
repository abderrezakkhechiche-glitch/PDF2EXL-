import os
import pandas as pd
import tabula
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
import io
import tempfile

# ------------------- الإعدادات -------------------
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ------------------- دالة البداية -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 **مرحباً! أنا بوت استخراج الجداول من PDF**\n\n"
        "أرسل لي ملف PDF وسأقوم باستخراج الجداول منه وتحويلها إلى Excel.\n\n"
        "✅ يدعم المستندات النصية فقط.\n"
        "✅ يمكن استخراج جداول متعددة من نفس الملف.\n\n"
        "✨ **أرسل الملف الآن**",
        parse_mode='Markdown'
    )

# ------------------- معالجة ملف PDF -------------------
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة المعالجة
    processing_msg = await update.message.reply_text("🔄 جاري استخراج الجداول...")
    
    try:
        # 1. تحميل الملف من تيليغرام
        file = await update.message.document.get_file()
        pdf_bytes = io.BytesIO()
        await file.download_to_memory(pdf_bytes)
        
        # 2. حفظ مؤقت للملف
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes.getvalue())
            tmp_path = tmp.name
        
        # 3. استخراج الجداول باستخدام tabula
        tables = tabula.read_pdf(tmp_path, pages='all', multiple_tables=True)
        
        # 4. التحقق من وجود جداول
        if not tables or len(tables) == 0:
            await processing_msg.edit_text(
                "❌ لم أتمكن من العثور على جداول في هذا الملف.\n\n"
                "تأكد أن الملف يحتوي على جداول نصية وليس صوراً."
            )
            os.unlink(tmp_path)
            return
        
        # 5. فلترة الجداول الفارغة
        valid_tables = [table for table in tables if not table.empty]
        
        if not valid_tables:
            await processing_msg.edit_text("❌ جميع الجداول المستخرجة فارغة.")
            os.unlink(tmp_path)
            return
        
        # 6. إنشاء ملف Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for i, table in enumerate(valid_tables):
                sheet_name = f"جدول {i+1}"
                # قص اسم الورقة إذا كان طويلاً
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                table.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        # 7. إرسال ملف Excel للمستخدم
        await update.message.reply_document(
            document=output,
            filename="extracted_tables.xlsx",
            caption=f"✅ تم استخراج {len(valid_tables)} جدول بنجاح!"
        )
        
        # 8. تنظيف الملفات المؤقتة
        os.unlink(tmp_path)
        await processing_msg.delete()
        
    except Exception as e:
        # في حالة حدوث خطأ
        error_message = str(e)[:200]  # نأخذ أول 200 حرف فقط
        await processing_msg.edit_text(
            f"❌ حدث خطأ أثناء المعالجة:\n\n{error_message}\n\n"
            "تأكد أن الملف PDF سليم وحاول مرة أخرى."
        )

# ------------------- الدالة الرئيسية -------------------
def main():
    if not BOT_TOKEN:
        print("❌ خطأ: لم يتم تعيين TELEGRAM_BOT_TOKEN")
        return
    
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    
    print("✅ PDF to Excel Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
