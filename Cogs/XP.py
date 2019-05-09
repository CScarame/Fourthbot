import discord
from discord.ext import commands

import logging

def setup(bot):
    bot.add_cog(XP(bot))

class XP(commands.Cog):
    """ All experience related commands"""
    def __init__(self,bot):
        self.bot = bot
        logging.debug("XP Cog loaded")

    @commands.command(help="xp command")
    async def xp(self, ctx):
        await ctx.send("Implementation in progress")

    @commands.command(help="current command")
    async def current(self,ctx):
        await ctx.send("Inplementation in progress")

    @commands.command(help="bank command")
    async def bank(self, ctx):
        await ctx.send("Implementation in progress")

    @commands.command(help="session command")
    async def session(self,ctx):
        await ctx.send("Implementation in progress")

    @commands.command(help="bonus command")
    async def bonus(self, ctx):
        await ctx.send("Implementation in Progress")