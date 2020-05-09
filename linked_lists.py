from collections import deque


def main():
    llist = CircularLinkedList(['a', 'b', 'c', 'd', 'e'])
    print(llist)

    llist.add_node(Node('f'))
    print(llist)

    llist.remove_node(Node('b'))
    print(llist)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None    # a Node

    def __repr__(self):
        return self.data


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


main()