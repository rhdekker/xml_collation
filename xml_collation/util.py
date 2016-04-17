class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]

