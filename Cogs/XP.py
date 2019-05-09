import discord
from discord.ext import commands

import logging
import googleHandler
import json
import os

def setup(bot):
    bot.add_cog(XP(bot))

class XP(commands.Cog):
    """ All experience related commands"""
    def __init__(self,bot):
        self.bot = bot
        logging.debug("XP Cog loaded")
        ## TODO: Eventually pull handle from somewhere
        google_token = '1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo'
        self.handler = googleHandler.googleHandler(google_token)
        ## Get Important JSON files
        with open('config/users.json','r') as users_file:
            self.users = json.load(users_file)
        self.dms = ['Chris','Brian','Tommy']

    @commands.command(help="xp command")
    async def xp(self, ctx):
        ## Words is a list of words in the command
        words = ctx.message.content.split()
        specific_flag = False
        specific_char = []
        if len(words) >= 2:
            # If command references specific characters, remember them
            specific_flag = True
            for character in words[1:]:
                specific_char.append(character.lower())
        # Get author
        author_id = ctx.message.author.id
        author = self.users[str(author_id)]
        # Get google raw_data
        raw_data = self.handler.read('Character Chart!A2:G13')
        # Start output
        msg = '```'
        for character in raw_data:
            if author == character[0] or author in self.dms and character[0] is not 'Player':
                if not specific_flag or character[1].lower() in specific_char:
                    msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(character[1],
                                                character[4],character[5],character[6])
        msg = msg + '```'
        if msg == '``````':
            msg = 'No characters found, please check your spelling! :clap:'
        await ctx.send(msg)

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