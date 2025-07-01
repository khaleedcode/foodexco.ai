# 🚀 Slash-Command Dining Menu Bot (Railway Ready)

This version uses `/menu` and `/ping` slash commands instead of `!` prefixes.

## 📁 Files Included
- `daily_menu_bot.py` — main bot script (slash command version)
- `menu.csv` — all July meals marked "Semester Break"
- `requirements.txt` — dependencies

## 🔧 Setup on Railway
1. Go to [https://railway.app](https://railway.app)
2. Create a new project
3. Upload all files
4. Add environment variables:
   - `DISCORD_TOKEN`
   - `CHANNEL_ID`
5. Set the Start Command:
   ```
   python3 daily_menu_bot.py
   ```

## ✅ Slash Commands Available
- `/menu` → Get today's dining hall menu
- `/ping` → Check bot status
