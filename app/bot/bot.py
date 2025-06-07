import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Happy cat is ready to launch! ฅᨐฅ")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(f"happy happy happy! happy happy happy happy happy! happy happy happy happy happy!")
    except Exception as e:
        print(e)

# TODO
# @bot.tree.command(name="random")
# async def random(interaction: discord.Interaction):
#     # request /gifs/random in happycatapi 
#     try:
#         await interaction.response.send_message(file=...)
#     except Exception as e:
#         print(e)

# @bot.tree.command(name="tag")
# @app_commands.search_by_tag(tag="What should I say?")
# async def say(interaction: discord.Interaction, tag:str):
#     request /gifs/{tag} in happycatapi
#     await interaction.response.send_message(f"{interaction.user.name} said `{arg}")

# to add-on: send gif upon hearing a certain word (e.g. "happy" -> happycat, 😭 -> bananacat, huh -> huhcat)

bot.run(TOKEN)