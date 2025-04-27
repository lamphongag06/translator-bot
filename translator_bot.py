from flask import Flask
import threading
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

# Thay TOKEN bot của bạn vào đây
TOKEN = "8151098705:AAGKgRPB7bO-4wP-uhFypDaCu5W9kDdmmqk"

# Hàm khởi chạy bot Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Xin chào! Gửi tôi 1 đoạn tiếng nước ngoài, tôi sẽ dịch sang tiếng Việt!')

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = GoogleTranslator(source='auto', target='vi').translate(text)
    await update.message.reply_text(translated)

def run_bot():
    # Cực kỳ quan trọng: tạo event loop mới cho thread
    asyncio.set_event_loop(asyncio.new_event_loop())

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))
    app.run_polling()

# Flask server để giữ cổng 8080 cho Render
server = Flask('')

@server.route('/')
def home():
    return "Bot is alive!"

if __name__ == "__main__":
    # Chạy bot Telegram trên thread phụ
    threading.Thread(target=run_bot).start()
    # Flask giữ main thread để Render thấy PORT 8080
    server.run(host='0.0.0.0', port=8080)
