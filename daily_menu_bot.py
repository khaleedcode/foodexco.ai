import discord
from discord.ext import tasks, commands
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import os
import logging
logging.basicConfig(level=logging.DEBUG)

# === CONFIG ===
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
CSV_FILE = 'menu.csv'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_today_meals():
    today_str = datetime.now().strftime('%Y-%m-%d')
    df = pd.read_csv(CSV_FILE)
    today_df = df[df['Date'] == today_str]

    if today_df.empty:
        return f"No menu found for {today_str}."

    meals = []
    for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
        meal_texts = today_df[today_df['Meal'].str.lower() == meal_type.lower()]['Menu'].tolist()
        if meal_texts:
            meals.append(f"**{meal_type}:**\n{meal_texts[0]}")
        else:
            meals.append(f"**{meal_type}:** No menu available.")

    return f"🍽️ **Dining Hall Menu for {today_str}** 🍽️\n\n" + "\n\n".join(meals)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    daily_menu.start()

@tasks.loop(hours=24)
async def daily_menu():
    now = datetime.now()
    # Set the target time to 01:10:05
    future = now.replace(hour=1, minute=10, second=5, microsecond=0)
    if now > future:
        # If we've passed the target time today, schedule for tomorrow
        future += timedelta(days=1)
    await asyncio.sleep((future - now).total_seconds())

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        menu_message = get_today_meals()
        await channel.send(menu_message)

@bot.command(name='testmenu')
async def test_menu(ctx):
    menu_message = get_today_meals()
    await ctx.send(menu_message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
