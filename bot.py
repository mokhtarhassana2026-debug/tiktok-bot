import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا يا مختار! ارسل رابط تيك توك")

async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "tiktok.com" not in url:
        return
    m = await update.message.reply_text("⏳ جاري التحميل...")
    try:
        opts = {"format": "best", "outtmpl": "vid.%(ext)s", "quiet": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fn = ydl.prepare_filename(info)
        with open(fn, 'rb') as f:
            await update.message.reply_video(video=f)
        os.remove(fn)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"خطأ: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dl))
    app.run_polling()
