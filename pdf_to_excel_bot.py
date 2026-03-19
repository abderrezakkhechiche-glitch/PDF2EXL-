import os
import pandas as pd
import tabula
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
import io
import tempfile

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 **مرحباً! أنا بوت استخراج الجداول من PDF**\n\n"
        "أرسل لي ملف PDF وسأقوم باستخراج الجداول منه وتحويلها إلى Excel.\n\n"
        "✅ يدعم استخراج جداول متعددة من نفس الملف.\n"
        "✨ **أرسل الملف الآن**",
        parse_mode='Markdown'
    )

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    processing_msg = await update.message.reply_text("🔄 جاري استخراج الجداول...")
    
    try:
        file = await update.message.document.get_file()
        pdf_bytes = io.BytesIO()
        await file.download_to_memory(pdf_bytes)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes.getvalue())
            tmp_path = tmp.name
        
        tables = tabula.read_pdf(tmp_path, pages='all', multiple_tables=True)
        
        if not tables or len(tables) == 0:
            await processing_msg.edit_text("❌ لم أتمكن من العثور على جداول.")
            os.unlink(tmp_path)
            return
        
        valid_tables = [table for table in tables if not table.empty]
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for i, table in enumerate(valid_tables):
                sheet_name = f"جدول {i+1}"
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                table.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        await update.message.reply_document(
            document=output,
            filename="extracted_tables.xlsx",
            caption=f"✅ تم استخراج {len(valid_tables)} جدول بنجاح!"
        )
        
        os.unlink(tmp_path)
        await processing_msg.delete()
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ خطأ: {str(e)[:100]}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.run_polling()

if __name__ == "__main__":
    main()