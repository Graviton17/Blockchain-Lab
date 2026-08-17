import hashlib
import random


class Curve:
    def __init__(self, p, a, b, gx, gy, n):
        self.p = p
        self.a = a
        self.b = b
        self.gx = gx
        self.gy = gy
        self.n = n

secp256k1 = Curve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
    gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)

def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(p1, p2, curve):
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 != y2:
        return None

    if p1 == p2:
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p) % curve.p
    else:
        m = (y2 - y1) * inverse_mod(x2 - x1, curve.p) % curve.p

    x3 = (m * m - x1 - x2) % curve.p
    y3 = (m * (x1 - x3) - y1) % curve.p
    return (x3, y3)

def point_mul(k, point, curve):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend, curve)
        addend = point_add(addend, addend, curve)
        k >>= 1
    return result

def generate_keypair(curve):
    priv = random.randrange(1, curve.n - 1)
    pub = point_mul(priv, (curve.gx, curve.gy), curve)
    return priv, pub

def hash_message(message):
    digest = hashlib.sha256(message.encode()).digest()
    return int.from_bytes(digest, byteorder="big")

def sign(message, priv, curve):
    z = hash_message(message)
    r = 0
    s = 0
    while r == 0 or s == 0:
        k = random.randrange(1, curve.n - 1)
        point = point_mul(k, (curve.gx, curve.gy), curve)
        if point is None:
            continue
        x, y = point
        r = x % curve.n
        if r == 0:
            continue
        k_inv = inverse_mod(k, curve.n)
        s = (k_inv * (z + r * priv)) % curve.n
    return (r, s)

def verify(message, signature, pub, curve):
    r, s = signature
    if not (1 <= r <= curve.n - 1 and 1 <= s <= curve.n - 1):
        return False

    z = hash_message(message)
    w = inverse_mod(s, curve.n)
    u1 = (z * w) % curve.n
    u2 = (r * w) % curve.n

    point1 = point_mul(u1, (curve.gx, curve.gy), curve)
    point2 = point_mul(u2, pub, curve)
    point = point_add(point1, point2, curve)

    if point is None:
        return False

    x, y = point
    return r == x % curve.n

class Transaction:
    def __init__(self, sender, receiver, amount, sender_pub=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.sender_pub = sender_pub
        self.signature = None

    def to_string(self):
        return f"{self.sender}->{self.receiver}:{self.amount}"

    def sign_transaction(self, priv, curve=secp256k1):
        self.signature = sign(self.to_string(), priv, curve)

    def is_valid(self, pub, curve=secp256k1):
        if self.signature is None:
            return False
        return verify(self.to_string(), self.signature, pub, curve)

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        payload = self.previous_hash + "".join(tx.to_string() for tx in self.transactions)
        return hashlib.sha256(payload.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        genesis = Block([], "0" * 64)
        self.chain = [genesis]

    def add_block(self, transactions):
        for tx in transactions:
            if not tx.is_valid(tx.sender_pub):
                raise ValueError(f"invalid signature for transaction {tx.to_string()}")
        block = Block(transactions, self.chain[-1].hash)
        self.chain.append(block)
        return block

if __name__ == "__main__":
    alice_priv, alice_pub = generate_keypair(secp256k1)
    bob_priv, bob_pub = generate_keypair(secp256k1)

    tx = Transaction("Alice", "Bob", 50, sender_pub=alice_pub)
    tx.sign_transaction(alice_priv)

    print("signature:", tx.signature)
    print("valid with correct key:", tx.is_valid(alice_pub))
    print("valid with wrong key:", tx.is_valid(bob_pub))

    chain = Blockchain()
    block = chain.add_block([tx])
    print("block hash:", block.hash)
    print("previous hash:", block.previous_hash)