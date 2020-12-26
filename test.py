from main import compare, Player, Node, CircularLinkedList
import random

distribution = {'a': 13, 'b': 3, 'c': 3, 'd': 6, 'e': 18, 'f': 3, 'g': 4, 'h': 3, 'i': 12, 'j': 2, 'k': 2, 'l': 5,
                'm': 3, 'n': 8, 'o': 11, 'p': 3, 'q': 2, 'r': 9, 's': 6, 't': 9, 'u': 6, 'v': 3, 'w': 3, 'x': 2, 'y': 3,
                'z': 2
}

def test():
    # Test all of the possible outcomes of a comparison
    pool=['r', 'a', 'c', 'd', 'x', 'z']
    # Comparison is valid
    print("LUMEN -> NUMERAL: {}".format(compare("lumen", "numeral", pool)))  # Returns ['r', 'a']
    # No tiles from the pool are used
    print("LISTEN -> SILENT: {}".format(compare("listen", "silent", pool)))  # Returns []
    # At least one letter does not show in test_word or in pool
    print("ELITE -> ELICITED: {}".format(compare("elite", "elicited", pool)))  # Returns []
    # Not all of the letters in test_word are used
    print("ULTIMATE -> LAME: {}".format(compare("ultimate", "lame", pool)))  # Returns []
    print()
    print()

    # Test adding and removing words and accessing class variables from Player
    p1=Player("Carson")
    p1.add_word("neat")
    p1.add_word("epic")
    p1.add_word("cool")
    print("{}: {}".format(p1.name, p1.words))
    print()
    p2=Player("Chase")
    p2.add_word("discombobulate")
    p1.remove_word("cool")
    print("{}: {}".format(p1.name, p1.words))
    print("{}: {}".format(p2.name, p2.words))
    print()
    print()

    llist=CircularLinkedList(['a', 'b', 'c', 'd', 'e'])
    print(llist)

    llist.add_node(Node('f'))
    print(llist)

    llist.remove_node(Node('b'))
    print(llist)
    print()
    print()

    llist2 = CircularLinkedList()
    print(llist2)
    llist2.add_node(Node('a'))
    print(llist2)
    llist2.add_node(Node('b'))
    print(llist2)

def test1():
    llist = CircularLinkedList([Player('name', 'username'), Player('name1','username1')])    
    player = llist.head
    player.data.add_word('lol')
    
def test2():
    tile_bag = [] # set it up!!
    for letter in distribution:
        for i in range(distribution[letter]):
            tile_bag.append(letter)
            
    print(tile_bag)

    random.shuffle(tile_bag)
    
    print(tile_bag)


def test3():
    print(compare(['d', 'e', 'a', 'l'], 'dealers', ['r','s','e']))

test3()