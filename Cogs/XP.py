#############
## XP.py
## Author: Chris Scaramella and Brian Scaramella
## Date: 5/15/2019
## All commands involved in experience calculation
#############
## List of commands:
## xp       :   Check xp of all players, can check specific characters using that player's name
## current  :   Check who your current character is, can be used to change a player's current character
## bank     :   Check player's banked xp, can be used to spend banked xp on characters
## session  :   Used by DMs to grant all player current characters xp for the previous session
## bonus    :   Used by DMs to grant a player bonus XP
#############
import discord
from discord.ext import commands

import logging
import googleHandler
import json
import os
import datetime

## Magic Variables
# Other
DM_LIST         = ['Chris','Brian','Tommy']

# Google
GOOGLE_HANDLE   = '1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo'
XP_LOCATION     = 'Character Chart!A2:G14'
BANK_LOCATION   = 'Bank Chart!A:B'
BANK_TRACKER    = 'Bank Tracker!A:G'
SESSION_TRACKER = 'Session Tracker!A:E'

#JSON
JSON_USERS      = 'config/users.json'
JSON_CURRENT    = 'config/current_characters.json'
JSON_CHATS      = 'config/character_chats.json'

def setup(bot):
    bot.add_cog(XP(bot))

class XP(commands.Cog):
    """ All experience related commands"""
    ## XP Cog Variables
    ## self.handler : googleHandler - for accessing Google Doc
    ## self.users   : dict of ids to the names associated with them
    ## self.dms     : list of dm names #TODO: Replace self.dms with check role of the author
    
    def __init__(self,bot):
        self.bot = bot
        logging.debug("XP Cog loaded")
        ## TODO: Eventually pull handle from somewhere
        google_token = GOOGLE_HANDLE
        self.handler = googleHandler.googleHandler(google_token)
        ## Get Important JSON files
        with open(JSON_USERS,'r') as users_file:
            self.users = json.load(users_file)
        self.dms = DM_LIST

    @commands.command(help="Use this command to check the xp of your characters")
    async def xp(self, ctx, *args):
        ## Get important variables
        args = [x.lower() for x in args]
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data = self.handler.read(XP_LOCATION)
        msg = '```'
        if not args: # No arg call show all chars user can possibly see
            for character in raw_data:
                if author == character[0] or is_dm:
                    msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(
                          character[1],character[4],character[5],character[6])
        if args: # call for if there are args
            for character in raw_data:
                if (author == character[0] or is_dm) and character[1].lower() in args:
                    msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(
                          character[1],character[4],character[5],character[6])
        msg = msg + '```'
        if msg == '``````':
            msg = 'No characters found, please check your spelling! :clap:'
        await ctx.send(msg)

    @commands.command(help="Check or change your current character")
    async def current(self,ctx, *args):
        ## Get important variables
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data  = self.handler.read(XP_LOCATION)
        with open(JSON_CURRENT,'r') as current_file:
            current = json.load(current_file)
        msg = ''
        if args and is_dm: #DM changes player's character and/or checks currents
            for arg in args:
                if arg.capitalize() in current:
                    msg = msg + '{}\'s current character is **{}**\n'.format(arg.capitalize(), current[arg.capitalize()])
                for character in raw_data:
                    if arg.lower() == character[1]:
                        current[character[0]] == character[1]
                        with open(JSON_CURRENT, 'w') as current_file:
                            json.dump(current,current_file)
                        msg = msg + '{0[0]}\'s current character has been set to **{0[1]}**\n'.format(character)
                        break
            if not msg:
                msg = 'I did not recognize any names.'
        elif args and not is_dm: #Player changes his or her character
            if len(args) > 1:
                msg = 'You can only have one current character.  Please only use one name'
                await ctx.send(msg)
                return
            arg = args[0]
            for character in raw_data:
                if arg != character[1]:
                    continue
                if author != character[0]:
                    msg = 'You do not own that character!'
                    break
                current[character[0]] == character[1]
                with open(JSON_CURRENT, 'w') as current_file:
                    json.dump(current,current_file)
                msg = 'I set your current character as \n'
                msg = msg + '```{:10}{:5} XP Level {:3}({:5} XP to next level)```'.format(
                    character[1],character[4],character[5],character[6])
                break
        elif not args and is_dm: #DM checks all current chars
            msg = msg + 'Current Characters:\n```'
            for player in current:
                msg = msg + '{:10}:{:10}\n'.format(player,current[player])
            msg = msg + '```'
        elif not args and not is_dm: #Player checks their current char
            msg = 'Your current character is **{:10}**\n'.format(current[author])
            msg = msg + 'To switch to a different character use **!current (character)**'    
        await ctx.send(msg)

    @commands.command(help="Check your xp bank balance or spend it on characters")
    async def bank(self, ctx, *args):
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data = self.handler.read(BANK_LOCATION)
        char_data = self.handler.read(XP_LOCATION)
        if not args and is_dm: #DM checks all banked xp
            msg = 'Players\' banked xp:\n```'
            for player in raw_data:
                msg = msg + '{:8}:{:4}\n'.format(player[0],str(player[1]))
            msg = msg + '```'
            await ctx.send(msg)
        elif not args and not is_dm: # Player checks their xps
            for player in raw_data:
                if player[0] == author:
                    msg = 'You currently have **{}** banked xp\n'.format(str(player[1]))
                    msg = msg + 'To spend xp use **!bank (character) (amount) confirm**'
                    break
            await ctx.send(msg)
        elif args and not is_dm: #Player spends xp
            confirm_flag, value_flag, character_flag = False, False, False
            for player in raw_data:
                if author == player[0]:
                    max_value = int(player[1])
            characters = set()
            for character in char_data:
                characters.add(character[1])
            for arg in args:
                if arg == 'confirm' or arg == 'Confirm':
                    confirm_flag = True
                    continue
                elif arg.isdigit() and not value_flag:
                    value = int(arg)
                    if max_value < value:
                        msg = "Error:  You do not have that many points to spend!"
                        await ctx.send(msg)
                        return
                    value_flag = True
                    continue
                elif arg in characters:
                    character = arg
                    character_flag = True
            if not (character_flag and value_flag and confirm_flag): # Oops section
                msg = 'The following problems occurred\n'
                if not character_flag:
                    msg = msg + 'You did not name a character, or I did not recognize the name\n'
                if not value_flag:
                    msg = msg + 'You did not enter a valid value\n'
                if not confirm_flag:
                    msg = msg + 'You must say **confirm** with the command for it to work.\n'
                msg = msg + 'Proper use of the command is **!bank (character) (value) confirm**'
                await ctx.send(msg)
                return
            self.handler.append(BANK_TRACKER,[[str(datetime.date.today()),author,author, character, '0', str(value), '-'+str(value)]])
            msg = "Confirmed! {} gained {} xp!".format(character, value)
            await ctx.send(msg)
        elif args and is_dm: # Dm checks specific player's bank values
            msg = 'Players\' banked xp:\n```'
            for player in raw_data:
                if player[0] in args:
                    msg = msg + '{:8}:{:4}\n'.format(player[0],str(player[1]))
            msg = msg + '```'
            await ctx.send(msg)

    @commands.command(help="DMs ONLY: grant session XP")
    async def session(self,ctx, *args):
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        if not is_dm: #Only DMs can use this command
            msg = "DMs can use this command in order to award session xp.  Any awarded XP will show up in the #announcements thread"
        elif not args: #Command doesn't work without arguments
            msg = "Use **!session (value)** to assign points for a session to current characters
        elif args: #Actual command
            session_data = []
            points = int(args[0])
            msg = "The following characters have been awarded {} xp for a session\n```".format(points)
            with open(JSON_CURRENT,'r') as current_file:
                current = json.load(current_file)
                for player in current:
                    session_data.append([str(datetime.date.today()),author,player,current[player],points])
                    msg = msg + "{:10}\n".format(current[player])
                msg = msg + "```"
            self.handler.append(SESSION_TRACKER, session_data)
        await ctx.send(msg)

    @commands.command(help="DMs ONLY: grant bonus XP")
    async def bonus(self, ctx, *args):
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        if not is_dm:
            msg = "Sorry kid.  You have to be running the game to use this command."
        elif not args:
            msg = "Use **!bonus (player) (value)** to give a player bonus xp, or **!bonus (value)** in a player's chat."
        elif args:
            with open(JSON_CHATS,'r') as cc_file:
                chats = json.load(cc_file)
            with open(JSON_CURRENT,'r') as current_file:
                current = json.load(current_file)
            player_flag, value_flag = False, False
            if str(ctx.message.channel.id) in chats:
                player = chats[str(ctx.message.channel.id)]
                player_flag = True
            for arg in args:
                if arg.isdigit() and not value_flag:
                    value = int(arg)
                    value_flag = True
                elif arg in current:
                    player = arg
                    player_flag = True
            if not player_flag or not value_flag:
                msg = "No xp awarded because message did not parse correctly"
            else:
                session_data = [[str(datetime.date.today()),author, player, "", str(value), "0", str(value)]]
                self.handler.append(BANK_TRACKER, session_data)
                msg = "{} awarded {} {} bonus xp.  Congrats!".format(author,player,str(value))
        await ctx.send(msg)

