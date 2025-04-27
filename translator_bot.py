from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

# Dán TOKEN bot của bạn vào đây
TOKEN = "8151098705:AAGKgRPB7bO-4wP-uhFypDaCu5W9kDdmmqk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Xin chào! Gửi tôi 1 đoạn tiếng nước ngoài, tôi sẽ dịch sang tiếng Việt!')

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = GoogleTranslator(source='auto', target='vi').translate(text)
    await update.message.reply_text(translated)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

    print("Bot is running...")  # Thêm dòng này để báo bot đã chạy
    app.run_polling()

if __name__ == '__main__':
    main()
