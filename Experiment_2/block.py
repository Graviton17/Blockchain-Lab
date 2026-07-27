import hashlib

def calc_hash(index, nonce, data, previous_hash):
    text = str(index) + str(nonce) + data + previous_hash
    return hashlib.sha256(text.encode()).hexdigest()

def main():
    index = 1
    previous_hash = "0"

    data = input("Enter data: ")
    nonce = int(input("Enter nonce: "))

    block_hash = calc_hash(index, nonce, data, previous_hash)

    print("\nBlock #      :", index)
    print("Nonce        :", nonce)
    print("Data         :", data)
    print("Previous Hash:", previous_hash)
    print("Hash         :", block_hash)

if __name__ == "__main__":
    main()