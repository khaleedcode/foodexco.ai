import discord
from discord.ext import tasks
from discord import app_commands
import pandas as pd
from datetime import datetime, timedelta, timezone
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CSV_FILE = "menu.csv"

# Set timezone to GMT+8
tz = timezone(timedelta(hours=8))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def get_meals_for(date_str):
    df = pd.read_csv(CSV_FILE)
    date_df = df[df['Date'] == date_str]

    if date_df.empty:
        return f"No menu found for {date_str}."

    meals = []
    for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
        meal_texts = date_df[date_df['Meal'].str.lower() == meal_type.lower()]['Menu'].tolist()
        if meal_texts:
            meals.append(f"**{meal_type}:**\n{meal_texts[0]}")
        else:
            meals.append(f"**{meal_type}:** No menu available.")

    return f"🍽️ **Dining Hall Menu for {date_str}** 🍽️\n\n" + "\n\n".join(meals)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await tree.sync()
    daily_menu.start()

@tree.command(name="ping", description="Check if the bot is alive")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

@tree.command(name="menu", description="Show today's dining hall menu")
async def menu_command(interaction: discord.Interaction):
    today_str = datetime.now(tz).strftime('%Y-%m-%d')
    await interaction.response.send_message(get_meals_for(today_str))

@tree.command(name="menu_tomorrow", description="Show tomorrow's dining hall menu")
async def menu_tomorrow_command(interaction: discord.Interaction):
    tomorrow_str = (datetime.now(tz) + timedelta(days=1)).strftime('%Y-%m-%d')
    await interaction.response.send_message(get_meals_for(tomorrow_str))

@tasks.loop(hours=24)
async def daily_menu():
    now = datetime.now(tz)
    future = now.replace(hour=21, minute=30, second=00, microsecond=0)
    if now > future:
        future = future + timedelta(days=1)
    await asyncio.sleep((future - now).seconds)

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        today_str = datetime.now(tz).strftime('%Y-%m-%d')
        await channel.send(get_meals_for(today_str))

client.run(TOKEN)
