import asyncio
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

TOKEN = "8151098705:AAGKgRPB7bO-4wP-uhFypDaCu5W9kDdmmqk"

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Bot is alive!"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Xin chào! Gửi tôi 1 đoạn tiếng nước ngoài, tôi sẽ dịch sang tiếng Việt!')

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = GoogleTranslator(source='auto', target='vi').translate(text)
    await update.message.reply_text(translated)

async def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))
    await app_bot.run_polling()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_bot())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
