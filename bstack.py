# bstack.py
# Simple Stack implementation for Magical Flask

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Push an item onto the stack"""
        self.items.append(item)

    def pop(self):
        """Pop an item off the stack"""
        if not self.isEmpty():
            return self.items.pop()
        else:
            return None

    def peek(self):
        """Look at the top item without removing it"""
        if not self.isEmpty():
            return self.items[-1]
        else:
            return None

    def isEmpty(self):
        """Check if the stack is empty"""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the stack"""
        return len(self.items)

    def __str__(self):
        """Return a space-separated string of items (bottom → top)"""
        return " ".join(self.items)
