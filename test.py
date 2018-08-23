import Linkedlist as Ll
link = Ll.Linkedlist()
for i in range(9):
    link.append(i**2)
cur = link.head
while True:
    print(link.get_index(cur), cur.data)
    if cur.data % 2 == 0:
        cur = cur.next
        link.delete(cur.pre)
    else:
        cur = cur.next
        if cur == link.head:
            break

cur = link.head
while True:
    print(link.get_index(cur), cur.data)
    cur = cur.next
    if cur == link.head:
        break