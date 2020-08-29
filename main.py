import random
import discord
import os
from discord.ext import commands

command_prefix = '$'

# create an instance of a client object - the bot is the client
client = commands.Bot(command_prefix)

distribution = {'a': 13, 'b': 3, 'c': 3, 'd': 6, 'e': 18, 'f': 3, 'g': 4, 'h': 3, 'i': 12, 'j': 2, 'k': 2, 'l': 5,
                'm': 3, 'n': 8, 'o': 11, 'p': 3, 'q': 2, 'r': 9, 's': 6, 't': 9, 'u': 6, 'v': 3, 'w': 3, 'x': 2, 'y': 3,
                'z': 2
}


GUILD = "Messing with Bots"

# @@@@@@@@@@@@@@@@@@@@@@@ Define Classes @@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Player has a name and a list of words
class Player:
    def __init__(self, name, user=None):
        self.name = name    # The in-game name a player uses
        self.user = user    # The discord username of the player
        self.words = []
        self.vip = False

    def __str__(self):
        rtn = "{}: {}".format(self.user, self.name)
        if self.vip:
            rtn += " (VIP)"
        return rtn

    def add_word(self, word):
        self.words.append(word)

    def remove_word(self, word):
        self.words.remove(word)


class Node:
    def __init__(self, data):
        self.data = data    # the value the Node carries
        self.next = None    # a Node

    def __repr__(self):
        return self.data


class CircularLinkedList:
    def __init__(self, nodes=None):
        self.head = None    # a Node
        if nodes is not None:   # iterates through iterable nodes and links one to the next
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
            node.next = self.head   # links the last node to the first

    def __repr__(self):
        if self.head is None:
            return "List is Empty"
        node = self.head
        nodes = []
        while True:
            nodes.append(str(node.data))
            node = node.next
            if node == self.head:   # if all nodes have been added to list
                nodes.append(str(node.data))
                break
        nodes.append("...")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while True:
            yield node
            node = node.next
            if node == self.head:   # iterate until loop is complete
                return

    def add_node(self, node):   #adds node to the "end" of the circular linked list
        if self.head is None:
            self.head = node
            self.head.next = self.head
            return "empty"
        for current_node in self:
            if current_node.next == self.head:  # if the "end" has been reached
                current_node.next = node    #insert node
                node.next = self.head   # link back to head

    def remove_node(self, node):    # remove node from circular linked list
        for current_node in self:
            if current_node.next.data == node.data:     # if target node is found
                current_node.next = current_node.next.next  # skip over target node
                return

# Returns the letters that need to be removed from the pool
# If the word is invalid, an empty list is returned
def compare(test_word, new_word, pool):
    pool_letters = []   # list of returned letters
    test_list = str_to_list(test_word)
    for letter in new_word:
        if letter in test_list:
            test_list.remove(letter)    # keeps track of which letters have been used already
        elif letter in pool:
            pool_letters.append(letter)
        else:               # If a certain letter is not in the word or pool,
            return []       # comparison is invalid
    if len(test_list) == 0 and len(pool_letters) > 0:   # If all of the letters in test_word were used, and if some
        return pool_letters                             # letters from the pool were used, comparison is valid
    return []


# Converts a string into a list of characters
def str_to_list(string):
    letters = []
    for letter in string:
        letters.append(letter)
    return letters


# Splits string into two parts based on the location of a semicolon
def split(string):
    index = 0
    for i in range(len(string)):
        if string[i] == ':':
            index = i
            break
    return string[0:index], string[index + 1:len(string)]

# @@@@@@@@@@@@@@@@@@@@@@@ Actual Game Events Begin @@@@@@@@@@@@@@@@@@@@@@@@@@
    
client.playing = False; # indicates when it is ok to start the game
client.players = CircularLinkedList() # create list

# EVENTS

@client.event
# runs when bot successfully connects to discord
async def on_ready():

    # bot retrieves name of current server (defined in GUILD variable)
    # from list of servers (guilds) that the bot is connected to
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    # print statements print to the local Python console
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# This was preventing me from seeing other errors so we can uncomment it once we'd reasonable expect to be done debugging

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please pass in all required arguments.')


# COMMANDS

# cog infrastructure

# @client.command()
# async def load(ctx, extension):
#     client.load_extension(f'cogs.{extension}')
#     print(f'{extension} cog loaded')

# @client.command()
# async def unload(ctx, extension):
#     client.unload_extension(f'cogs.{extension}')
#     print(f'{extension} cog unloaded')

# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
async def start(ctx):
    if client.playing == True: # can't start the game if already playing
        await ctx.send("Game in progress! Cannot start new game.")
        return # return basically ends the bot interaction with a message
    client.playing = True  # we playin now bois
    client.tile_bag = [] # set it up!!
    for letter in distribution:
        for i in range(distribution[letter]):
            client.tile_bag.append(letter)

    # shuffle that bad boy up!
    random.shuffle(client.tile_bag)

    client.table = [] #represents letters on table

    # prompt them for their names
    await ctx.send(f'Enter "{command_prefix}name [name], and use "{command_prefix}play" when all players entered.')

@client.command()
async def rules(ctx):
    await ctx.send('A set of letter tiles is mixed into a bag. One tile at a time is drawn out of the bag and placed face up on the table (the pool). When more than three tiles are in the pool, any player that sees a word (>3 letters) that can be formed by some subset of the letters in the pool (as an anagram, so no using letters multiple times unless they appear multiple times in the pool) simply calls out the word they see.')
                   
    await ctx.send('If the other players agree that the word is a valid anagram of some subset of the letters in the pool, the word is formed and moved in front of that player. Any player can then "steal" that word by using ALL of its letters (in combination with words from the main pool of letters on the table) to create a new word or new words. ALL letters from the stolen word must be used in the new word or words created, although not all letters from the pool need be used. Anagrams that bear significant similarity to the word they are being formed from (for example, adding "S" to make a word plural) are subject to a vote of the players in their best judgement.')
    
@client.command()
async def name(ctx, *, name):
    if client.playing == False:
        await ctx.send(f"You need to start a game using {command_prefix}start first!")
        return

    for playerNode in client.players:
        if playerNode == None: # no players yet!
            break
        if playerNode.data.user == ctx.message.author.display_name:
            await ctx.send(f"{ctx.message.author.display_name}, you can't enter more than once!")
            return   
    
    newPlayer = Player(name, ctx.message.author.display_name)
    
    if client.players.head is None: #grants vip privileges if player is first
        newPlayer.vip = True

    client.players.add_node(Node(newPlayer))
    await ctx.send(f"Added {newPlayer.user} as {newPlayer.name}.") 
        
@client.command()
async def play(ctx):
    if client.playing == False:
        await ctx.send(f"You need to start a game using {command_prefix}start first!")
        return
    
    client.currentPlayer = client.players.head.data
    
    await ctx.send(f"{client.currentPlayer.name}, start us off by drawing a tile using {command_prefix}draw.")
    
    
    
#TODO - printout name list

# @client.command()
# async def disconnect(ctx):
#     client.close()
        
    
    
# actual command that starts bot    
client.run('NzA4NTQ2Nzk3MDg1MzkyOTE2.XrY7oA.guqEvcCgqCJwGRFvXLVEc2BjoIk')


