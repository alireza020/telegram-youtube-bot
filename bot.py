import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")  # یا می‌تونی مستقیماً مقدار توکن رو اینجا بذاری

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک یوتیوب رو بفرست تا صدای MP3 برات بفرستم.")

async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("در حال دانلود صدا از یوتیوب...")

    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title).30s.%(ext)s',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"

        with open(filename, 'rb') as audio:
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio, title=info.get("title", "Audio"))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_mp3))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
