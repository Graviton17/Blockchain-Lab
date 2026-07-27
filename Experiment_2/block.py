import hashlib
import random
import time

def calc_hash(index, nonce, data, previous_hash):
    text = str(index) + str(nonce) + data + previous_hash
    return hashlib.sha256(text.encode()).hexdigest()

def mine(index, data, previous_hash, difficulty):
    target = "0" * difficulty
    while True:
        nonce = random.randint(0, 999999999)
        block_hash = calc_hash(index, nonce, data, previous_hash)
        if block_hash.startswith(target):
            return nonce, block_hash

def main():
    index = 1
    previous_hash = "0"
    difficulty = 4

    data = input("Enter data: ")

    for d in range(1, difficulty + 1):
        start = time.time()
        nonce, block_hash = mine(index, data, previous_hash, d)
        elapsed = time.time() - start

        print(f"\nDifficulty   : {d}")
        print("Block #      :", index)
        print("Nonce        :", nonce)
        print("Data         :", data)
        print("Previous Hash:", previous_hash)
        print("Hash         :", block_hash)
        print(f"Time to mine : {elapsed:.4f} sec")

if __name__ == "__main__":
    main()