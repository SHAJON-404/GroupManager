import os
import logging
from utils.__url_validator import contains_url, is_sender_admin
from utils.__delete_link import delete_link
from utils.__warnings_then_ban import warn_then_ban
from utils.__profile_tracker import track_and_announce_profile_changes
from utils.__join_left import handle_member_join_left

logger = logging.getLogger(__name__)

# Configs
GROUP_ID = os.environ.get('GROUP_ID')
ALLOW_ADMIN_SEND_URL = os.environ.get('ALLOW_ADMIN_SEND_URL', 'True').lower() in ['true', '1', 't', 'y', 'yes']
MAX_WARNINGS = int(os.environ.get('MAX_WARNINGS', '5'))

# File paths for storing state
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WARNINGS_FILE = os.path.join(DATA_DIR, 'warnings.json')
PROFILES_FILE = os.path.join(DATA_DIR, 'user_profiles.json')

def register_handlers(bot):
    """Registers all message and event handlers for the Telegram Bot."""

    @bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
    def handle_join_leave(message):
        chat_id = message.chat.id

        # If GROUP_ID is configured, only act on that group.
        if GROUP_ID:
            try:
                configured_group_id = int(GROUP_ID)
                if chat_id != configured_group_id:
                    return
            except ValueError:
                logger.error(f"Invalid GROUP_ID in configuration: {GROUP_ID}")

        handle_member_join_left(bot, message)

    @bot.message_handler(
        func=lambda message: message.chat.type in ['group', 'supergroup'],
        content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation']
    )
    def handle_group_message(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        # If GROUP_ID is configured, only act on that group.
        if GROUP_ID:
            try:
                configured_group_id = int(GROUP_ID)
                if chat_id != configured_group_id:
                    return
            except ValueError:
                logger.error(f"Invalid GROUP_ID in configuration: {GROUP_ID}")

        # First track profile changes for all users sending messages
        track_and_announce_profile_changes(bot, message, PROFILES_FILE)

        # Check if the message contains any URL
        if contains_url(message):
            logger.info(f"URL detected in chat {chat_id} from user {username} ({user_id})")

            # Check if admins are allowed to send URLs and if the sender is an admin
            if ALLOW_ADMIN_SEND_URL and is_sender_admin(bot, chat_id, user_id):
                return

            # Try to delete the message containing the URL
            if delete_link(bot, chat_id, message.message_id, username):
                # If successfully deleted, handle warnings and bans
                warn_then_ban(bot, chat_id, user_id, username, WARNINGS_FILE, MAX_WARNINGS)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('unban_'))
    def handle_unban_callback(call):
        chat_id = call.message.chat.id
        clicker_id = call.from_user.id

        # 1. Check if the user who clicked is an admin
        if not is_sender_admin(bot, chat_id, clicker_id):
            bot.answer_callback_query(
                call.id,
                text="⚠️ Only administrators can unban users!",
                show_alert=True
            )
            return

        # 2. Extract user_id to unban
        try:
            user_to_unban = int(call.data.split('_')[1])
        except (IndexError, ValueError):
            bot.answer_callback_query(call.id, text="❌ Invalid user ID.")
            return

        # 3. Perform unban
        try:
            bot.unban_chat_member(chat_id, user_to_unban, only_if_banned=True)
            bot.answer_callback_query(call.id, text="✅ User unbanned successfully!")

            # Update the original ban message to show who unbanned the user
            clicker_name = call.from_user.username or call.from_user.first_name
            unban_announce = (
                f"✅ <b>User Unbanned!</b>\n\n"
                f"👤 <b>Unbanned by:</b> @{clicker_name}\n"
                f"ℹ️ The user has been unbanned and can join the group again."
            )
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text=unban_announce,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Failed to unban user {user_to_unban}: {e}")
            bot.answer_callback_query(
                call.id,
                text=f"❌ Failed to unban: {str(e)}",
                show_alert=True
            )
