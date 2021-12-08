import os
import discord
import requests
import json
from json import loads
from keep_alive import keep_alive
from urllib.request import urlopen
from discord.ext import commands
import music
import game
import chat
import sys
import random

# This is a simple utility discord bot. It uses 3 different cogs to handle user input. The game cog allows you to play a game of tictactoe against an AI(Minimax algorithm has not been implemented as of now, AI has random inputs). The music cog allows you to play youtube vidoes on the bot and the chat cog allows multiple chat commands such as API calls to check the player's rank and stats in multiple games. 
cogs = [game, music, chat]
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
#Loop through and add all the cogs to the client
for i in range(len(cogs)):
    cogs[i].setup(client)

#The discord bot key is kept secure in an envrioment variable. 
my_secret = os.environ['key']
keep_alive()
client.run(my_secret)
