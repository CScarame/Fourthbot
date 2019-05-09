import discord
from   discord.ext import commands

import logging
import os

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    logging.debug("Discord connection made.")
    logging.info("Logging in as:{0} : {1}".format(bot.user.name,bot.user.id))
    print("Logged in as\n{0}\n{1}".format(bot.user.name,bot.user.id))
    bot.load_extension("Cogs.XP")

@bot.event
async def on_command(ctx):
    logging.info("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))
    print("Command Received")

if __name__ == "__main__":
    ## TODO: Set logging level to DEBUG if command line args include --debug or -d

    logging.basicConfig(filename="runtime.log",level=logging.INFO)
    logging.debug("Starting program")
    bot.run('NDM4Mjg4NjYxMzk4NjgzNjUw.DcCb5A.gyiEoXkZyEnnByhjOXshRriRHXY')


