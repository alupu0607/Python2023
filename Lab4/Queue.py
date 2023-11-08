class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return None

    def size(self):
        return len(self.items)

# Example usage:
queue = Queue()
queue.push(1)
queue.push(2)
queue.push(3)

print(queue.peek())  # Output: 1
print(queue.pop())   # Output: 1
print(queue.pop())   # Output: 2
print(queue.pop())   # Output: 3
print(queue.pop())   # Output: None
