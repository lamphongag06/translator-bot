import os
import logging
from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ["BOT_TOKEN"]

def auto_translate(text):
    detection = translate_client.detect_language(text)
    source_lang = detection['language']

    if source_lang == 'vi':
        target_lang = 'en'
    else:
        target_lang = 'vi'

    result = translate_client.translate(text, target_language=target_lang, format_='text')
    return result['translatedText']

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_text = update.message.text or update.message.caption
    if not original_text:
        return

    translated = auto_translate(original_text)
    await update.message.reply_text(translated, parse_mode="HTML")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.FORWARDED, handle_message))
    app.run_polling()
