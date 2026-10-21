"""
Author: huiwon choi
Last updated: 10/18/2026
Description: Custom Queue (FIFO) and Stack (LIFO) classes used by the
BFS and DFS searches in game_data.py. Both classes share the same method
names (add, remove, is_empty) so the search code can use either one.
"""

class Queue():
    def __init__(self):
        self.items = []

    def add(self, item) -> None:
        """ "Enqueue" the item to the end of the queue """
        self.items.append(item)

    def remove(self):
        """ "Dequeue" the item from the front of the queue and return it """
        return self.items.pop(0)

    def is_empty(self) -> bool:
        """ Returns whether or not the queue is empty """
        return len(self.items) == 0


class Stack():
    def __init__(self):
        self.items = []

    def add(self, item) -> None:
        """ Push an item to the top (end) of the stack """
        self.items.append(item)

    def remove(self):
        """ Pop the item from the top (end) of the stack and return it """
        return self.items.pop()

    def is_empty(self) -> bool:
        """ Returns whether or not the stack is empty """
        return len(self.items) == 0