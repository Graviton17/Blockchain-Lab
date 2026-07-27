import hashlib

def main():
    input_text = input("Enter text: ")
    hash_object = hashlib.sha256(input_text.encode())
    hex_string = hash_object.hexdigest()
    print("SHA-256 Hash: " + hex_string)

if __name__ == "__main__":
    main()