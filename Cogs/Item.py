############
## Item.py
## Author: Chris Scaramella
## Date: 9/4/2019
## Let players get descriptions for any item in DnD
############
import discord
from discord.ext import commands

import logging

def setup(bot):
    bot.add_cog(Item(bot))

class Item(commands.Cog):
    """Commands for learning what an item is/does"""

    def __init__(self,bot):
        self.bot = bot
        logging.debug("Item Cog loaded")


    @commands.command(help="Get an item description")
    async def item(self,ctx):
        msg = "item command is currently in work."
        await ctx.send(msg)