# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 01:14:00 2020

@author: chase
"""


import discord
from discord.ext import commands

class Example(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    # Events    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online.')
    
    # Commands
    @commands.command()    
    async def ping(self, ctx):
        await ctx.send('Pong! uwu')
        
        
        
        
def setup(client):
    client.add_cog(Example(client))
    