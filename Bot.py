import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", 0))

if not TOKEN or not ADMIN_CHAT_ID:
    raise ValueError("Не заданы TOKEN или ADMIN_CHAT_ID в переменных окружения")

SECRET_STRING = "MDAxMDEwMTEwMTExMDExMDAxMDAwMTAxMDEwMTExMTEwMDEwMTAxMTAwMTExMTEwMDAxMDAwMTEwMTAxMTExMTAxMTEwMDAwMDEwMDEwMDAwMTExMDExMTAxMDExMTExMDExMTExMDAwMDEwMDAxMDAxMTExMDExMDExMDAwMDAwMDEwMTAxMTAxMTAwMDAxMDAxMDEwMTEwMDExMTEwMDAwMTAxMDExMDAxMTExMTAwMTAwMDAxMDAxMDAwMTEwMDAxMDEwMTEwMDEwMDEwMTAxMTEwMTExMDEwMTExMTEwMDEwMTAxMTAwMTExMTEwMDExMTEwMTEwMTEwMDEwMDAwMTAxMDExMDExMTAxMTAwMTAwMDAwMTAxMTAwMDAwMDExMTAwMDEwMTExMDExMDAxMDAwMDEwMDEwMDEwMDE="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        "Привет! Я бот, который хранит секретный шифр.\n"
        "Отправь /get, чтобы получить его.\n\n"
        "Если хочешь разгадать шифр — просто пиши свои варианты, они уйдут автору."
    )

async def get_secret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вот твой шифр:\n\n{SECRET_STRING}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text



    name = user.full_name
    username = f"@{user.username}" if user.username else "нет username"
    user_id = user.id

    report = (
        f"✉️ Новое сообщение от {name} ({username}, ID: {user_id}):\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{text}"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=report)
        logger.info(f"Переслано сообщение от {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке админу: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_secret))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен и начинает polling...")
    app.run_polling()

if __name__ == "__main__":
    main()