import discord
from discord.ext import commands
import logging

import config as c # `config.py`

# Bot permissions, etc
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=c.prefix,
    intents=intents,
    help_command=None # Remove help command, to not cause any conflicts with the custom one
)

# Commands text
command_h = f"""```
{c.prefix}commands:    | Prints this text
{c.prefix}status:      | Prints if bot is alive
```"""

# On ready, print info and ping admin role
@bot.event
async def on_ready():
    print("-" * 50)
    print(f"Bot name: {bot.user.name}")
    print("-" * 50)


# Commands
async def load_cogs():
    await bot.load_extension("cogs.info")

@bot.command()
async def ch(ctx):

    embed = discord.Embed(
        title="Commands",
        description=command_h,
        color=(c.color.default)
    )

    msg = await ctx.reply(embed=embed)

# Actually run
@bot.event
async def setup_hook():
    await load_cogs()

bot.run(c.TOKEN, log_handler=handler, log_level=logging.DEBUG)