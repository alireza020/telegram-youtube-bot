import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = '7854509170:AAFXw_iKAm1F0U1fM4GGfFYJQ-P4DMDdngs'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('سلام! لینک یوتیوب رو بفرست تا برات دانلود کنم.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id
    await update.message.reply_text('در حال پردازش لینک...')

    try:
        output_path = 'downloads'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            'outtmpl': f'{output_path}/%(title).30s.%(ext)s',
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_text('دانلود کامل شد. در حال ارسال...')

        with open(filename, 'rb') as f:
            await context.bot.send_document(chat_id=chat_id, document=f)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f'❌ خطا: {e}')

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))

print("✅ ربات yt-dlp اجرا شد.")
app.run_polling()
