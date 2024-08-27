# do imports here

def main():
    
    # Get user input
    plaintext = input("Enter a message: ")
    length = len(plaintext)

    # TODO Encode the message
    ciphertext = encode(plaintext)

    # Print the encoded message
    print(f"{ciphertext}")


if __name__ == "__main__":
    main()