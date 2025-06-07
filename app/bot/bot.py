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

bot.run(TOKEN)