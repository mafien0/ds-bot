import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import json
import config as c
from utils import returnError, returnSuccess, sendDM, parseTime

class bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # start background task
        self.check_bans.start() 

    def cog_unload(self):
        self.check_bans.cancel()

    #! Unban on expire task
    @tasks.loop(minutes=1)  # check every 10 minutes
    async def check_bans(self):
        try:
            with open(c.bans_loc, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        changed = False

        now = datetime.now(timezone.utc)

        # Look for members with expired ban
        for user_id, info, in list(data.items()):
            expires = datetime.fromisoformat(info["expires"])
            if now >= expires:
                guild = self.bot.get_guild(c.GUILD_ID)
                if not guild:
                    raise "Guild not found"
                await guild.unban(discord.Object(id=int(user_id)))

                
                # Remove from file
                del data[user_id]
                changed = True

        if changed:
            with open(c.bans_loc, "w") as f:
                json.dump(data, f, indent=4)

    @check_bans.before_loop
    async def before_check_bans(self):
        await self.bot.wait_until_ready()


    #! Commands

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None, arg1: str = None, *, reason: str = None):
        # Takes member, time(optional) and reason(optional)

        # Permission check
        if not ctx.author.guild_permissions.administrator:
            await returnError(ctx, "Permisson Denied!")

        # If doesn't specify member: error
        if not member:
            await returnError(ctx, "ban who?")
            return

        # If member is yourself: error
        if ctx.author.id == member.id:
            await returnError(ctx, "You can't ban yourself")
            return

        # If doesn't specify time: time = 1mo
        if not arg1:
            arg1 = "1mo"

        # If doesn't specify reason: Set "No Reason"
        if not reason:
            reason = "No Reason"

        # If everythings seems good:
        # Save {expires_at}, {reason} to json
        # Load the json
        try:
            with open(c.bans_loc, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Calculating unban time
        duration = parseTime(arg1)
        expires_at = (datetime.now(timezone.utc) + duration).isoformat()

        # Storing it
        data[str(member.id)] = {"expires": expires_at, "reason": reason}
        with open(c.bans_loc, "w") as f:
            json.dump(data, f, indent=4)

        # Feedback
        await returnSuccess(ctx, "Ban", (
            f"Successfully baned {member.mention}\n"
            f"**Time:** {arg1}\n"
            f"**Reason:** {reason}"
        ))
        await sendDM(member, "You got baned", (
            f"**By:** {ctx.author.mention}\n"
            f"**Time:** {arg1}\n"
            f"**Reason:** {reason}\n"
        ))

        # Actually banning
        await member.ban()

    # Error handling
    @ban.error
    async def ban_error(self, ctx, error):
        if c.debug:
            await returnError(ctx, f"{error}")
        else:
            await returnError(ctx, "Something went wrong")


    @commands.command()
    async def unban(self, ctx, user: discord.User):
        # Permission check
        if not ctx.author.guild_permissions.administrator:
            await returnError(ctx, "Permission Denied!")
            return

        guild = ctx.guild
        bans = [entry async for entry in guild.bans()]

        # Try to find the user by name, mention, or ID
        banned_user = None
        for entry in bans:
            if isinstance(user, (discord.User, discord.Member)):
                if user.id == entry.user.id:
                    banned_user = entry.user
                    break
            elif isinstance(user, str):
                user = user.strip('<@!>')
                if (
                    user == str(entry.user.id) or 
                    user.lower() == entry.user.name.lower()
                ):
                    banned_user = entry.user
                    break
        
        if not banned_user:
            await returnError(ctx, f'User "{user}", not found')
            return

        await guild.unban(banned_user)

        # Remove from JSON
        with open(c.bans_loc, "r") as f:
            data = json.load(f)
        data.pop(str(user.id), None)
        with open(c.bans_loc, "w") as f:
            json.dump(data, f, indent=4)

        # Feedback
        await returnSuccess(ctx, "Unban", (
            f"Successfully unbanned {user.mention}"
        ))

        try:
            await sendDM(user, "You were unbanned", f"**By:** {ctx.author.mention}")
        except:
            pass

    # Error handling
    @unban.error
    async def ban_error(self, ctx, error):
        if c.debug:
            await returnError(ctx, f"{error}")
        else:
            await returnError(ctx, "Something went wrong")

async def setup(bot):
    await bot.add_cog(bans(bot))