import random
import discord

distribution = {'a': 13, 'b': 3, 'c': 3, 'd': 6, 'e': 18, 'f': 3, 'g': 4, 'h': 3, 'i': 12, 'j': 2, 'k': 2, 'l': 5,
                'm': 3, 'n': 8, 'o': 11, 'p': 3, 'q': 2, 'r': 9, 's': 6, 't': 9, 'u': 6, 'v': 3, 'w': 3, 'x': 2, 'y': 3,
                'z': 2
}

# read in bot's discord token from an outside file
TOKEN = open("token.txt", "r").read()

GUILD = "Messing with Bots"

# create an instance of a client object - the bot is the client
client = discord.Client()

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


@client.event
# runs every time a message is sent in a channel the bot can see
async def on_message(message):
    # this is true if the bot is the author of the message
    # this prevents the bot from reacting to its own messages
    if message.author == client.user:
        return
    
    # ignores non-command messages
    if not message.content.startswith('$'):
        return
    
    command = message.content[1:] # removes dollar sign from command message
    
    print(command)
    
    # def main():
    #     # Fill tile bag
    #     tile_bag = []
    #     for letter in distribution:
    #         for i in range(distribution[letter]):
    #             tile_bag.append(letter)
    
    #     players = CircularLinkedList()
    #     response = ""
    #     while True:
    #         response = input("What is your name and username? (user:response) ") # TO BE REPLACED WITH DISCORD.PY
    
    #         # Checks for invalid input
    #         if ':' not in response:
    #             print("Invalid Input: ':' not in input")
    #         elif response[-1] == ':':
    #             print("Invalid Input: user not specified")
    #         elif response[0] == ':':
    #             print("Invalid Input: response not included")
    
    #         else:
    #             response_tup = split(response)
    
    #             # Checks to see if game is ready to be played
    #             if response_tup[1] == "!play":
    #                 break
    
    #             # Creates player and adds it to players
    #             player = Player(response_tup[1], response_tup[0])
    #             if players.head is None:    #grants vip privileges if player is first in players
    #                 player.vip = True
    #             players.add_node(Node(player))
    #             print(players)
    
    #         print()


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


#main()
    
client.run(TOKEN)
