import os
import sys
import logging
from dotenv import load_dotenv
import telebot
from utils.__handlers import register_handlers

# Load environment variables first so configurations are available
load_dotenv()

DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't', 'y', 'yes']

# Configure logging based on DEBUG mode
if DEBUG:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(
        level=logging.CRITICAL,
        handlers=[
            logging.NullHandler()
        ]
    )

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logger.critical("BOT_TOKEN is missing in the .env file!")
    raise ValueError("BOT_TOKEN is not set in the environment.")

if __name__ == '__main__':
    logger.info("Bot starting up...")
    
    # Initialize the bot
    bot = telebot.TeleBot(BOT_TOKEN)
    
    # Register handlers from the handlers module
    register_handlers(bot)

    try:
        logger.info("Starting bot polling (infinity_polling)... Press Ctrl+C to exit.")
        bot.infinity_polling(timeout=60, long_polling_timeout=20)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Keyboard interrupt received. Shutting down bot gracefully...")
        try:
            bot.stop_polling()
        except Exception:
            pass
        sys.exit(0)
    except Exception as err:
        logger.critical(f"Bot terminated due to an unexpected error: {err}")
        sys.exit(1)