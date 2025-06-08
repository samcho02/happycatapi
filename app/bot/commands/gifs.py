# import asyncio
# import discord
# from discord import app_commands
# from discord.ext import commands
# from config import TOKEN
# from utils.helper import get_gif_url
# from app.bot.bot import happy_cat_bot

# TODO
# @happy_cat_bot.tree.command(name="random")
# async def random(interaction: discord.Interaction):
#     # request /gifs/random in happycatapi 
#     try:
#         await interaction.response.send_message(file=...)
#     except Exception as e:
#         print(e)

# @happy_cat_bot.tree.command(name="tag")
# @app_commands.describe(query="What should I say?")
# async def say(interaction: discord.Interaction, tag:str):
#     # request /gifs/{tag} in happycatapi
#     await interaction.response.send_message(f"{interaction.user.name} said `{tag}`")

# to add-on: send gif upon hearing a certain word (e.g. "happy" -> happycat, 😭 -> bananacat, huh -> huhcat)