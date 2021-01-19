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


GUILD = "The Domino & Machine Community"
client.playChannel = None

# @@@@@@@@@@@@@@@@@@@@@@@ Define Classes @@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Player has a name and a list of words
class Player:
    def __init__(self, name, user=None):
        self.name = name    # The in-game name a player uses
        self.user = user    # The discord username of the player
        self.words = {}
        self.score = 0
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
    if len(test_list) == 0:   # If all of the letters in test_word were used,
        if len(pool_letters) > 0:
            return pool_letters # if some letters from the pool were used, comparison is valid
        else:
            return ['1'] # return if rearrangement
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
    gameStr = ''

    for player in client.players:
        gameStr += f'**{player.data.name}:**\n'
        if len(player.data.words) < 1:
            gameStr += 'No words yet! \n'
            continue
        for playerWord in player.data.words:
            gameStr += f'{player.data.words[playerWord]}\n'
            if len(gameStr) >= 1700 and '@@@' not in gameStr: # prevent exceeding 2000 limit
                gameStr += '@@@' # TODO THIS IS NOT ELEGANT
        
    gameStr += '@@@'
    gameStr += '**Tile pool:**\n'  
    gameStr +=f'{client.tablePrint}\n'
        
    gameStr += f'Enter any anagrams you see as a single word.\n'
    
    gameStr += f'**{client.currentPlayer.data.name}**, it is your turn to draw using "{command_prefix}draw"'
    
    gameStrLst = gameStr.split('@@@')
    
    return gameStrLst

