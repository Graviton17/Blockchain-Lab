import hashlib
from typing import Optional

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

class Node:
    def __init__(self, data: str, prev_hash: str, prev: Optional["Node"]):
        self.data = data
        self.prev_hash = prev_hash
        self.hash = sha256(prev_hash + data)
        self.prev: Optional["Node"] = prev
        self.next: Optional["Node"] = None

class AppendOnlyList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        prev_hash = self.tail.hash if self.tail else "0" * 64
        node = Node(data, prev_hash, self.tail)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        return node

    def find_by_hash(self, h: str) -> Optional["Node"]:
        cur = self.head
        while cur:
            if cur.hash == h:
                return cur
            cur = cur.next
        return None

    def print_all(self):
        cur = self.head
        while cur:
            print(f"data: {cur.data}\n  prevHash: {cur.prev_hash}\n  hash:     {cur.hash}")
            cur = cur.next

    def deleteNode(self, node: Node):
        # In an append-only list, we do not allow deletion of nodes.
        print("Deletion is not allowed in AppendOnlyList.")

    def modifyNode(self, node: Node, val: str):
        # In an append-only list, we do not allow modification of nodes.
        print("Modification is not allowed in AppendOnlyList.")


# --- demo ---
lst = AppendOnlyList()
lst.append("1")
second = lst.append("2")
lst.append("3")

print("=== Full chain ===")
lst.print_all()

print("\n=== Neighbors of 'second entry' ===")
found = lst.find_by_hash(second.hash)
if found:
    print("prev:", found.prev.data if found.prev else None)
    print("next:", found.next.data if found.next else None)

lst.deleteNode(second)  # This will raise NotImplementedError
lst.modifyNode(second, "1")  # This will raise NotImplementedError