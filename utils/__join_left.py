import html
import logging
from utils.__delete_link import delete_message_delayed

logger = logging.getLogger(__name__)

def handle_member_join_left(bot, message):
    """
    Deletes the default Telegram join/left system notifications.
    Sends a custom welcome message for new members, which is deleted after 5 seconds.
    """
    chat_id = message.chat.id

    # 1. Try to delete the default system message
    try:
        bot.delete_message(chat_id, message.message_id)
        logger.info(f"Deleted default system message {message.message_id} in chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to delete default system message: {e}")
        logger.error("Make sure the bot has 'Delete Messages' admin permission in the group.")

    # 2. If it's a join event, send a custom welcome message
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            # Skip welcoming bots
            if new_member.is_bot:
                continue

            first_name = new_member.first_name
            username = new_member.username

            if username:
                user_mention = f"@{username}"
            else:
                user_mention = f"<b>{html.escape(first_name)}</b>"

            welcome_text = (
                f"👋 <b>Welcome to the group, {user_mention}!</b>\n"
                f"Please read the rules and enjoy your stay. 😊"
            )

            try:
                welcome_msg = bot.send_message(chat_id, welcome_text, parse_mode='HTML')
                logger.info(f"Sent welcome message to user {new_member.id} in chat {chat_id}")
                
                # Auto-delete welcome message after 5 seconds to keep group clean
                delete_message_delayed(bot, chat_id, welcome_msg.message_id, delay=5)
            except Exception as e:
                logger.error(f"Failed to send welcome message: {e}")