# check to see if word can be stolen from a combination of two or more on the table
def check_steal(client, allWords, word):
    wordLetters = str_to_list(word)
    usableWords = allWords.copy()
    for playerWord in allWords.keys():
        for letter in playerWord:
            if letter not in wordLetters: # player word can't be stolen - contains letter that was not entered
                del usableWords[playerWord]
                break
    
    if len(usableWords) < 2: # no combo possible
        return ([], [], [])
    
    allWordList = list(usableWords.keys())
    
    for i in range(len(usableWords)): # for each word
        for j in range(i+1, len(usableWords)): # all other words
            word1 = allWordList[i]
            word2 = allWordList[j]
            if len(word1) + len(word2) > len(word):
                continue
            poolLetters = compare(word1+word2, word, client.table) #test those combined bois
            if len(poolLetters) > 0:
                stolenWords = [word1, word2]
                stolenPlayers = [usableWords[word1], usableWords[word2]]
                if '1' in poolLetters:
                    poolLetters.remove('1')
                return (poolLetters, stolenWords, stolenPlayers)
            
    # if we went through all of the words but no dice
    return ([], [], [])


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
    
    if msg.content == ''.join(filter(str.isalpha, msg.content)) and msg.channel == client.playChannel: # if a single word is entered in the gameplay channel
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
        loopBreak = False
        gameStr = ''
        allWords = {} #words as keys, values as players
        stolenWords = [] # default is no words stolen
        stolenPlayers = []
        poolLetters = []
    
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
                    if word == playerWord: # check for repeats first because it makes the word invalid if true
                        repeatWord = True
                        loopBreak = True
                        break
                    
                    allWords[playerWord] = player
                    
                    poolLetters = compare(playerWord, word, client.table)
                    if '1' in poolLetters: # word is a direct anagram with no pool addition
                        poolLetters.remove('1')
                    if len(poolLetters) > 0: # match found, valid steal
                        valid = True
                        loopBreak = True
                        stolenWords = [playerWord]
                        stolenPlayers = [player]
                        break
                if loopBreak:
                    break
            
            if not valid and not repeatWord: # we found no steal and the word isn't a repeat, check pool formation
                poolLetters = compare('', word, client.table)
                # if word is entirely a subset of tiles in pool
                if len(poolLetters) > 0 and poolLetters[0] != '1': # but we found a pool combo
                    valid = True
            
            if not valid and not repeatWord: # check two word meld
                (poolLetters, stolenWords, stolenPlayers) = check_steal(client, allWords, word)
                if len(stolenWords) > 0:
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
            client.voting = False
            return
        else:
            
            # if consensus against 
            if ((msg.reactions[1].count-1) > client.numPlaying/2):
                await msg.channel.send("Looks like the consensus is against you.")
                client.voting = False
                return
      
        # @@@@@@@@@@@@ THEY GOT THE WORD!
        client.voting = False
        sender.data.add_word(word)
        sender.data.score += len(word)
        if stolenPlayers != []:
            for i in range(len(stolenPlayers)):
                stolenPlayer = stolenPlayers[i]
                del stolenPlayer.data.words[stolenWords[i]] # remove matched word
                stolenPlayer.data.score -= len(stolenWords[i])
        gameStr += f"Nice job, **{sender.data.name}**, you got the word **{word.upper()}**! \n"
        
     
        thisMove = [sender, word, poolLetters, stolenWords, stolenPlayers]
        
        # add move to moves list
        client.moves.push_node(Node(thisMove))
        
        # remove requisite tiles from pool    
        for poolLetter in poolLetters:
            client.table.remove(poolLetter)
            client.tablePrint = client.tablePrint.replace(f':regional_indicator_{poolLetter}:', '', 1)
        
        client.currentPlayer = sender
        
        await msg.channel.send(gameStr)
        gameStrLst = print_board(client)
        for i in range(len(gameStrLst)):
            if gameStrLst[i] != '':
                await msg.channel.send(gameStrLst[i])
        return
        
    # all of that above only happens if they send a word
    
    if 'start' in msg.content or msg.channel == client.playChannel:
        await client.process_commands(msg) # all other commands
    
    # ignore commands outside of relevant channel

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
    client.playChannel = ctx.channel # only read commands in this channel

    # move storage format is a list of 
    # player that got the word (player object)
    # word they got
    # list of letters used from pool
    # list of people's words used (if any)
    # list of people whose words were used (player object)
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
    
    if len(client.tileBag) != 144: #draw has happened already
        await ctx.send(f'You already made this command! {client.currentPlayer.data.name}, use "{command_prefix}draw" to continue gameplay.')
        return
    
    client.currentPlayer = client.players.head #start us out with the VIP going first

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
    
    if ctx.message.author.display_name != client.currentPlayer.data.user: # if it's not their turn
        for player in client.players: # find the player who did send
            if player.data.user == ctx.message.author.display_name:
                sender = player.data
                if not sender.vip: # if they're not VIP
                    await ctx.send("Oi! It's not your turn!")
                    return
                break # if the sender was VIP
                
        # otherwise, let them override
        await ctx.send("It's not your turn. Do you want to VIP override?")
        await ctx.message.add_reaction('👍')
        await ctx.message.add_reaction('👎')
        client.voting = True
        
        def check(reaction, user):
            if reaction != '👍' and reaction != '👎':
                return False
            elif user.display_name != sender.user: # if it's not the person who drew that reacted
                return False
            return True
        
        # start the wait loop that only breaks when a consensus made
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
        except asyncio.TimeoutError:
            await ctx.message.channel.send("You did not confirm in time.")
            client.voting = False
            return
        else:
            client.voting = False
            # if they thumbs down
            async for user in ctx.message.reactions[1].users():
                if user.display_name == sender.user:
                    await ctx.message.channel.send("Ok, no override.")
                    return
            # if they didn't thumb down, they thumbed up, so we draw
            await ctx.message.channel.send("Ok, override.")
            
    if client.voting:
        await ctx.send("You can't draw right now - go vote!")
        return
    
    if len(client.tileBag) == 0:
        await ctx.send(f"Tile bag is empty! Make any last anagrams you see, and then use {command_prefix}end to end the game.")
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

    gameStrLst = print_board(client)
    for i in range(len(gameStrLst)):
        if gameStrLst[i] != '':
            await ctx.send(gameStrLst[i])
    
@client.command()
async def undo(ctx):
    if not client.playing:
        await ctx.send("Can't undo. No game happening.")
        return
    
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
        
        gameStrLst = print_board(client)
        for i in range(len(gameStrLst)):
            if gameStrLst[i] != '':
                await ctx.send(gameStrLst[i])
        return
    
    # remove word from player
    for player in client.players:
        if player.data.user == move[0].data.user: # find player that got the word
            player.data.remove_word(move[1])
            player.data.score -= len(move[1])
    
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
                player.data.score += len(move[3][i])
    
    gameStrLst = print_board(client)
    for i in range(len(gameStrLst)):
        if gameStrLst[i] != '':
            await ctx.send(gameStrLst[i])
    return


@client.command()
async def show(ctx):
    gameStrLst = print_board(client)
    for i in range(len(gameStrLst)):
        if gameStrLst[i] != '':
            await ctx.send(gameStrLst[i])
    
@client.command()
async def stats(ctx):
    await ctx.send(gen_stats(''))
 
