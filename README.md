# Telegram URL Remover Bot (Group Helper)

A modern, highly-modular Telegram Bot built in Python that keeps your group chats clean and secure. It automatically removes messages containing links/URLs, implements a persistent warning counter with auto-banning, provides interactive inline unban keyboards for administrators, announces user name/username profile changes in real-time, removes default user join/leave system alerts, and greets new members. 

For maximum chat cleanliness, all temporary bot alerts automatically disappear after 5 seconds!

---

## 🚀 Key Features

- **Protocol-less Link/URL Detection:** 
  - Detects standard URLs (e.g., `https://google.com`, `www.example.com`).
  - Catches protocol-less links (e.g., `google.com`, `t.me/username`) using a curated fallback registry of common Top Level Domains (TLDs).
  - Designed to prevent false-positives on programming filenames (e.g., `main.py`, `storage.py`, `settings.json`) or general abbreviations (e.g., `e.g.`, `i.e.`).
- **Admin Exemption Bypass:** Optional config bypass allowing administrators and creators to send URLs.
- **Warning System & Auto-Banning:** 
  - Tracks user violations persistently inside a lightweight JSON database (`warnings.json`).
  - Automatically bans users from the group upon exceeding the configurable warning threshold (`MAX_WARNINGS`).
- **Interactive Unban Keyboard (Admins Only):** 
  - Banned notification messages feature a `🔓 Unban User` inline button.
  - If a non-admin clicks it, the bot flags a custom Telegram error alert.
  - If an admin clicks it, the bot unbans the member and updates the message in-place to state `✅ User Unbanned! Unbanned by: @username` (removing the keyboard to keep the chat clean).
- **Self-Cleaning Messaging (5s Delay):** 
  - To prevent chat pollution, **all temporary messages** sent by the bot (link warning notices, member welcome messages, and profile change alerts) automatically delete themselves after exactly **5 seconds**.
- **System Notification Cleanup:** Deletes default Telegram system join and leave alerts (e.g., `"User joined the group"` or `"User left the group"`).
- **Profile Change Tracker:** Compares member usernames and names against cached records (`user_profiles.json`) in real-time, announcing changes in the group.
- **Graceful Shutdown:** Handles `KeyboardInterrupt`/`SystemExit` (Ctrl+C) by immediately stopping long-polling, closing open connections, and exiting cleanly.

---

## 📁 File Structure

```text
GroupHelper/
├── utils/
│   ├── __init__.py
│   ├── __handlers.py            # Directs and maps bot event listeners
│   ├── __delete_link.py         # Standard and delayed message deletion utilities
│   ├── __warnings_then_ban.py   # Warning database tracker, banning, and inline unban keyboard
│   ├── __profile_tracker.py     # Username/Name change comparison logic
│   ├── __url_validator.py       # Message entities and protocol-less URL regex validator
│   ├── __join_left.py           # Handles join/left notification deletion + greets new members
│   └── storage.py               # Safe JSON persistent database helpers
├── .dockerignore                # Specifies files ignored in Docker builds
├── .gitignore                   # Prevents tracking virtual env, configs, and json databases in Git
├── .env                         # Environment credentials and configurations
├── docker-compose.yml           # Docker Compose services configuration
├── Dockerfile                   # Docker image blueprint instructions
├── main.py                      # Pure bot bootstrapper and polling runner (minimal script)
├── requirements.txt             # Python packages dependencies list
├── warnings.json                # User warning database (auto-generated)
├── user_profiles.json           # Cached user profiles database (auto-generated)
└── README.md                    # This documentation
```

---

## 🛠️ Prerequisites

- Python 3.8 or higher, **OR** Docker installed on your system.
- A Telegram Bot token (obtainable from [@BotFather](https://t.me/BotFather))

---

## 💻 Local Installation

1. Clone or navigate to the project directory:
   ```bash
   cd GroupHelper
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Create or modify the `.env` file in the root directory:

```env
# Your Telegram Bot Token obtained from @BotFather
BOT_TOKEN=7528061691:AAHyqGV-6oY76sd7ZuJGJx1ZveIARCNyI3k

# (Optional) Restrict the bot to only operate in a specific group.
# Leave empty or omit to monitor all groups where the bot is added as an administrator.
GROUP_ID=-1003921732317

# Configuration flags
ALLOW_ADMIN_SEND_URL=True
MAX_WARNINGS=5
DEBUG=True
```

---

## 🤖 Group Permissions Setup

To ensure all functions operate correctly:
1. Add the bot to your Telegram Group.
2. Promote the bot to **Administrator**.
3. Enable the following admin permissions:
   - **Delete Messages** (required to remove URLs, system alerts, and auto-delete warnings)
   - **Ban Users** (required to enforce bans and unban members via the inline button)

---

## 🏃 Running the Bot

### Option 1: Standard Python Run
Run the bot script directly:
```bash
python main.py
```
*Press `Ctrl+C` to terminate the bot cleanly.*

### Option 2: Docker Compose (Recommended)
Create the persistent json databases on the host system first to prevent Docker from creating directories:
```bash
# On Linux/macOS
touch warnings.json user_profiles.json

# On Windows (PowerShell)
New-Item -Path . -Name "warnings.json" -ItemType "file" -Force
New-Item -Path . -Name "user_profiles.json" -ItemType "file" -Force
```

Build and run in detached mode:
```bash
docker compose up -d --build
```

View logs:
```bash
docker compose logs -f
```

Stop the containers:
```bash
docker compose down
```
