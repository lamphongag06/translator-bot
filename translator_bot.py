import logging
import os
import re
import io
import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Replace with your new token
TOKEN = "7574715872:AAEZ4b7cRadrisYuT8IZs2t7sWRwWChVIas"

app = FastAPI()

# Initialize the bot application
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def detect_language(text):
    return GoogleTranslator(source='auto', target='en').detect(text)

def translate_text(text):
    try:
        detected_lang = detect_language(text)
        if detected_lang == "vi":
            return GoogleTranslator(source='vi', target='en').translate(text)
        else:
            return GoogleTranslator(source='auto', target='vi').translate(text)
    except Exception as e:
        return f"Lỗi dịch: {str(e)}"

def preserve_format_and_translate(message: str) -> str:
    code_blocks = re.findall(r"```.*?```", message, flags=re.DOTALL)
    inline_codes = re.findall(r"`[^`]*`", message)

    placeholders = {}
    for i, block in enumerate(code_blocks):
        key = f"[[CODE_BLOCK_{i}]]"
        message = message.replace(block, key)
        placeholders[key] = block
    for i, code in enumerate(inline_codes):
        key = f"[[INLINE_CODE_{i}]]"
        message = message.replace(code, key)
        placeholders[key] = code

    translated = translate_text(message)

    for key, value in placeholders.items():
        translated = translated.replace(key, value)

    return translated

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    message = update.message

    # Handle photo messages with captions (image + text)
    if message.photo:
        caption = message.caption or ""
        translated_caption = translate_text(caption) if caption else ""
        await message.reply_text(f"Dịch chú thích:
{translated_caption}" if translated_caption else "Ảnh không có chú thích.")

        # Try OCR to extract text from image
        try:
            photo_file = await message.photo[-1].get_file()
            photo_bytes = await photo_file.download_as_bytearray()
            image = Image.open(io.BytesIO(photo_bytes))
            text_from_image = pytesseract.image_to_string(image)
            if text_from_image.strip():
                translated_text = translate_text(text_from_image)
                await message.reply_text(f"📷 Văn bản từ ảnh:
{text_from_image}

🌐 Dịch:
{translated_text}")
        except Exception as e:
            await message.reply_text("Không thể trích xuất văn bản từ ảnh.")
        return

    # Handle text messages including forwarded ones
    if message.text:
        translated = preserve_format_and_translate(message.text)
        await message.reply_text(translated)

telegram_app.add_handler(MessageHandler(filters.ALL, handle_message))

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telegram_app.run_polling())

@app.get("/")
def read_root():
    return {"status": "Bot is running."}
