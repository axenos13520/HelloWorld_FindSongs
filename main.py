import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import ReplyKeyboardMarkup

def search_youtube(query: str):
    with yt_dlp.YoutubeDL({'quiet': True, "cookies": "cookies.txt"}) as ydl:
        results = ydl.extract_info(f"ytsearch1:{query}", download=False)
        video = results['entries'][0]
        return {
            "title": video['title'],
            "url": f"https://www.youtube.com/watch?v={video['id']}"
        }

searchingForSong = False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global searchingForSong

    text = update.message.text

    if text == "🔍 Поиск песни по названию / тексту":
        searchingForSong = True

        reply_keyboard = [
            ["❌ Отменить поиск"]
        ]

        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

        await update.message.reply_text("Введи название / текст песни:", reply_markup=markup)
    elif text == "❌ Отменить поиск":
        searchingForSong = False

        reply_keyboard = [
            ["🔍 Поиск песни по названию / тексту"]
        ]

        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

        await update.message.reply_text("Поиск отменён", reply_markup=markup)
    elif searchingForSong:
        song = search_youtube(text)

        if searchingForSong:
            await update.message.reply_text("🎵 " + song["title"] + "\n🔗 " + song["url"])
    elif text == "Закрыть":
        exit() 
    else:
        await update.message.reply_text("Для начала поиска выберите команду поиска")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ["🔍 Поиск песни по названию / тексту"]
    ]

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Нужна помощь в поиске песни?", reply_markup=markup)


if __name__ == '__main__':
    app = ApplicationBuilder().token("7472175298:AAEJL-RLx6NNKqq63DdiAV0tdnQeXSA1PbU").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

    print("closing...")