import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN
from utils.helper import get_gif_url

happy_cat_bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@happy_cat_bot.event
async def on_ready():
    print("Happy cat is ready to launch! ฅᨐฅ")
    try:
        synced = await happy_cat_bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

happy_cat_bot.run(TOKEN)