#############
## Spell.py
## Author: Chris Scaramella
## Date: 5/16/2019
## For spell based commands
#############
## Command List
## spell    : Give a spell description.
#############

## Magic Variables
SPELL_LOCATION = 'config/spell3.json'

import discord
from discord.ext import commands

import json
import difflib

def setup(bot):
    bot.add_cog(Basic(bot))

class Spell(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        logging.debug("Spell Cog Loaded")
        
        ## self.spells is a set() of spell names that is stored locally, so we don't have to open the json file every time.
        with open(SPELL_LOCATION) as spell_file:
            self.spells = set(json.load(spell_file).keys())
        logging.debug("Spell list loaded")
            
                
            

    @commands.command(help="Get info about a spell")
    async def spell(self, ctx, *, spell_name: str):
        spell_name.translate(str.maketrans('', '', string.punctuation)) #remove punctuation from input string
        if spell_name not in self.spells:
            possible_matches = difflib.get_close_matches(spell_name,list(self.spells))
            if not possible_matches:
                msg = ("Not sure what spell you were asking for.  Check your spelling!")
            else:
                msg = ("The spell you listed doesn't match any spells.  Did you mean:\n"
                       "\n".join(possible_matches))
            await ctx.send(msg)
        logging.debug("Recognized spell command for spell {}".format(spell_name)
        with open(SPELL_LOCATION) as spell_file:
            spell_data = json.load(spell_file)[spell_name]
        msg = ("```{0}\n  Level: {1['level']}\n  School: {1['school']}\n  Casting Time: {1['time']}\n"
               "  Components: {1['components']}\n  Duration: {1['duration']}\n"
               "  Ritual: {1['ritual']} | Concentration: {1['concentration']}\n  Source: {1['source'}\n"
               "    {1['description']```").format(spell_name, spell_data)
        await ctx.send(msg)        
        
            
        

