import asyncio
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

TOKEN = "8151098705:AAH3SRpc4AbU8EBnP58We_YOdPA94qvyywc"

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Bot is alive!"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Xin chào! Gửi tôi 1 đoạn tiếng nước ngoài, tôi sẽ dịch sang tiếng Việt!')

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ưu tiên lấy text nếu có
    text = update.message.text

    # Nếu không có text, kiểm tra caption (trong trường hợp chuyển tiếp media có chú thích)
    if not text and update.message.caption:
        text = update.message.caption

    if text:
        try:
            translated = GoogleTranslator(source='auto', target='vi').translate(text)
            await update.message.reply_text(translated)
        except Exception as e:
            await update.message.reply_text(f"Đã xảy ra lỗi khi dịch: {str(e)}")
    else:
        await update.message.reply_text("Không tìm thấy nội dung văn bản để dịch.")

@app.on_event("startup")
async def startup_event():
    global app_bot
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(MessageHandler(filters.TEXT | filters.Caption(), translate_message))

    await app_bot.initialize()
    await app_bot.start()
    asyncio.create_task(app_bot.updater.start_polling())

@app.on_event("shutdown")
async def shutdown_event():
    await app_bot.stop()
    await app_bot.shutdown()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
