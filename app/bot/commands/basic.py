import asyncio
import discord
from discord import app_commands
from config import TOKEN
from utils.helper import get_gif_url
from app.bot.bot import happy_cat_bot

@happy_cat_bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    try:
        # gif_url = asyncio.run(get_gif_url("happycat"))
        await interaction.response.send_message("https://tenor.com/bXAn9.gif")
    except Exception as e:
        print(e)


@happy_cat_bot.tree.command(name="say")
@app_commands.describe(arg="What should I say?")
async def say(interaction: discord.Interaction, arg:str):
    await interaction.response.send_message(f"{interaction.user.name} said `{arg}`")