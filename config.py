from discord import Colour as c
from dotenv import load_dotenv
import os
import json

debug = True

prefix = "."

# File locations
mutes_loc = "data/mutes.json"
bans_loc = "data/bans.json"
bans_loc = "data/bans.json"

# From private config(`.env`)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")        # Discord bot token
GUILD_ID = int(os.getenv("GUILD_ID"))     # Server id
MUTE_ROLE = int(os.getenv("MUTE_ROLE"))   # Role id for mutes

# Commands Help text
ch = f"""```
----- Base -----
{prefix}commands    | Prints this text
{prefix}status      | Prints if bot is alive

----- Moderation -----
{prefix}mute <@member> <time>(Optional) <reason>(Optional):
    Mutes member for time(N+y/mo/d/h/m) with reason
    If time doesn't specified, mute for 10m
    If reason doesn't specified, mute for "No Reason"

    Example:
    >>> {prefix}mute @bad_guy 1d Saying bad words


{prefix}unmute <@member>
    opposite of {prefix}mute, removes mute from a member

    Example:
    >>> {prefix}unmute @good_guy
```"""

# Colors config
class color:
    white = c.from_rgb(255, 244, 230)
    red = c.from_rgb(133, 68, 66)
    green = c.from_rgb(119, 171, 89)
    yellow = c.from_rgb(255, 204, 92)

    default = white
    error = red
    success = green
    punishment = yellow