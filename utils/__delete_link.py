import time
import logging
import threading

logger = logging.getLogger(__name__)

def delete_link(bot, chat_id: int, message_id: int, username: str) -> bool:
    """
    Attempts to delete a message containing a URL.
    Returns True if deletion succeeded, False otherwise.
    """
    try:
        bot.delete_message(chat_id, message_id)
        logger.info(f"Successfully deleted message {message_id} from {username}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete message {message_id}: {e}")
        logger.error("Make sure the bot is an Admin with 'Delete Messages' permission in the group.")
        return False

def delete_message_delayed(bot, chat_id: int, message_id: int, delay: int = 5):
    """Deletes a message after a specified delay in seconds."""
    def target():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
            logger.info(f"Deleted message {message_id} in chat {chat_id}")
        except Exception as e:
            logger.debug(f"Could not delete message {message_id}: {e}")

    threading.Thread(target=target, daemon=True).start()
