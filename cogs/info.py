import discord
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # status
    @commands.command()
    async def status(self, ctx):
        await ctx.reply("Alive!")

async def setup(bot):
    await bot.add_cog(info(bot))