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


# --- demo ---
lst = AppendOnlyList()
lst.append("first entry")
second = lst.append("second entry")
lst.append("third entry")

print("=== Full chain ===")
lst.print_all()

print("\n=== Neighbors of 'second entry' ===")
found = lst.find_by_hash(second.hash)
if found:
    print("prev:", found.prev.data if found.prev else None)
    print("next:", found.next.data if found.next else None)