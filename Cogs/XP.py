import discord
from discord.ext import commands

import logging
import googleHandler
import json
import os
import datetime

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
        words = ctx.message.content.split()
        author_id = ctx.message.author.id
        author = self.users[str(author_id)]
        if len(words) == 1: # Simple bank check call
            raw_data = self.handler.read('Bank Chart!A:C')
            if not author in self.dms:
                for player in raw_data:
                    if player[0] == author:
                        msg = 'You currently have **{}** banked xp\n'.format(str(player[1]))
                        msg = msg + 'To spend xp use **!bank (character) (amount) confirm**'
            else:
                msg = 'Players\' banked xp:\n```'
                for player in raw_data:
                    msg = msg + '{:8}:{:4}\n'.format(player[0],str(player[1]))
                msg = msg + '```'
        else: # call to change values
            character_flag = False
            spend_flag = False
            confirm_flag = False
            raw_data = self.handler.read('Bank Chart!A:B')
            characters = set() ### Creating list of potential characters
            for player in raw_data:
                if author == player[0]:
                    max_spend = int(player[1])
            for word in words[1:]:
                if word in characters and not character_flag:
                    character = word
                    character_flag = True
                if word.isdigit() and int(word) <= max_spend and not spend_flag:
                    spend = word
                    spend_flag = True
                if word == 'Confirm' or word == 'corfirm':
                    confirm_flag = True
            if not character_flag:
                msg = "I didn't recognize which character you want to spend on.  Use !xp if you forget your character names."
            elif not spend_flag:
                msg = "I didn't recognize a number of points to spend.  Don't use anything but numbers for that."
            elif not confirm_flag:
                msg = "Enter the same command, with \"Confirm\" after it in order to confirm your spending"
            else: #Date, Author, Player, Character, Debits, Credits, Delta
                self.handler.append('Bank Tracker!A:G',[[str(datetime.date.today()),author,author, character, '0', spend, '-'+spend]])
                msg = "Confirmed! {} gained {} xp!".format(character, str(spend))
        await ctx.send(msg)

    @commands.command(help="session command")
    async def session(self,ctx):
        words = ctx.message.content.split()
        author_id = ctx.message.author.id
        author = self.users[str(author_id)]
        if len(words) == 1: # Help call
            msg = "DMs can use this command in order to award session xp.  Any awarded XP will show up in the #announcements thread"
        else:
            if not author in self.dms:
                msg = "Sorry kid.  You have to be running the game to use this command."
            else:
                session_data = []
                points = words[1]
                msg = "The following characters have been awarded {} xp for a session\n```".format(points)
                with open('config/current_characters.json','r') as current_file:
                    current = json.load(current_file)
                    for player in current:
                        session_data.append([str(datetime.date.today()),author,player,current[player],points])
                        msg = msg + "{:10}\n".format(current[player])
                    msg = msg + "```"
                self.handler.append('Session Tracker!A:E', session_data)
        await ctx.send(msg)

    @commands.command(help="bonus command")
    async def bonus(self, ctx):
        await ctx.send("Implementation in Progress")