import html
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.storage import load_json, save_json
from utils.__delete_link import delete_message_delayed

logger = logging.getLogger(__name__)

def warn_then_ban(bot, chat_id: int, user_id: int, username: str, warnings_file: str, max_warnings: int):
    """
    Increments user warnings. Bans the user if the warnings threshold is reached.
    Otherwise, sends a temporary self-deleting warning message.
    """
    key = f"{chat_id}_{user_id}"
    warnings_db = load_json(warnings_file, {})
    current_warnings = warnings_db.get(key, 0) + 1

    if current_warnings >= max_warnings:
        # Reset warning count
        if key in warnings_db:
            del warnings_db[key]
        save_json(warnings_file, warnings_db)

        # Ban user
        try:
            bot.ban_chat_member(chat_id, user_id)
            logger.info(f"Banned user {username} ({user_id}) from chat {chat_id} (exceeded warnings limit)")

            ban_text = (
                f"🚫 <b>User Banned!</b>\n\n"
                f"👤 <b>User:</b> {html.escape(username)} (ID: {user_id})\n"
                f"⚠️ <b>Reason:</b> Sent link and exceeded URL warning limit ({max_warnings}/{max_warnings})."
            )
            
            # Create inline keyboard for unbanning
            markup = InlineKeyboardMarkup()
            unban_btn = InlineKeyboardButton(text="🔓 Unban User", callback_data=f"unban_{user_id}")
            markup.add(unban_btn)

            bot.send_message(chat_id, ban_text, parse_mode='HTML', reply_markup=markup)
        except Exception as ban_err:
            logger.error(f"Failed to ban user {user_id}: {ban_err}")
            logger.error("Make sure the bot has 'Ban Users' admin permission in the group.")
            
            # Fallback message
            warning_text = (
                f"⚠️ @{html.escape(username)}, you reached the warning limit "
                f"({current_warnings}/{max_warnings}) but I failed to ban you. (Check my admin permissions!)"
            )
            bot.send_message(chat_id, warning_text)
    else:
        # Update warning count
        warnings_db[key] = current_warnings
        save_json(warnings_file, warnings_db)

        # Send warning message
        warning_text = (
            f"⚠️ @{html.escape(username)}, sharing links is not allowed in this group!\n"
            f"<b>Warning:</b> {current_warnings}/{max_warnings}"
        )
        try:
            warning_msg = bot.send_message(chat_id, warning_text, parse_mode='HTML')
            # Auto-delete warning message after 5 seconds
            delete_message_delayed(bot, chat_id, warning_msg.message_id, delay=5)
        except Exception as warn_err:
            logger.error(f"Failed to send warning message: {warn_err}")
