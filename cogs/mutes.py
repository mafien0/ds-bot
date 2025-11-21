import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import json
import config as c
from utils import return_error, return_success, send_dm, parse_time

class mutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # start background task
        self.check_mutes.start() 

    def cog_unload(self):
        self.check_mutes.cancel()


    #! Unmute on expire task
    @tasks.loop(minutes=1)  # check every 1 minute
    async def check_mutes(self):
        try:
            with open(c.mutes_loc, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        changed = False

        now = datetime.now(timezone.utc)

        # Look for members with expired mute
        for user_id, info, in list(data.items()):
            expires = datetime.fromisoformat(info["expires"])
            if now >= expires:
                guild = self.bot.get_guild(c.GUILD_ID)
                member = guild.get_member(int(user_id))
                if member:
                    mute_role = guild.get_role(c.MUTE_ROLE)
                    await member.remove_roles(mute_role)
                
                # Remove from file
                del data[user_id]
                changed = True

        if changed:
            with open(c.mutes_loc, "w") as f:
                json.dump(data, f, indent=4)

    # Start unmute task only after `on_ready` function
    @check_mutes.before_loop
    async def before_check_mutes(self):
        await self.bot.wait_until_ready()


    #! Commands

    #* mute
    @commands.command()
    async def mute(self, ctx, member: discord.Member = None, arg1: str = None, *, reason: str = None):
        # Takes member, time(optional) and reason(optional)

        # Permission check
        if not ctx.author.guild_permissions.administrator:
            await return_error(ctx, "Permisson Denied!")

        # If doesn't specify member: error
        if not member:
            await return_error(ctx, "Mute who?")
            return

        # If member is yourself: error
        if ctx.author.id == member.id:
            await return_error(ctx, "You can't mute yourself")
            return

        # If doesn't specify time: time = 10m
        if not arg1:
            arg1 = "10m"

        # If doesn't specify reason: Set "No Reason"
        if not reason:
            reason = "No Reason"


        # If everything seems good:

        # Save {expires_at}, {reason} to json
        # Load the json
        try:
            with open(c.mutes_loc, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Calculating unmute time
        duration = parse_time(arg1)
        expires_at = (datetime.now(timezone.utc) + duration).isoformat()

        # Storing it
        data[str(member.id)] = {"expires": expires_at, "reason": reason}
        with open(c.mutes_loc, "w") as f:
            json.dump(data, f, indent=4)

        # Feedback
        await return_success(ctx, "Mute", (
            f"Successfully muted {member.mention}\n"
            f"**Time:** {arg1}\n"
            f"**Reason:** {reason}"
        ))
        await send_dm(member, "You got muted", (
            f"**By:** {ctx.author.mention}\n"
            f"**Time:** {arg1}\n"
            f"**Reason:** {reason}\n"
        ))

        # Giving a mute role 
        mute_role = ctx.guild.get_role(c.MUTE_ROLE)
        await member.add_roles(mute_role)

    # Error handling
    @mute.error
    async def mute_error(self, ctx, error):
        if c.debug:
            await return_error(ctx, f"{error}")
        else:
            await return_error(ctx, "Something went wrong")


    #* Unmute 
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):

        # Permission check
        if not ctx.author.guild_permissions.administrator:
            return_error(ctx, "Permisson Denied!")
            return

        # Removing mute role
        mute_role = ctx.guild.get_role(c.MUTE_ROLE)
        await member.remove_roles(mute_role)

        # Removing from json
        with open(c.mutes_loc, "r") as f:
            data = json.load(f)
        data.pop(str(member.id), None)
        with open (c.mutes_loc, "w") as f:
            json.dump(data, f, indent=4)

        # Feedback
        await return_success(ctx, "Unmute", (
            f"Succefully unmuted {member.mention}"
        ))
        await send_dm(member, "You got unmuted", (
            f"**By:** {ctx.author.mention}\n"
        ))


    # Error handling
    @unmute.error
    async def mute_error(self, ctx, error):
        if c.debug:
            await return_error(ctx, f"{error}")
        else:
            await return_error(ctx, "Something went wrong")



async def setup(bot):
    await bot.add_cog(mutes(bot))
