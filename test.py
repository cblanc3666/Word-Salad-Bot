from main import compare, Player, Node, CircularLinkedList


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


test()
