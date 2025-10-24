from dotenv import load_dotenv
import os

prefix = "."

# From private config(`.env`)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")   # Discord bot token
ADMIN_ROLE = os.getenv("ADMIN_ROLE") # Admin role id