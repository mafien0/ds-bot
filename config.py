from discord import Colour as c
from dotenv import load_dotenv
import os
import json

prefix = "."

mutes_loc = "data/mutes.json"
bans_loc = "data/bans.json"
bans_loc = "data/bans.json"

# From private config(`.env`)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")        # Discord bot token
GUILD_ID = int(os.getenv("GUILD_ID"))     # Server id
ADMIN_ROLE = int(os.getenv("ADMIN_ROLE")) # Admin role id
MUTE_ROLE = int(os.getenv("MUTE_ROLE"))   # Role id for mutes

# Commands Help text
ch = f"""```
{prefix}commands:    | Prints this text
{prefix}status:      | Prints if bot is alive
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