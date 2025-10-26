from dateutil.relativedelta import relativedelta
import discord
import config as c

async def returnError(ctx, error: str,):
    embed = discord.Embed(
        title="Error",
        description=f"{error}",
        color=c.color.error
    )
    await ctx.message.add_reaction("❌")
    await ctx.reply(embed=embed)


async def returnSuccess(ctx, action: str, description: str):
    embed = discord.Embed(
        title=action,
        description=description,
        color=c.color.success
    )
    await ctx.message.add_reaction("✅")
    await ctx.reply(embed=embed)


async def sendDM(member, title: str, description: str):
        embed = discord.Embed(
            title=title,
            description=description,
            color=c.color.punishment
        )
        try: await member.send(embed=embed)
        except: pass


def parseTime(time_str: str):
    # If starting not with number, num = 1
    try:
        num = int(time_str[:-1])
    except:
        num = 1

    # 2 Letters, so handled separately
    if time_str.endswith("mo"):
        return relativedelta(months=num)

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