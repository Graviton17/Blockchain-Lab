import hashlib
from typing import List, Tuple


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def hash_leaf(tx: str) -> bytes:
    return sha256(tx.encode("utf-8"))


def hash_pair(left: bytes, right: bytes) -> bytes:
    return sha256(left + right)


class MerkleTree:
    def __init__(self, transactions: List[str]):
        if not transactions:
            raise ValueError("Need at least 1 transaction")
        self.transactions = transactions
        self.leaves = [hash_leaf(tx) for tx in transactions]
        self.levels: List[List[bytes]] = []
        self._build()

    def _build(self) -> None:
        level = self.leaves[:]
        self.levels.append(level)
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else level[i]
                next_level.append(hash_pair(left, right))
            self.levels.append(next_level)
            level = next_level
        self.root = level[0]

    def get_root(self) -> str:
        return self.root.hex()

    def get_proof(self, index: int) -> List[Tuple[str, str]]:
        if not 0 <= index < len(self.leaves):
            raise IndexError("transaction index out of range")

        proof = []
        idx = index
        for level in self.levels[:-1]:
            is_right_child = idx % 2 == 1
            if is_right_child:
                sibling_idx = idx - 1
                side = "L"
            else:
                sibling_idx = idx + 1 if idx + 1 < len(level) else idx
                side = "R"
            proof.append((level[sibling_idx].hex(), side))
            idx //= 2
        return proof

    def print_tree(self) -> None:
        for depth, level in enumerate(self.levels):
            label = "leaves" if depth == 0 else f"level {depth}"
            print(f"  {label:9s}: " + "  ".join(h.hex()[:8] for h in level))


def verify_proof(tx: str, index: int, proof: List[Tuple[str, str]], root_hex: str) -> bool:
    current = hash_leaf(tx)
    for sibling_hex, side in proof:
        sibling = bytes.fromhex(sibling_hex)
        current = hash_pair(sibling, current) if side == "L" else hash_pair(current, sibling)
    return current.hex() == root_hex


def run(n: int, target_tx_num: int) -> None:
    transactions = [f"tx{i + 1}" for i in range(n)]
    tree = MerkleTree(transactions)

    print(f"n = {n}  ->  transactions = {transactions}")
    print(f"Merkle Root: {tree.get_root()}")
    tree.print_tree()

    target_index = min(target_tx_num - 1, n - 1)
    target_tx = transactions[target_index]
    proof = tree.get_proof(target_index)

    print(f"\nAuthentication path for '{target_tx}' (index {target_index}):")
    for step, (h, side) in enumerate(proof, 1):
        print(f"  step {step}: sibling={h[:16]}...  sibling_is_{('left' if side=='L' else 'right')}")

    ok = verify_proof(target_tx, target_index, proof, tree.get_root())
    print(f"Verify('{target_tx}', proof, root) -> {ok}  (proof of presence {'CONFIRMED' if ok else 'FAILED'})")

    forged_ok = verify_proof("tx_forged", target_index, proof, tree.get_root())
    print(f"Verify('tx_forged', proof, root) -> {forged_ok}  (should be False)")


if __name__ == "__main__":
    n = int(input("Enter number of transactions (n): "))
    target_tx_num = int(input("Enter transaction number to prove (default 1 if >= n): ") or "1")
    
    if n < 1:
        print("n must be at least 1")
    else:
        run(n, target_tx_num)