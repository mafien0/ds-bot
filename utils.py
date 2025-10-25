from dateutil.relativedelta import relativedelta
import discord
import config as c

async def throwError(ctx, error: str,):
    embed = discord.Embed(
        title="Error",
        description=f"{error}",
        color=c.color.error
    )
    await ctx.message.add_reaction("❌")
    await ctx.reply(embed=embed)


async def parse_time(time_str: str):
    # 2 Letters, so handled separately
    if time_str.endswith("mo"):
        num = int(time_str[:-2])
        return relativedelta(months=num)

    num = int(time_str[:-1])
    unit = time_str[-1]
    if unit == "y":
        return relativedelta(years=num)
    if unit == "d":
        return relativedelta(days=num)
    if unit == "h":
        return relativedelta(hours=num)
    if unit == "m":
        return relativedelta(minutes=num)
    else:
        raise "Error, use `Num + y/mo/d/h/m"