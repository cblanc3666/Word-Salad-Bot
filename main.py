import random


distribution = {'a': 13, 'b': 3, 'c': 3, 'd': 6, 'e': 18, 'f': 3, 'g': 4, 'h': 3, 'i': 12, 'j': 2, 'k': 2, 'l': 5,
                'm': 3, 'n': 8, 'o': 11, 'p': 3, 'q': 2, 'r': 9, 's': 6, 't': 9, 'u': 6, 'v': 3, 'w': 3, 'x': 2, 'y': 3,
                'z': 2
}


def main():
    # Fill tile bag
    tile_bag = []
    for letter in distribution:
        for i in range(distribution[letter]):
            tile_bag.append(letter)

    players = []
    command = ""


# Player has a name and a list of words
class Player:
    def __init__(self, name, user):
        self.name = name    # The in-game name a player uses
        self.user = user    # The discord username of the player
        self.words = []
        self.vip = False

    def add_word(self, word):
        self.words.append(word)

    def remove_word(self, word):
        self.words.remove(word)

    def is_vip(self):
        vip = True


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
        node = self.head
        nodes = []
        counter = 0
        while True:
            nodes.append(node.data)
            node = node.next
            if node == self.head:   # if all nodes have been added to list
                nodes.append(node.data)
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
        if not self.head:
            self.head = node
            return
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


main()
