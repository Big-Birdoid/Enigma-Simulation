
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# parent class for the basic substitution cipher that both the rotors and reflector board are based on
class Substitution:
    def __init__(self, key: str) -> None:
        self.key = key # key used for the substitution cipher
        self.reversedKey = self.reverseKey(key) # the inverse mapping of the key

    def substitute(self, letter: str, k: str) -> str: # k is the key to use for the substitution (either standard or reversed)
        return k[alphabet.index(letter)]
    
    # returns the inverse mapping of the key (think inverse functions from maths)
    def reverseKey(self, key: str) -> str:
        rev = [''] * 26    # Create a list of 26 empty strings
        for i, char in enumerate(key):
            rev[ord(char) - ord('A')] = chr(i + ord('A'))  # Map each character to its corresponding position
        return ''.join(rev)  # Join the list into a string and return it


# The rotor on its own performa a rather simple substitution cipher
class Rotor(Substitution):
    def __init__(self, key: str, notch: str) -> None:
        super().__init__(key)
        self.key = key # key used for the rotor's substitution cipher
        self.notch = notch # the position at which the rotor will rotate the next rotor
        self.rotateNext = False # whether the next rotor should rotate

    # simmulates the circular rotation of the rotor thing
    def rotate(self) -> None:
        self.key = self.key[1:] + self.key[0]
        if self.key[25] == self.notch: # if this rotation has moved from the notch letter
            self.rotateNext = True # signal for the next rotor to rotate
        else:
            self.rotateNext = False


# The plugboard is also a simple substitution cipher
# TODO make this only have 10 options for letter swapping rather than 26
class Plugboard(Substitution):
    def __init__(self, key: str) -> None:
        super().__init__(key)


class Reflector(Substitution):
    def __init__(self, key: str) -> None:
        super().__init__(key)


# class for the whole rotor assembly
class Assembly:
    def __init__(self, r1: Rotor, r2: Rotor, r3: Rotor) -> None:
        # the rotors in the assembly from rightmost to leftmost
        self.rotors = [r1, r2, r3]
    
    def advanceRotors(self) -> None:
        for i in range(0, 1):
            if self.rotors[i].rotateNext:
                self.rotors[i + 1].rotate()
            self.rotors[i].rotate()

    def rotorEncrypt(self, letter: str) -> str:
        for rotor in self.rotors:
            letter = rotor.substitute(letter, rotor.key)
        return letter
    
    def rotorReverseEncrypt(self, letter: str) -> str: # sending the signal back through the rotors but in the reversed wiring path
        for rotor in reversed(self.rotors):
            letter = rotor.substitute(letter, rotor.reversedKey)
        return letter


class Machine:
    def __init__(self, r1: Rotor, r2: Rotor, r3: Rotor, ref: Reflector, plugs: Plugboard) -> None:
        self.assembly = Assembly(r1, r2, r3)
        self.reflector = ref
        self.plugboard = plugs

    def encrypt(self, plaintext: str) -> str:
        ciphertext = ""  # Initialize the ciphertext variable
        for char in plaintext:
            encryptedChar = self.plugboard.substitute(char, self.plugboard.key) # character goes through the plugboard initially
            encryptedChar = self.assembly.rotorEncrypt(encryptedChar) # then through rotors
            encryptedChar = self.reflector.substitute(encryptedChar, self.reflector.key) # then through the reflector (this is the flaw in the machine - the reflector cannot assign a letter to itself)
            encryptedChar = self.assembly.rotorReverseEncrypt(encryptedChar) # then back through the rotors in the reversed wiring path
            encryptedChar = self.plugboard.substitute(encryptedChar, self.plugboard.key) # then back through the plugboard
            ciphertext += encryptedChar
            self.assembly.advanceRotors()
        return ciphertext
            


# Testing
if __name__ == "__main__":
    # Initialising the rotors
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "J")
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "O")

    # Initialising the reflector
    reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Initialise the plugboard
    plugboard = Plugboard(alphabet) # no swapping of letters for now

    # Initialising the machine
    enigma = Machine(rotor1, rotor2, rotor3, reflector, plugboard)

    # Get user input
    plaintext = input("Enter a message: ")
    
    # Encode the message
    ciphertext = enigma.encrypt(plaintext)

    # Print the encoded message
    print(f"{ciphertext}")
