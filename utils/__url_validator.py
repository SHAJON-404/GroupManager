import re
import logging

logger = logging.getLogger(__name__)

# Regex to detect links. Catches:
# 1. Links starting with http://, https://, or www.
# 2. Links without protocol/www but using common TLDs (e.g. google.com, t.me/username) to avoid false positives on filenames (like main.py)
URL_REGEX = re.compile(
    r'(?:https?://|www\.)\S+'
    r'|[a-zA-Z0-9.-]+\.(?:com|net|org|xyz|info|co|io|me|cc|tv|link|in|dev|biz|us|uk|ru|ca|de|fr|app|online|site|tech|store|top|edu|gov)\b(?:/\S*)?',
    re.IGNORECASE
)

def contains_url(message) -> bool:
    """Checks if a message contains a URL using Telegram entities or regex search."""
    # 1. Check text entities (for plain text messages)
    if message.entities:
        for entity in message.entities:
            if entity.type in ['url', 'text_link']:
                return True

    # 2. Check caption entities (for photos, videos, etc.)
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.type in ['url', 'text_link']:
                return True

    # 3. Fallback regex search on message text
    if message.text and URL_REGEX.search(message.text):
        return True

    # 4. Fallback regex search on message caption
    if message.caption and URL_REGEX.search(message.caption):
        return True

    return False

def is_sender_admin(bot, chat_id: int, user_id: int) -> bool:
    """Checks if the user is an administrator or creator of the chat."""
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking admin status for user {user_id} in chat {chat_id}: {e}")
        return False
