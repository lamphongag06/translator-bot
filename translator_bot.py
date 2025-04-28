
import logging
from fastapi import FastAPI, Request
import uvicorn
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
import pytesseract
from PIL import Image
import aiohttp
import io

# Telegram bot token
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

app = FastAPI()
bot_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Xử lý text message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        detected_lang = GoogleTranslator(source='auto', target='en').translate(text)
        if detected_lang.lower() == text.lower():
            translated_text = GoogleTranslator(source='vi', target='en').translate(text)
        else:
            translated_text = GoogleTranslator(source='auto', target='vi').translate(text)
        await update.message.reply_text(translated_text)
    except Exception as e:
        await update.message.reply_text(f"Lỗi dịch: {e}")

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
                translated_text = GoogleTranslator(source='auto', target='vi').translate(text)
                await update.message.reply_text(translated_text)
    except Exception as e:
        await update.message.reply_text(f"Lỗi OCR: {e}")

bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
bot_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

@app.on_event("startup")
async def startup_event():
    bot_app.create_task(bot_app.start())

@app.get("/")
async def root():
    return {"message": "Bot is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    