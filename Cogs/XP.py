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
            if author == character[0] or author in self .dms and character[0] is not 'Player':
                if not specific_flag or character[1].lower() in specific_char:
                    msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(character[1],
                                                character[4],character[5],character[6])
        msg = msg + '```'
        if msg == '``````':
            msg = 'No characters found, please check your spelling! :clap:'
        await ctx.send(msg)

    @commands.command(help="current command")
    async def current(self,ctx):
        words = ctx.message.content.split()
        ## Specific flag for if a specific character is chosen
        specific_flag = False
        specfic_char = ''
        if len(words) >= 2:
            specific_flag = True
            specific_char = words[1]
        author_id = ctx.message.author.id
        author = self.users[str(author_id)]
        raw_data = self.handler.read('Character Chart!A:G')
        with open('config/current_characters.json','r') as current_file:
            current = json.load(current_file)
        msg = ''
        if specific_flag == True:
            for character in raw_data:
                if author == character[0] and specific_char == character[1]:
                    current[author] = specific_char
                    msg =       'I set your current character as \n'
                    msg = msg + '```{:10}{:5} XP Level {:3}({:5} XP to next level)```'.format(
                        character[1],character[4],character[5],character[6])
                    with open('config/current_characters.json','w') as current_file:
                        json.dump(current, current_file)
                if msg == '':
                    msg = 'I didn\'t recognize the character you listed.  Here are your current characters:\n```'
                    for character in raw_data:
                        if author == character[0]:
                            msg = msg + '{:10}'.format(character[1])
                    msg = msg + '```\nUse **!current (character)** to switch characters.'
                    msg = msg + 'Be sure to use proper capitalization.'
        elif author in self.dms:
            msg = msg + 'Current Character:\n```'
            for player in current:
                msg = msg + '{:10}:{:10}\n'.format(player,current[player])
            msg = msg + '```'
        else:
            msg = 'Your current character is\n```{:10}```\n'.format(current[author])
            msg = msg + 'To switch to a different character use **!current (character)**'    
        await ctx.send(msg)

    @commands.command(help="bank command")
    async def bank(self, ctx):
        await ctx.send("Implementation in progress")

    @commands.command(help="session command")
    async def session(self,ctx):
        await ctx.send("Implementation in progress")

    @commands.command(help="bonus command")
    async def bonus(self, ctx):
        await ctx.send("Implementation in Progress")