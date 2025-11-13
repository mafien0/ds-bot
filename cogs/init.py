import discord
import json
import config as c

async def initGuild():
    try:
        with open(c.mutes_loc, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
