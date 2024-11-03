
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# parent class for the basic substitution cipher that the rotors, plugboard and reflector are based on
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


# The rotor on its own performs a rather simple substitution cipher
class Rotor(Substitution):
    def __init__(self, key: str, notch: str, starting_position: str = 'A') -> None:
        super().__init__(key)
        self.key = key # key used for the rotor's substitution cipher
        self.notch = notch # the position at which the rotor will rotate the next rotor
        # rotate to starting position
        while self.key[0] != starting_position:
            self.rotate()
        self.initialPosition = self.key # store initial position for reset

    # simulates the circular rotation of the rotor thing
    def rotate(self) -> None:
        self.key = self.key[1:] + self.key[0]
    
    # checks if this rotor should cause the next one to rotate
    def should_rotate_next(self) -> bool:
        return self.key[0] == self.notch
    
    def reset(self) -> None: # reset the rotor to its initial position
        self.key = self.initialPosition


# The plugboard is also a simple substitution cipher but works in pairs
class Plugboard(Substitution):
    def __init__(self, pairs: str = '') -> None:
        # start with normal alphabet mapping
        key = list(alphabet)
        # swap the pairs of letters
        for i in range(0, len(pairs), 2):
            if i + 1 < len(pairs):
                a, b = pairs[i], pairs[i + 1]
                idx_a = alphabet.index(a)
                idx_b = alphabet.index(b)
                key[idx_a] = b
                key[idx_b] = a
        super().__init__(''.join(key))



# The reflector ensures the encryption is reciprocal (if A->B then B->A)
class Reflector(Substitution):
    def __init__(self, key: str = "YRUHQSLDPXNGOKMIEBFZCWVJAT") -> None: # using historical Reflector B wiring
        super().__init__(key)


# class for the whole rotor assembly
# class for the whole rotor assembly
class Assembly:
    def __init__(self, r1: Rotor, r2: Rotor, r3: Rotor) -> None:
        # the rotors in the assembly from rightmost to leftmost
        self.rotors = [r1, r2, r3]
    
    def advanceRotors(self) -> None:
        # implement double-stepping mechanism
        # if middle rotor is at notch, rotate middle and left rotors
        if self.rotors[1].should_rotate_next():
            self.rotors[1].rotate()
            self.rotors[2].rotate()
        # if right rotor is at notch, rotate middle rotor
        elif self.rotors[0].should_rotate_next():
            self.rotors[1].rotate()
        # always rotate right rotor
        self.rotors[0].rotate()

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
    
    def reset_rotors(self) -> None:
        for rotor in self.assembly.rotors:
            rotor.reset()


# Test the machine
if __name__ == "__main__":
    # All substutions are identity mappings
    rotor1 = Rotor("YFBKTAXUQVMOZIJSPNLHRGCEWD", "Z")
    rotor2 = Rotor("XQZIUHNBKJCVMFRLWDYGOESATP", "Z")
    rotor3 = Rotor("ZTVIRKHQDXPNOLGYFMUACBWSJE", "Z")
    reflector = Reflector(alphabet)
    plugboard = Plugboard(alphabet)

    machine = Machine(rotor1, rotor2, rotor3, reflector, plugboard)
    plaintext = "HELLO"
    print("Plaintext:", plaintext)
    ciphertext = machine.encrypt(plaintext)
    print("Ciphertext:", ciphertext)

    # Reset rotors before decryption
    machine.reset_rotors()
    decrypted_text = machine.encrypt(ciphertext)
    print("Decrypted text:", decrypted_text)
