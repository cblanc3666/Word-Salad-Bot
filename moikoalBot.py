# -*- coding: utf-8 -*-
"""
Created on Sat May  9 01:18:33 2020

@author: chase
"""


# bot.py
import discord

# note: I store the token in a separate text file for security purposes
# I have uploaded the text file (token.txt) it to the git repository
# This is okay because the git repository is private
# THE TOKEN MUST BE KEPT PRIVATE
TOKEN = open("token.txt", "r").read()

# we can also make the guild name private and read in from a text file too
# I've hard-coded it in here, though
GUILD = "Messing with Bots"

# create an instance of a client object - the bot is the client
client = discord.Client()



@client.event
# runs when bot successfully connected to discord
async def on_ready():
    # bot retrieves name of current server (defined in GUILD variable)
    # from list of servers (guilds) that the bot is connected to
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    # print statements print to the local Python console
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
@client.event
# runs every time a message is sent in a channel the bot can see
async def on_message(message):
    # this is true if the bot is the author of the message
    # this prevents the bot from reacting to its own messages
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        # returns a msg in the channel where the original msg was received
        await message.channel.send('OI')
        await message.channel.send(':heart:')

# begins the run loop that makes the bot go online
client.run(TOKEN)