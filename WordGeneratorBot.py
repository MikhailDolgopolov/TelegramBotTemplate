import logging
from warnings import filterwarnings

import urllib3
from telegram import Update
from telegram.ext import (
    Application,
    PicklePersistence,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackContext, filters, CallbackQueryHandler)
from telegram.warnings import PTBUserWarning

from helpers import read_json

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.ERROR)


# Telegram bot API token
TOKEN = read_json("secrets.json")["telegram-token"]


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет!')


async def reply(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Извините, ничего больше я не умею.')


def main() -> None:
    persistence = PicklePersistence(filepath='bot_persitence', update_interval=5)
    application = Application.builder().token(TOKEN).persistence(persistence).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(".{1,}"), reply))


    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()