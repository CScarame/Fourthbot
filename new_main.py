#############
## new_main.py
## Author: Chris Scaramella
## Date: 5/15/2019
## Main function for Fourthbot.  Logs in and starts bot.
#############


import discord
from   discord.ext import commands

import logging
import os, sys, getopt

## Magic Variables
COMMAND_PREFIX = '!'
DISCORD_TOKEN  = 'NTYyNDczNjY4MzYyNTAyMTc2.XKLSbA.6wdrDFes0nyVckUGrGhauASzkdM'
DISCORD_TOKEN_PARTY  = 'NDM4Mjg4NjYxMzk4NjgzNjUw.DcCb5A.gyiEoXkZyEnnByhjOXshRriRHXY'

LOG_LEVEL    = logging.INFO

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

@bot.event # Decorator that triggers whenever something happens that the bot can pick up.
async def on_ready(): # Function that runs when bot first logs on
    logging.debug("Discord connection made.")
    logging.info("Logging in as:{0} : {1}".format(bot.user.name,bot.user.id))
    print("Logged in as\n{0}\n{1}".format(bot.user.name,bot.user.id))
    # Load in all Cogs
    for file in os.listdir("Cogs"):
        if file[-3:] == ".py":
            logging.debug("Loading {}".format(file))
            print("Loading {}".format(file))
            file_name = file[:-3]
            cog_name = ".".join(["Cogs",file_name])
            bot.load_extension(cog_name)

@bot.event
async def on_command(ctx): # Function that runs when the bot recognizes a command being sent
    logging.info("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))
    print("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))

if __name__ == "__main__":
    ## Set debug if using cmd line args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d")
    except getopt.GetoptError:
        print('error in args')
    for opt, arg in opts:
        if opt == '-d':
            LOG_LEVEL = logging.DEBUG
    logging.basicConfig(filename="runtime.log",level=LOG_LEVEL)
    logging.debug("Starting program")
    bot.run(DISCORD_TOKEN)


