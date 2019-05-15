#############
## new_main.py
## Author: Chris Scaramella
## Date: 5/15/2019
## Main function for Fourthbot.  Logs in and starts bot.
#############
## Use logging.debug() when entering functions etc for debugging help
## Use logging.info for data collection on command entry

import discord
from   discord.ext import commands

import logging
import os

## Magic Variables
COMMAND_PREFIX = '!'
DISCORD_TOKEN  = 'NDM4Mjg4NjYxMzk4NjgzNjUw.DcCb5A.gyiEoXkZyEnnByhjOXshRriRHXY'
DEBUG_LEVEL    = logging.INFO

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

@bot.event # Decorator that triggers whenever something happens that the bot can pick up.
async def on_ready(): # Function that runs when bot first logs on
    logging.debug("Discord connection made.")
    logging.info("Logging in as:{0} : {1}".format(bot.user.name,bot.user.id))
    print("Logged in as\n{0}\n{1}".format(bot.user.name,bot.user.id))
    
    ## TODO: Check Cogs folder for all Cogs and load them in
    bot.load_extension("Cogs.XP")

@bot.event
async def on_command(ctx): # Function that runs when the bot recognizes a command being sent
    logging.info("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))
    print("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))

if __name__ == "__main__":
    ## TODO: Set logging level to DEBUG if command line args include --debug or -d
    logging.basicConfig(filename="runtime.log",level=DEBUG_LEVEL)
    logging.debug("Starting program")
    bot.run(DISCORD_TOKEN)


