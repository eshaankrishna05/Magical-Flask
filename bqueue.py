# bqueue.py
# Simple Bounded Queue implementation for Magical Flask

class BoundedQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def enqueue(self, item):
        """Add an item to the queue if not full"""
        if not self.isFull():
            self.items.append(item)

    def dequeue(self):
        """Remove and return the first item in the queue"""
        if not self.isEmpty():
            return self.items.pop(0)
        else:
            return None

    def isEmpty(self):
        """Check if the queue is empty"""
        return len(self.items) == 0

    def isFull(self):
        """Check if the queue is full"""
        return len(self.items) == self.capacity

    def size(self):
        """Return the number of items in the queue"""
        return len(self.items)

    def __str__(self):
        """Return a space-separated string of items"""
        return " ".join(self.items)
