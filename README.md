# Telegram URL Remover Bot (Group Helper)

A modern Telegram Bot built in Python that monitors group chats, removes messages containing links/URLs, automatically warns and bans repeat offenders, announces user profile changes (name/username) in real-time, deletes default system join/leave notifications, and welcomes new members.

## Features

- **Link / URL Removal:** Scans text messages and media captions (images, videos, etc.) for links using Telegram's built-in message entities and regex fallback.
- **Admin Exemption:** Admins and creators can bypass link removal rules (optional and configurable).
- **Warning Count & Auto-Ban:** Tracks warnings persistently per user in a lightweight JSON database. If a user exceeds the warning threshold, they are automatically banned from the group.
- **Self-Cleaning Warnings:** To avoid cluttering the group chat, warning notices automatically delete themselves after 5 seconds.
- **Profile Change Announcements:** Detects and posts a message if a group member changes their profile name or Telegram `@username`.
- **System Notification Cleanup:** Automatically deletes default Telegram "user joined" and "user left" system messages.
- **Custom Welcome Messages:** Sends a clean welcome message greeting new members by name/username.

---

## File Structure

```text
GroupHelper/
├── utils/
│   ├── __init__.py
│   ├── __handlers.py            # Event/Message Handlers registry logic
│   ├── __delete_link.py         # Link deletion implementation
│   ├── __warnings_then_ban.py   # Warning increments & banning implementation
│   ├── __profile_tracker.py     # Profile tracking implementation
│   ├── __url_validator.py       # Message entities and regex scanning
│   ├── __join_left.py           # Handles deletion of join/left alerts + welcomes users
│   └── storage.py               # JSON storage loaders and savers
├── .dockerignore                # Specifies files ignored in Docker builds
├── .gitignore                   # Specifies files ignored in Git version control
├── .env                         # Configuration & credentials
├── docker-compose.yml           # Docker Compose services definition
├── Dockerfile                   # Docker build instructions
├── main.py                      # Pure bot bootstrapper and polling runner (minimal script)
├── requirements.txt             # Python packages dependencies list
├── warnings.json                # Persistent warnings database (auto-generated)
├── user_profiles.json           # Saved user profiles database (auto-generated)
└── README.md                    # This documentation
```

---

## Prerequisites

- Python 3.8 or higher, **OR** Docker installed on your system.
- A Telegram Bot token (from [@BotFather](https://t.me/BotFather))

---

## Local Installation

1. **Clone the repository** (or navigate to the workspace directory).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create or modify the `.env` file in the root directory:

```env
# Your Telegram Bot Token obtained from @BotFather
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# (Optional) Restrict the bot to only operate in a specific group.
# Leave empty or omit to monitor all groups where the bot is added as an administrator.
GROUP_ID=-100XXXXXXXXXX

# Configuration flags
ALLOW_ADMIN_SEND_URL=True
MAX_WARNINGS=5
DEBUG=True
```

---

## Setting up in Telegram

1. Add your bot to the target group.
2. Promote the bot to **Administrator**.
3. Ensure the bot is granted the following permissions:
   - **Delete Messages** (required to remove URLs, warnings, and system join/left notifications)
   - **Ban Users** (required to perform auto-bans)

---

## Running the Bot

### Option 1: Standard Python Run
Run the bot script using Python:
```bash
python main.py
```

### Option 2: Run with Docker Compose (Recommended)
Before running Docker Compose, ensure you create empty state tracking files so that Docker mounts them as files (not directories):
```bash
# On Linux/macOS
touch warnings.json user_profiles.json

# On Windows (PowerShell)
New-Item -Path . -Name "warnings.json" -ItemType "file" -Force
New-Item -Path . -Name "user_profiles.json" -ItemType "file" -Force
```

To build and start the bot service in the background:
```bash
docker compose up -d --build
```

To view logs:
```bash
docker compose logs -f
```

To stop the bot service:
```bash
docker compose down
```
