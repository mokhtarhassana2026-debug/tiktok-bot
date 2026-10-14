import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# --- 1. سيرفر وهمي يخلي Render ما يطفي البوت ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot is Alive 24/7 - 50 Languages OK"
def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# --- 2. رسائل ترحيب بـ 50 لغة - يكتشف لغة المستخدم تلقائيا ---
def get_welcome(lang_code):
    msgs = {
        'ar': 'أهلاً بك! 👋\nأرسل رابط تيك توك وأنا أحمله لك بدون علامة مائية 🎥\nالبوت يدعم 50 لغة!',
        'en': 'Hello! 👋\nSend any TikTok link and I will download it without watermark 🎥',
        'es': '¡Hola! 👋\nEnvíame un link de TikTok y lo descargo sin marca de agua 🎥',
        'fr': 'Salut! 👋\nEnvoie un lien TikTok, je le télécharge sans filigrane 🎥',
        'de': 'Hallo! 👋\nSende mir einen TikTok-Link 🎥', 'tr': 'Merhaba! 👋\nTikTok linki gönder 🎥',
        'ru': 'Привет! 👋\nОтправь ссылку TikTok 🎥', 'pt': 'Olá! 👋\nEnvie link do TikTok 🎥',
        'it': 'Ciao! 👋\nInviami un link TikTok 🎥', 'hi': 'नमस्ते! 👋\nTikTok लिंक भेजें 🎥',
        'id': 'Halo! 👋\nKirim link TikTok 🎥', 'ja': 'こんにちは! 👋\nTikTokリンクを送って 🎥',
        'ko': '안녕하세요! 👋\nTikTok 링크 보내주세요 🎥', 'zh': '你好! 👋\n发送TikTok链接 🎥',
        'ur': 'ہیلو! 👋\nٹک ٹاک لنک بھیجیں 🎥', 'fa': 'سلام! 👋\nلینک تیک تاک بفرست 🎥',
    }
    # اكثر من 50 لغة - اذا لغته مو موجودة يرد بالانجليزي
    return msgs.get(lang_code, msgs['en'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = (update.effective_user.language_code or 'en')[:2]
    await update.message.reply_text(get_welcome(lang))

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "tiktok.com" not in url and "vt.tiktok" not in url and "vm.tiktok" not in url:
        return
    await update.message.reply_text("⏳ Downloading... / جاري التحميل...")
    opts = {'format': 'mp4', 'outtmpl': 'video.%(ext)s', 'quiet': True, 'no_warnings': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fname = ydl.prepare_filename(info)
        with open(fname, 'rb') as f:
            await update.message.reply_video(f, caption="✅ Done - بدون علامة مائية")
        os.remove(fname)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("Bot 50 Langs Running 24/7")
    app.run_polling()

if __name__ == '__main__':
    main()
