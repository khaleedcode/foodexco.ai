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

# Use GMT+8
tz = timezone(timedelta(hours=8))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def get_meals_for(date_str):
    try:
        df = pd.read_csv(CSV_FILE)
        date_df = df[df['Date'] == date_str]

        if date_df.empty:
            return f"The latest menu has not been sent yet. Please check back soon."

        weekday = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
        meals = []
        for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
            meal_texts = date_df[date_df['Meal'].str.lower() == meal_type.lower()]['Menu'].tolist()
            if meal_texts:
                meals.append(f"**{meal_type}:**\n{meal_texts[0]}")
            else:
                meals.append(f"**{meal_type}:** No menu available.")

        return f"🍽️ **Dining Hall Menu for {date_str} ({weekday})** 🍽️\n\n" + "\n\n".join(meals)

    except Exception:
        return "An error occurred while fetching the menu. Please try again later."

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await tree.sync()
    daily_menu.start()

@tree.command(name="ping", description="Check if the bot is alive")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

@tree.command(name="menu", description="Show today's (or tomorrow's after 9PM) dining hall menu")
async def menu_command(interaction: discord.Interaction):
    now = datetime.now(tz)
    target_date = now + timedelta(days=1) if now.hour >= 21 else now
    await interaction.response.send_message(get_meals_for(target_date.strftime('%Y-%m-%d')))

@tree.command(name="menu_tomorrow", description="Show tomorrow's dining hall menu")
async def menu_tomorrow_command(interaction: discord.Interaction):
    tomorrow_str = (datetime.now(tz) + timedelta(days=1)).strftime('%Y-%m-%d')
    await interaction.response.send_message(get_meals_for(tomorrow_str))

@tree.command(name="menu_date", description="Show dining hall menu for a specific date (YYYY-MM-DD)")
@app_commands.describe(date="Date in YYYY-MM-DD format")
async def menu_date_command(interaction: discord.Interaction, date: str):
    try:
        datetime.strptime(date, '%Y-%m-%d')  # validate format
        await interaction.response.send_message(get_meals_for(date))
    except ValueError:
        await interaction.response.send_message("Invalid date format. Use YYYY-MM-DD.")

@tasks.loop(hours=24)
async def daily_menu():
    now = datetime.now(tz)
    future = now.replace(hour=21, minute=0, second=0, microsecond=0)
    if now > future:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).seconds)

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        tomorrow_str = (datetime.now(tz) + timedelta(days=1)).strftime('%Y-%m-%d')
        await channel.send(get_meals_for(tomorrow_str))

client.run(TOKEN)
