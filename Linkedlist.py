class Node():
    def __init__(self, data):
        self.data = data
        self.next = None

class Linkedlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    #append item at the end of Linkedlist
    def append(self, item):
        new_node = Node(item)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
            self.tail.next = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head
        self.length += 1

    #insert item after cur
    def insert(self, item, cur):
        new_node = Node(item)
        new_node.next = cur.next
        cur.next = new_node
        self.length += 1
        if cur == self.tail:
            self.tail = cur.next

if __name__ == '__main__':
    s = Linkedlist()
    P = [[i, i*i] for i in range(8)]
    for i in range(4):
        s.append(P[i])
    print(s.length)
    cur = s.head
    for i in range(s.length):
        print(cur.data)
        cur = cur.next
    print('')

    cur = s.head
    s.insert(P[4], cur)
    print(s.length)
    for i in range(s.length):
        print(cur.data)
        cur = cur.next
    print('')

    cur = s.head
    for i in range(20):
        print(cur.data)
        cur = cur.next