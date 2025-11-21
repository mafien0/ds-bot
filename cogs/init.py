import discord
from discord.ext import commands
import json
import config as c
from utils import return_error, add_warning, return_success

async def create_mute_role(bot, ctx, guild_id) -> int:
    guild = bot.get_guild(guild_id)
    try:
        new_role = await guild.create_role(name="Muted")
        await return_success(ctx, "Role creation", "Successfully made a mute role")
        return int(new_role.id)
    except Exception as e:
        if c.debug:
            await return_error(ctx, f"{e}")
        else:
            await return_error(ctx, f"Could not create mute role")
        return 0

class init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Init command
    @commands.command()
    async def init(self, ctx):
        guild = ctx.guild
        guild_id = str(guild.id)

        # Open config file
        try:
            with open(c.serinfo_loc, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        changed = False

        if guild_id not in data:
            data[guild_id] = {}

        # Looking for for mute role
        role_id = int(data[guild_id].get("mute_role", 0))

        if not guild.get_role(role_id):
            await add_warning(ctx, "No mute role found", "Going to make one...")
            data[guild_id]["mute_role"] = await create_mute_role(self.bot, ctx, guild.id)
            changed = True

        if c.debug:
            print("~" * 50)
            print(f"{data}")
            print(f"Changed: {changed}")

        if changed:
            with open(c.serinfo_loc, "w") as f:
                json.dump(data, f, indent=4)

        await return_success(ctx, "Init", "All set up!")

async def setup(bot):
    await bot.add_cog(init(bot))
