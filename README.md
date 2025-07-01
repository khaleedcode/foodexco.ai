# 🍽️ Dining Hall Discord Bot

This Discord bot sends daily breakfast, lunch, and dinner menus from a CSV file at midnight every day.

## 🚀 Setup Instructions

### 1. Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Bot Configuration

- Rename `daily_menu_bot.py`
- Replace:
  - `DISCORD_TOKEN` in Replit secrets with your bot token
  - `CHANNEL_ID` in Replit secrets with your channel ID

### 3. Running the Bot

```bash
python daily_menu_bot.py
```

---

## 🌐 Hosting on Replit with UptimeRobot

### 🧰 On Replit:

1. Go to https://replit.com
2. Create a new Python Repl
3. Upload:
   - `daily_menu_bot.py`
   - `keep_alive.py`
   - `menu.csv`
   - `requirements.txt`
4. Go to the "Secrets" tab (🔐) and add:
   - `DISCORD_TOKEN` → your bot token
   - `CHANNEL_ID` → your channel ID (as string)

5. Run your bot!

---

### ⏰ Keep Alive with UptimeRobot

1. Copy your Replit URL (e.g. https://your-repl-name.repl.co)
2. Go to https://uptimerobot.com → Add new monitor
   - Type: HTTP
   - URL: your Replit URL
   - Interval: 5 mins
   - Name: DiningBot KeepAlive

That's it! Your bot will now post the daily menu and stay awake 24/7.
