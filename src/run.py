"""
Skyline Discord Bot
~~~~~~~~~~~~~~~~~~~~~

© 2023 AstonK69
GPL-3.0 License, see LICENSE for more details

~~~~~~~~~~~~~~~~~~~~~
run.py
"""

import os
import load
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

prefix = "."
activity = discord.Activity(type=discord.ActivityType.watching, name="Seven win all the time")
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, activity=activity, owner_id=[760602301790158868], intents=intents)
bot.remove_command("help")


def loadCog(path, folder=True):
    if folder:
        for filename in os.listdir(f'{load.path}/cogs/{path}'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{path}.{filename[:-3]}')
                print(f'{filename[:-3]} cog loaded')
    else:
        bot.load_extension(f'cogs.{path}')
        return "Loaded extensions"


if __name__ == "__main__":
    loadCog("events")
    loadCog("commands")

    bot.run(load.token)
