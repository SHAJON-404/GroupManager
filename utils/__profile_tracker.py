import html
import logging
from utils.storage import load_json, save_json
from utils.__delete_link import delete_message_delayed

logger = logging.getLogger(__name__)

def track_and_announce_profile_changes(bot, message, profiles_file: str):
    """
    Compares the sender's current name and username against saved records.
    Announces changes in the group and updates records.
    The announcement is auto-deleted after 5 seconds.
    """
    user = message.from_user
    if not user or user.is_bot:
        return

    user_id = str(user.id)
    chat_id = message.chat.id

    current_first = user.first_name or ""
    current_last = user.last_name or ""
    current_username = user.username or ""

    current_full_name = f"{current_first} {current_last}".strip()
    current_handle = f"@{current_username}" if current_username else "No Username"

    profiles_db = load_json(profiles_file, {})

    if user_id in profiles_db:
        old_profile = profiles_db[user_id]
        old_first = old_profile.get("first_name", "")
        old_last = old_profile.get("last_name", "")
        old_username = old_profile.get("username", "")

        old_full_name = f"{old_first} {old_last}".strip()
        old_handle = f"@{old_username}" if old_username else "No Username"

        changes = []

        # Check name change
        if current_full_name != old_full_name:
            changes.append(f"Name: '<i>{html.escape(old_full_name)}</i>' ➡️ '<b>{html.escape(current_full_name)}</b>'")

        # Check username change
        if current_username != old_username:
            changes.append(f"Username: <i>{html.escape(old_handle)}</i> ➡️ <b>{html.escape(current_handle)}</b>")

        if changes:
            user_ref = f"@{current_username}" if current_username else current_full_name
            announcement = (
                f"🔔 <b>Profile Change Detected for {html.escape(user_ref)}!</b>\n\n"
                + "\n".join([f"• {c}" for c in changes])
            )
            try:
                announcement_msg = bot.send_message(chat_id, announcement, parse_mode='HTML')
                logger.info(f"Announced profile change for user {user_id} in chat {chat_id}")
                
                # Auto-delete profile change alert after 5 seconds
                delete_message_delayed(bot, chat_id, announcement_msg.message_id, delay=5)
            except Exception as e:
                logger.error(f"Failed to send profile change announcement: {e}")

    # Save current profile
    profiles_db[user_id] = {
        "first_name": current_first,
        "last_name": current_last,
        "username": current_username
    }
    save_json(profiles_file, profiles_db)
