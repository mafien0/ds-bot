from discord import Colour as c
from dotenv import load_dotenv
import os

prefix = "."

# From private config(`.env`)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")   # Discord bot token
ADMIN_ROLE = os.getenv("ADMIN_ROLE") # Admin role id

class color:
    white = c.from_rgb(255, 244, 230)

    default = white