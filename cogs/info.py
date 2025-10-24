import discord
from discord.ext import commands

import config as c

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # status
    @commands.command()
    async def status(self, ctx):
        await ctx.reply("Alive!")

    @commands.command()
    async def ch(self, ctx):

        embed = discord.Embed(
            title="Commands",
            description=c.ch,
            color=(c.color.default)
        )

        msg = await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(info(bot))