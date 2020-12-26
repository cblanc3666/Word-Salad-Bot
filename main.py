import random
import discord
import asyncio
from discord.ext import commands

command_prefix = '.'

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
        self.words = {}
        self.vip = False

    def __str__(self):
        rtn = "{}: {}".format(self.user, self.name)
        if self.vip:
            rtn += " (VIP)"
        return rtn

    def add_word(self, word):
        wordStr = ''
        for letter in str_to_list(word):
            wordStr += f':regional_indicator_{letter}:'
            
        self.words[word] = wordStr

    def remove_word(self, word):
        if word in self.words:
            del self.words[word]


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
    client.tileBag = [] # set it up!!
    client.tablePrint = '' # output string
    for letter in distribution:
        for i in range(distribution[letter]):
            client.tileBag.append(letter)

    # shuffle that bad boy up!
    random.shuffle(client.tileBag)

    client.table = [] #represents letters on table
    client.numPlaying = 0 #represents number of players

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
    client.numPlaying += 1
    await ctx.send(f'Added **{newPlayer.user}** as **{newPlayer.name}**. \nYou can check who is playing using "{command_prefix}players." \nUse "{command_prefix}play" when all players have entered.')
        
@client.command()
async def play(ctx):
    if client.playing == False:
        await ctx.send(f"You need to start a game using {command_prefix}start first!")
        return
    
    if len(client.table) > 0: # draw has happened, current player should not be head
        await ctx.send(f'You already made this command! {client.currentPlayer.data.name}, use "{command_prefix}draw" to continue gameplay.')
        return
    
    client.currentPlayer = client.players.head
    
    await ctx.send(f'**{client.currentPlayer.data.name}**, start us off by drawing a tile using "{command_prefix}draw".')
    
@client.command()
async def players(ctx):
    if client.players.head is None:
        await ctx.send('No one is playing yet.')
        return
        
    for player in client.players:
        await ctx.send(player.data)
        
@client.command()
async def draw(ctx):
    if client.playing == False:
        await ctx.send(f"You need to start a game using {command_prefix}start first!")
        return
    
    if ctx.message.author.display_name != client.currentPlayer.data.user:
        await ctx.send("Oi! It's not your turn!")
        return
    
    gameStr = ''
    newTile = client.tileBag.pop(0)
    client.table.append(newTile)
    client.tablePrint += f':regional_indicator_{newTile}:'
    client.currentPlayer = client.currentPlayer.next
    
    gameStr += '**Tile pool:**\n'
    gameStr +=f'{client.tablePrint}\n'
    
    for player in client.players:
        gameStr += f'**{player.data.name}:**\n'
        if len(player.data.words) < 1:
            gameStr += 'No words yet! \n'
            continue
        for playerWord in player.data.words:
            gameStr += f'{player.data.words[playerWord]}\n'
         
    gameStr += f'Use "{command_prefix}word [word]" to enter any anagrams you see.\n'
    
    gameStr += f'**{client.currentPlayer.data.name}**, it is your turn to draw using "{command_prefix}draw"'
    
    await ctx.send(gameStr)
    
@client.command()
async def word(ctx, word):
    if client.playing == False:
        await ctx.send(f"You need to start a game using {command_prefix}start first!")
        return
    
    # clean up the word
    word = word.lower()
    
    valid = False
    gameStr = ''
    
    # find the nickname of the sender of the message
    author = ctx.message.author.display_name
    for player in client.players:
        if player.data.user == author:
            sender = player  # sender is always a player object
            break
    
    if len(word) > 3: # if this isn't true it won't be valid
        # if word is entirely a subset of tiles in pool
        poolLetters = compare('', word, client.table)
        if len(poolLetters) > 0:
            valid = True
    
        for player in client.players:
            if len(player.data.words) < 1:
                continue # no words to check
            # check to see if a word already made allows for creation
            # of the given word
            for playerWord in player.data.words:
                poolLetters = compare(playerWord, word, client.table)
                if len(poolLetters) > 0: # match found
                    valid = True
                    del player.data.words[playerWord] # remove matched word
                    break
    
    if not valid:
        await ctx.send(f"So close, **{sender.data.name}**!! That word is not a valid anagram :two_hearts:")
        return
    
    # add voting options
    await ctx.message.add_reaction('👍')
    await ctx.message.add_reaction('👎')
    
    await ctx.send("Looks good to me, but y'all should vote! You have 2 minutes to approve.")
       
    # returns true if consensus, else false
    def check(reaction, user):
        reaccs = ctx.message.reactions
        if ((reaccs[0].count-1) > client.numPlaying/2) or ((reaccs[1].count-1) > client.numPlaying/2):
            return True
        else:
            return False
    
    # start the wait loop that only breaks when a consensus made
    try:
        reaction, user = await client.wait_for('reaction_add', timeout = 120.0, check = check)
    except asyncio.TimeoutError:
        await ctx.channel.send("Looks like you couldn't decide! I'm going to move on to the next word now.")
        return
    else:
        # if consensus against 
        if ((ctx.message.reactions[1].count-1) > client.numPlaying/2):
            await ctx.channel.send("Looks like the consensus is against you.")
            return
  
    sender.data.add_word(word)
    gameStr += f"Nice job, **{sender.data.name}**, you got the word **{word.upper()}**! \n"
    
    # remove requisite tiles from pool    
    for poolLetter in poolLetters:
        client.table.remove(poolLetter)
        client.tablePrint = client.tablePrint.replace(f':regional_indicator_{poolLetter}:', '')
    
    client.currentPlayer = sender
    
    gameStr += f'**{client.currentPlayer.data.name}**, it is your turn to draw using "{command_prefix}draw"'
            
    await ctx.send(gameStr)
        

#TODO - two word melds into anagrams
#TODO - disconnect command
#TODO - show number of tiles remaining, game end logistics, scoring
#TODO - voting functionality so players can determine whether a word is legitimate
#TODO - undo functionality to undo a certain move 
#TODO - something to prevent other people for drawing for another player UNLESS we have to (timer runs out and they're afk, or we votekick them)
#TODO validate against names with asterisks or underscores or whatever fucky wucky stuff (quotes, backslashes - try to limit to letters and numbers). NO REPEAT NAMES
#TODO add a command that tells everyone whose turn it is
#TODO: is there a way to just have the bot scan every one-word message in the chat for acceptable answers? To avoid the need for .word entirely? Otherwise, command prefix of nothing and maybe "w" instead of "word"
#TODO: You will probably never do this, but use a dictionary instead of whatever the fuck you have in there right now to preserve the relation between player names and nicknames
    
#BUG FIX: ARIA in my game with joel and lyle
#BUG FIX: Won't let you rearrange word in place (change WAYFAIR to FAIRWAY) - ONLY LET PEOPLE DO THIS FOR THEIR OWN WORDS, and don't make it jump to their turn to draw if it's just a rearrange
    

# @client.command()
# async def disconnect(ctx):
#     client.close()
        
    
    
# actual command that starts bot    
client.run('NzA4NTQ2Nzk3MDg1MzkyOTE2.XrY7oA.guqEvcCgqCJwGRFvXLVEc2BjoIk')


