from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
import os

TOKEN = "7996761666:AAESN7ometeIUPulPwZ4RIuKKJENx6SShks"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک یوتیوب بفرست تا ویدیو mp4 دانلود و برات بفرستم.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text("لطفا لینک ویدیو رو بعد از /download بفرست.")
        return

    msg = await update.message.reply_text("در حال دانلود ویدیو...")

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("دانلود تموم شد، دارم ارسال می‌کنم...")

        with open(filename, 'rb') as video:
            await update.message.reply_video(video)

        os.remove(filename)

    except Exception as e:
        await msg.edit_text(f"مشکل پیش اومد: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
