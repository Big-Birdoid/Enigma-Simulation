import machine as eg

def main():
    
    # Get user input
    plaintext = input("Enter a message: ")
    print("encrypting...")

    # TODO Encode the message
    ciphertext = eg.encrypt(plaintext)

    # Print the encoded message
    print(f"Encrypted: {ciphertext}")


if __name__ == "__main__":
    main()