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
        self.vip = False #VIP function doesn't actually give the player anything at this point

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


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None    # a Node
        if nodes is not None:   # iterates through iterable nodes and links one to the next
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
            node.next = None   # last node has no next

    def __repr__(self):
        if self.head is None:
            return "List is Empty"
        node = self.head
        nodes = []
        while True:
            nodes.append(str(node.data))
            node = node.next
            if node == None:   # if all nodes have been added to list
                nodes.append(str(node.data))
                break
        nodes.append("...")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while True:
            yield node
            node = node.next
            if node == None:   # iterate until loop is complete
                return

    def add_node(self, node):   #adds node to the "end" of the linked list
        if self.head is None:
            self.head = node
            self.head.next = None
            return "empty"
        for current_node in self:
            if current_node.next == None:  # if the "end" has been reached
                current_node.next = node    #insert node
                node.next = None   # link to none
            
    def push_node(self, node): #adds node to head of linked list
        node.next = self.head
        self.head = node

    def remove_node(self, node):    # remove node from linked list
        for current_node in self:
            if current_node.next.data == node.data:     # if target node is found
                current_node.next = current_node.next.next  # skip over target node
                return
            
    def pop_node(self): # pops from the head
        # assumes there is data to pop
        popped_node = self.head # pop the head
        self.head = self.head.next # make the next node the head
        return popped_node

# Returns the letters that need to be removed from the pool
# If the word is invalid, an empty list is returned
def compare(test_word, new_word, pool):
    pool_letters = []   # list of returned letters
    pool_copy = pool.copy()
    test_list = str_to_list(test_word)
    for letter in new_word:
        if letter in test_list:
            test_list.remove(letter)    # keeps track of which letters have been used already
        elif letter in pool_copy:
            pool_letters.append(letter)
            pool_copy.remove(letter)
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

def print_board(client):
    # takes the client object
    if client.playing == False: # can't print board if no game
        return f'Cannot print board! Start a game using "{command_prefix}start" first.'
    elif client.players.head == None: # can't print board if no players
        return f'Cannot print board! Add players using "{command_prefix}name" first.'
    gameStr = '**Tile pool:**\n'
    gameStr +=f'{client.tablePrint}\n'
    for player in client.players:
        gameStr += f'**{player.data.name}:**\n'
        if len(player.data.words) < 1:
            gameStr += 'No words yet! \n'
            continue
        for playerWord in player.data.words:
            gameStr += f'{player.data.words[playerWord]}\n'
         
    gameStr += f'Enter any anagrams you see as a single word, .\n'
    
    gameStr += f'**{client.currentPlayer.data.name}**, it is your turn to draw using "{command_prefix}draw"'
    
    return gameStr

# @@@@@@@@@@@@@@@@@@@@@@@ Actual Game Events Begin @@@@@@@@@@@@@@@@@@@@@@@@@@
    
client.playing = False; # indicates when it is ok to start the game

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

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return # bot won't reply to itself
    
    if msg.content == ''.join(filter(str.isalpha, msg.content)): # if a single word is entered
        word = msg.content
        if client.playing == False:
            await msg.channel.send(f"You need to start a game using {command_prefix}start first!")
            return
        
        if client.currentPlayer is None:
            await msg.channel.send(f"You need to use the command {command_prefix}play first!")
            return
        
        if client.voting:
            await msg.channel.send("Another vote in progress!")
            return
    
        # clean up the word
        word = word.lower()
    
        valid = False
        repeatWord = False
        gameStr = ''
        stolenWord = None # default is no words stolen
        stolenPlayer = None
    
        # find the nickname of the sender of the message
        author = msg.author.display_name
        for player in client.players:
            if player.data.user == author:
                sender = player  # sender is always a player object
                break
    
        if len(word) > 3: # if this isn't true it won't be valid
            for player in client.players: # check for a steal (prioritize steal over pool formation)
                if len(player.data.words) < 1:
                    continue # no words to check
                # check to see if a word already made allows for creation
                # of the given word
                for playerWord in player.data.words:
                    if word == playerWord:
                        repeatWord = True
                        break
                    poolLetters = compare(playerWord, word, client.table)
                    if len(poolLetters) > 0: # match found
                        valid = True
                        stolenWord = playerWord
                        stolenPlayer = player
                        break
            if not valid and not repeatWord: # we found no steal and the word isn't a repeat
                poolLetters = compare('', word, client.table)
                # if word is entirely a subset of tiles in pool
                if len(poolLetters) > 0: # but we found a pool combo
                    valid = True
                
        if not valid:
            await msg.channel.send(f"So close, **{sender.data.name}**!! That word is not a valid anagram :two_hearts:")
            return
    
        # looks good to the bot - add voting options
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        client.voting = True
    
        await msg.channel.send("Looks good to me, but y'all should vote! You have 2 minutes to approve.")
           
        # returns true if consensus, else false
        def check(reaction, user):
            reaccs = msg.reactions
            if ((reaccs[0].count-1) > client.numPlaying/2) or ((reaccs[1].count-1) > client.numPlaying/2):
                return True
            else:
                return False
    
        # start the wait loop that only breaks when a consensus made
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 120.0, check = check)
        except asyncio.TimeoutError:
            await msg.channel.send("Looks like you couldn't decide! I'm going to move on to the next word now.")
            return
        else:
            # if consensus against 
            if ((msg.reactions[1].count-1) > client.numPlaying/2):
                await msg.channel.send("Looks like the consensus is against you.")
                return
      
        # @@@@@@@@@@@@ THEY GOT THE WORD!
        client.voting = False
        sender.data.add_word(word)
        if stolenPlayer != None:
            del stolenPlayer.data.words[stolenWord] # remove matched word
        gameStr += f"Nice job, **{sender.data.name}**, you got the word **{word.upper()}**! \n"
        
     
        thisMove = [sender, word, poolLetters, [stolenWord], [stolenPlayer]]
        
        # add move to moves list
        client.moves.push_node(Node(thisMove))
        
        # remove requisite tiles from pool    
        for poolLetter in poolLetters:
            client.table.remove(poolLetter)
            client.tablePrint = client.tablePrint.replace(f':regional_indicator_{poolLetter}:', '', 1)
        
        client.currentPlayer = sender
        
        await msg.channel.send(gameStr + print_board(client))
        
    # all of that above only happens if they send a word
    
    await client.process_commands(msg)

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
    client.players = LinkedList() # create list of player objects

    # move storage format is a list of 
    # player that got the word (player object)
    # word they got
    # list of letters used from pool
    # list of people's words used (if any) [TODO: Make this a list]
    # list of people whose words were used (player object) [TODO: Make this a list]
    client.moves = LinkedList()
    client.currentPlayer = None
    client.playing = True  # we playin now bois
    client.voting = False # only true when active voting occurring
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
    
    if client.voting:
        await ctx.send("Wait for this vote to finish and then join!")
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
    
    if client.voting:
        await ctx.send("You're already playing - go vote!")
        return
    
    client.currentPlayer = client.players.head #start us out with the VIP going first
    
    if len(client.table) > 0: # draw has happened, current player should not be head
        await ctx.send(f'You already made this command! {client.currentPlayer.data.name}, use "{command_prefix}draw" to continue gameplay.')
        return
    
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
    
    if client.currentPlayer is None:
        await ctx.send(f"You need to use the command {command_prefix}play first!")
        return
    
    if ctx.message.author.display_name != client.currentPlayer.data.user:
        await ctx.send("Oi! It's not your turn!")
        return
    
    if client.voting:
        await ctx.send("You can't draw right now - go vote!")
        return
    
    newTile = client.tileBag.pop()
    
    # change table output
    client.table.append(newTile)
    client.tablePrint += f':regional_indicator_{newTile}:'
    
    # add move to moves list
    client.moves.push_node(Node([None, None, [newTile], [], []]))
    
    # move to next player
    if client.currentPlayer.next == None:
        client.currentPlayer = client.players.head
    else:
        client.currentPlayer = client.currentPlayer.next

    await ctx.send(print_board(client))
    
