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


class CircularLinkedList:
    def __init__(self, nodes=None):
        self.head = None    # a Node
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
            node.next = self.head

    def __repr__(self):
        node = self.head
        nodes = []
        counter = 0
        while True:
            nodes.append(node.data)
            node = node.next
            if node == self.head:
                nodes.append(node.data)
                break
        nodes.append("...")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while True:
            yield node
            node = node.next
            if node == self.head:
                return

    def add_node(self, node):
        if not self.head:
            self.head = node
            return
        for current_node in self:
            if current_node.next == self.head:
                current_node.next = node
                node.next = self.head

    def remove_node(self, node):
        for current_node in self:
            if current_node.next.data == node.data:
                current_node.next = current_node.next.next
                return


# class LinkedList:
#     def __init__(self, nodes=None):
#         self.head = None
#         if nodes is not None:
#             node = Node(data=nodes.pop(0))
#             self.head = node
#             for elem in nodes:
#                 node.next = Node(data=elem)
#                 node = node.next
#
#     def __iter__(self):
#         node = self.head
#         while node is not None:
#             yield node
#             node = node.next
#
#     def __repr__(self):
#         node = self.head
#         nodes = []
#         while node is not None:
#             nodes.append(node.data)
#             node = node.next
#         nodes.append("None")
#         return " -> ".join(nodes)
#
#     def add_first(self, node):
#         node.next = self.head
#         self.head = node
#
#     def add_last(self, node):
#         if not self.head:
#             self.head = node
#             return
#         for current_node in self:
#             pass
#         current_node.next = node


main()
