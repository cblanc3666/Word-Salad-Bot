# commands are start, name [name],

import random
import discord
from discord.ext import commands

command_prefix = '$'

# create an instance of a client object - the bot is the client
client = commands.Bot(command_prefix)

distribution = {'a': 13, 'b': 3, 'c': 3, 'd': 6, 'e': 18, 'f': 3, 'g': 4, 'h': 3, 'i': 12, 'j': 2, 'k': 2, 'l': 5,
                'm': 3, 'n': 8, 'o': 11, 'p': 3, 'q': 2, 'r': 9, 's': 6, 't': 9, 'u': 6, 'v': 3, 'w': 3, 'x': 2, 'y': 3,
                'z': 2
}


GUILD = "Messing with Bots"

playing = False;

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
        counter = 0
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
    
playing = False; # indicates when it is ok to start the game
players = CircularLinkedList() # create list

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

@client.command()
async def start(ctx):
    if playing == True: # can't start the game if already playing
        await ctx.send("Game in progress! Cannot start new game.")
        return # return basically ends the bot interaction with a message
    playing = True  # we playin now bois
    tile_bag = [] # set it up!!
    for letter in distribution:
        for i in range(distribution[letter]):
            tile_bag.append(letter)

    # prompt them for their names
    await ctx.send(f'Enter "{command_prefix}name [name], and use "play" when all players entered.')
    return
    
@client.command()
async def name(ctx, *, name):
    await ctx.send(f"What's poppin, {name}")
    

# @client.command()
# async def disconnect(ctx):
#     client.close()
    
#     if playing == False: # all commands beyond this point apply only while playing
#         # if the users aren't playing and use any command other than start, 
#         # this will prompt them to start a game
#         await message.channel.send("Start a game with 'start' first!")
#         return
       
#     # allows players to enter their names
#     if command.lower() == 'name':
#         if len(inputList) < 2:
#             await message.channel.send("Enter a name!")
#             return
#         name = ' '.join(inputList[1:]) # concatenates all but the first word
#         # this will give all they entered except for the name command
        
#         player = Player(name, message.author)
#         if players.head is None: # grants vip privileges if player is first
#             player.vip = True
#         players.add_node(Node(player))
#         await message.channel.send(name) # TODO: add a message with list of players
        
    
# actual command that starts bot    
client.run('NzA4NTQ2Nzk3MDg1MzkyOTE2.XrY7oA.guqEvcCgqCJwGRFvXLVEc2BjoIk')