@client.command()
async def undo(ctx):
    if client.moves.head is None:
        await ctx.send("No moves to undo!")
        return
        
    if client.voting:
        await ctx.send("You can't undo right now - go vote!")
        return
    
    move = client.moves.pop_node().data
    if move[0] == None: # the move to be undone is a draw move
        client.table.remove(move[2][0]) # remove from table
        client.tablePrint = client.tablePrint.replace(f':regional_indicator_{move[2][0]}:', '', 1)
        client.tileBag.append(move[2][0])
        
        await ctx.send(print_board(client))
        return
    
    # remove word from player
    for player in client.players:
        if player.data.user == move[0].data.user: # find player that got the word
            player.data.remove_word(move[1])
    
    # put tiles back on table
    for poolLetter in move[2]:
        client.table.append(poolLetter)
        client.tablePrint += f':regional_indicator_{poolLetter}:'
    
    # return words to other people
    for i in range(len(move[3])): # loops over number of words they used. it's 1 if no word stolen
        if move[3][i] == None:
            break
        for player in client.players:
            if player.data.user == move[4][i].data.user: #find player whose word stolen
                player.data.add_word(move[3][i]) #give them word back
    
    await ctx.send(print_board(client))


@client.command()
async def show(ctx):
    await ctx.send(print_board(client))

#BUG FIX - when you steal a word but people vote you down, the word you steal is still deleted
#BUG FIX - undo cannot bring back words that were deleted by the previous bug
#BUG FIX - when you steal a word and use tiles from the pool, those tiles aren't properly removed
#TODO - Lock other people out of drawing or saying words when voting is happening on one person's word
#TODO - two word melds into anagrams
#TODO - disconnect command
#TODO - show number of tiles remaining, game end logistics, scoring
#TODO - something to prevent other people for drawing for another player UNLESS we have to (timer runs out and they're afk, or we votekick them)
#TODO validate against names with asterisks or underscores or whatever fucky wucky stuff (quotes, backslashes - try to limit to letters and numbers). NO REPEAT NAMES
    #TODO prevent people having the same names
#TODO: You will probably never do this, but use a dictionary instead of whatever the fuck you have in there right now to preserve the relation between player names and nicknames'
#TODO: allow VIP to designate new VIP, make it so that it won't accept a draw from anyone except the person whose turn it is (OR VIP OVERRIDE)
    
#BUG FIX: Won't let you rearrange word in place (change WAYFAIR to FAIRWAY) - ONLY LET PEOPLE DO THIS FOR THEIR OWN WORDS, and don't make it jump to their turn to draw if it's just a rearrange
    

# @client.command()
# async def disconnect(ctx):
#     client.close()
        
    
    
# actual command that starts bot    
client.run('NzA4NTQ2Nzk3MDg1MzkyOTE2.XrY7oA.guqEvcCgqCJwGRFvXLVEc2BjoIk')


