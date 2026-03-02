import os
import random
import pytz
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# 🔑 ТОКЕН
TOKEN = "8604828806:AAHQ_Y_QiGo5rYUwYsT9F6QVpxvfyhOHd3U"

# ===== СПИСОК МЕМОВ =====
memes = [f for f in os.listdir() if f.endswith(".mp4")]
random.shuffle(memes)

# ===== ОТПРАВКА МЕМА =====
async def send_random_meme(message, context):
    random_meme = random.choice(memes)

    with open(random_meme, "rb") as video:
        await message.reply_video(
            video=video,
            caption=random.choice([
                "🎬 Твой мем дня 😌\n\nПриходи завтра за новым!",
                "Вот твой ежедневный дофамин ✨\n\nПриходи завтра за новым!",
                "Алгоритм выбрал это для тебя 🤖\n\nПриходи завтра за новым!",
                "Рандом решил 😏\n\nПриходи завтра за новым!"
            ])
        )

# ===== ЕЖЕДНЕВНОЕ СООБЩЕНИЕ =====
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Получить мем дня", callback_data="meme")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="☀️ Доброе утро! Пора за мемом дня!",
        reply_markup=reply_markup
    )

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Получить мем дня", callback_data="meme")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Доброе утро ☀️\nГотов(а) к мему дня?",
        reply_markup=reply_markup
    )

    # запуск ежедневного сообщения
    context.job_queue.run_daily(
        send_daily_message,
        time=time(8, 0, tzinfo=pytz.timezone("Europe/Amsterdam")),
        chat_id=update.effective_chat.id
    )

# ===== КНОПКА =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "meme":
        await send_random_meme(query.message, context)

# ===== /meme =====
async def meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_random_meme(update.message, context)

# ===== /help =====
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n"
        "/start — Запуск\n"
        "/meme — Получить случайный мем\n"
        "/help — Помощь"
    )

# ===== ЗАПУСК =====
app = (
    ApplicationBuilder()
    .token(TOKEN)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("meme", meme_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
app.add_handler(CommandHandler("meme", meme_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
