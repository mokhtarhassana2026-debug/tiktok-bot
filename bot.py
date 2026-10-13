import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا والله يا مختار! 👋\nارسل لي رابط تيك توك وانا احمله لك بدون علامة")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "http" not in url:
        return
    msg = await update.message.reply_text("⏳ جاري التحميل...")
    try:
        opts = {'format': 'best', 'outtmpl': 'video.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f, caption="✅ تفضل")
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        logging.error(e)
        await msg.edit_text(f"❌ ما قدرت احمل: {e}")

def main():
    if not TOKEN:
        print("BOT_TOKEN not found!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