def gen_stats(gameStr):
    if not client.playing:
        return 'No game in progress.'
    for player in client.players:
        gameStr += f'{player.data.name}: {player.data.score} points \n'
        
    gameStr += f'Letters left in bag: {len(client.tileBag)} \n'
    return gameStr

@client.command()
async def end(ctx):
    if not client.playing:
        await ctx.send('No game to end!')
        return
    if client.currentPlayer is None:
        await ctx.send(f"You need to use the command {command_prefix}play first!")
        return
    
    gameStr = '**FINAL BOARD:**\n'
    gameStr+= 'Tile pool: \n'
    gameStr +=f'{client.tablePrint}\n'
    await ctx.send(gameStr) #TODO fix this
    client.playing = False
    gameStr = ''
    for player in client.players:
        gameStr += f'**{player.data.name}:**\n'
        if len(player.data.words) < 1:
            gameStr += 'No words yet! \n'
            continue
        for playerWord in player.data.words:
            gameStr += f'{player.data.words[playerWord]}\n'
            if len(gameStr) >= 1700: # prevent exceeding 2000 limit
                gameStr += '@@@' # TODO THIS IS NOT ELEGANT
        await ctx.send(gameStr) #TODO Fix this
        gameStr = ''

    gameStr += '\n**FINAL SCORES**\n'
    for player in client.players:
        gameStr += f'{player.data.name}: {player.data.score} points \n'

    await ctx.send(gameStr)

@client.command()
async def commands(ctx):
    gameStr = f'**Prefix all of these with {command_prefix}** \n \n'
    gameStr += 'name [name] will add you as a player with the requested nickname. \n'
    gameStr += 'play will start gameplay. Only use this one once, after all players have been added at the beginning. (You can add more players as the game goes on.) \n'
    gameStr += 'draw will draw a tile from the bag. Only use this after using the play command. \n'
    gameStr += '**Any single word message in this channel will be considered as an anagram.** Anagrams sent before the play command will be invalid. \n'
    gameStr += 'show will show the current board and prompt the next person to go. \n'
    gameStr += 'players will show a list of current players \n'
    gameStr += 'rules will tell you the rules of the game. \n'
    gameStr += 'undo will undo the last move. \n'
    gameStr += 'stats will show scores and number of tiles remaining in the bag. \n'
    gameStr += 'end will end the game at any point and show the final score and table. \n'
    gameStr += 'commands will list game commands.'
    
    await ctx.send(gameStr)

#TO TEST - can VIP override to draw? NOPE, FIX IT
#TO TEST - can two word melds include from multiple players?

#TODO: when you undo, it should reset whose turn it is
#TODO: use embedded messages to get around 2000 character issue
#TODO: add a command to either let players vote others out, and also a .leave command, and a remove command for VIP only
#TODO: make it so that the bot doesn't interact with (vote, take words from) people who aren't playing. only let them use the name command
#TODO: prevent multiple simultaneous end commands? (maybe limit to VIP)
#TODO: fix scoring (score of a word is equal to number of letters minus 2)
#TODO: sometimes the bot does the 2 min reminder for failed votes when multiple are simultaneous. try to end all votes that are happening so that doesn't clutter the chat
#TODO: Maybe change the length of the game based on how many people are playing. Could even add a speed game with fewer tiles. Basically have the same distribution but don't use all of the tiles when fewer people play.
#TODO: Order stats in descending score order
#TODO: finish VIP handoff command (one person to another) - also allow VIP override of long votes. add VIP validation for undo
#TODO: prevent show command during vote!!
#TODO validate against names with asterisks or underscores or whatever fucky wucky stuff (quotes, backslashes - try to limit to letters and numbers). NO REPEAT NAMES
#TODO prevent people having the same names
#TODO add more fun stats like number of steals per player, number of steals overall, etc
#TODO 3+ word melds
#TO CONSIDER - what if there are multiple different two word melds or multiple different stealable words for an entry?
    
#TODO - disconnect command
#TODO - add in a way to save and load from savefiles
#BUG FIX: Won't let you rearrange word in place (change WAYFAIR to FAIRWAY) - ONLY LET PEOPLE DO THIS FOR THEIR OWN WORDS, and don't make it jump to their turn to draw if it's just a rearrange

#TODO: You will probably never do this, but use a dictionary instead of whatever the fuck you have in there right now to preserve the relation between player names and nicknames
    

    

# @client.command()
# async def disconnect(ctx):
#     client.close()
        
    
    
# actual command that starts bot    
client.run('NzA4NTQ2Nzk3MDg1MzkyOTE2.XrY7oA.guqEvcCgqCJwGRFvXLVEc2BjoIk')


