
import discord
from   discord.ext import commands

import logging
import os, sys, getopt

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    logging.debug("Discord connection made.")
    logging.info("Logging in as:{0} : {1}".format(bot.user.name,bot.user.id))
    print("Logged in as\n{0}\n{1}".format(bot.user.name,bot.user.id))
    for file in os.listdir("Cogs"):
        logging.debug("Loading {}".format(file))
        file_name = file[:-3]
        cog_name = ".".join("Cogs",file_name)
        bot.load_extension(cog_name)

@bot.event
async def on_command(ctx):
    logging.info("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))
    print("Command Received")

if __name__ == "__main__":
    ## TODO: Set logging level to DEBUG if command line args include --debug or -d
    log_level = logging.INFO
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d")
    except getopt.GetoptError:
        print('error in args')
    for opt, arg in opts:
        if opt == '-d':
            log_level = logging.DEBUG
    logging.basicConfig(filename="runtime.log",level=log_level)
    logging.debug("Starting program")
    bot.run('NDM4Mjg4NjYxMzk4NjgzNjUw.DcCb5A.gyiEoXkZyEnnByhjOXshRriRHXY')


