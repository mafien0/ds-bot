import discord
from discord.ext import commands
import logging
import config as c # `config.py`

# Bot permissions, etc
handler = logging.FileHandler(filename="data/discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=c.prefix,
    intents=intents,
    help_command=None # Remove help command, to not cause any conflicts with the custom one
)

# On ready
@bot.event
async def on_ready():
    print("-" * 50)
    print(f"Bot name: {bot.user.name}")
    print("-" * 50)

# Cogs
async def load_cogs():
    await bot.load_extension("cogs.info")
    await bot.load_extension("cogs.mutes")
    await bot.load_extension("cogs.bans")

# Run
@bot.event
async def setup_hook():
    await load_cogs()

bot.run(c.TOKEN, log_handler=handler, log_level=logging.DEBUG) # Actually run