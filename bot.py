import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً يا مختار 👋\nارسل رابط تيك توك وانا احمله لك بدون علامة ✅")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        return
    msg = await update.message.reply_text("⏳ قاعد احمل لك... ثواني")
    try:
        opts = {"format": "best", "outtmpl": "video.%(ext)s", "quiet": True, "noplaylist": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"ما قدرت احمله: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
app.run_polling()
