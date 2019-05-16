#############
## test.py
## Author: Chris Scaramella
## Date: 5/15/2019
## Testing out cogs and commands.  This file will be archived during the switch to v2.0
#############

import discord
from discord.ext import commands

# This is where the cog is defined.
class TestCog(commands.Cog):
    """ This is a test cog with only one test command"""
    # This comment is pulled out of the file to be the help description for this command
    
    # Use at least this text, but you can add commands that add things to the bot.
    def __init__(self, bot):
        self.bot = bot
        
    # Use help= to change the help description of the command
    @commands.command(help="test help!")
    async def test(self, ctx, *, test : str):
        await ctx.send(test)

# Must use setup command below for loading extension into bot.
def setup(bot):
    bot.add_cog(TestCog(bot))
