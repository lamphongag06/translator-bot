import logging
from fastapi import FastAPI, Request, HTTPException
import uvicorn
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
import pytesseract
from PIL import Image
import aiohttp
import io
import asyncio

# Cấu hình logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot token
TELEGRAM_TOKEN = "8151098705:AAH3SRpc4AbU8EBnP58We_YOdPA94qvyywc"

app = FastAPI()
bot_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Xử lý text message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        detected_lang = GoogleTranslator(source='auto', target='en').translate(text)
        if detected_lang.lower() == text.lower():
            translated_text = GoogleTranslator(source='vi', target='en').translate(text)
        else:
            translated_text = GoogleTranslator(source='auto', target='vi').translate(text)
        await update.message.reply_text(translated_text)
    except Exception as e:
        logger.error(f"Lỗi khi dịch văn bản: {e}")
        await update.message.reply_text(f"Lỗi dịch: {str(e)}")

# Xử lý image message
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        async with aiohttp.ClientSession() as session:
            async with session.get(file.file_path) as resp:
                img_data = await resp.read()
                img = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(img)
                if not text.strip():
                    await update.message.reply_text("Không tìm thấy văn bản trong ảnh.")
                    return
                translated_text = GoogleTranslator(source='auto', target='vi').translate(text)
                await update.message.reply_text(translated_text)
    except Exception as e:
        logger.error(f"Lỗi khi xử lý ảnh: {e}")
        await update.message.reply_text(f"Lỗi OCR: {str(e)}")

# Đăng ký các handler
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
bot_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# Trình xử lý lỗi tổng quát cho FastAPI
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Lỗi chưa được xử lý: {exc}")
    return {"message": f"Có lỗi xảy ra: {str(exc)}"}

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Khởi động Telegram bot...")
        await bot_app.initialize()
        await bot_app.start()
        await bot_app.updater.start_polling()
        logger.info("Telegram bot đã khởi động thành công.")
    except Exception as e:
        logger.error(f"Lỗi khi khởi động bot: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi khởi động bot: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        logger.info("Tắt Telegram bot...")
        await bot_app.updater.stop()
        await bot_app.stop()
        await bot_app.shutdown()
        logger.info("Telegram bot đã tắt thành công.")
    except Exception as e:
        logger.error(f"Lỗi khi tắt bot: {e}")

@app.get("/")
async def root():
    return {"message": "Bot is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)