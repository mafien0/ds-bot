import discord
from discord.ext import commands
import logging


import config # `config.py`

# Bot permissions, etc
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.prefix, intents=intents)

# On ready, print info and ping admin role
@bot.event
async def on_ready():
    print("-" * 50)
    print(f"Bot name: {bot.user.name}")
    print("-" * 50)


#* Commands
async def load_cogs():
    await bot.load_extension("cogs.info")

# Actually run
@bot.event
async def setup_hook():
    await load_cogs()

bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)