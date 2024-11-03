alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Parent class for the basic substitution cipher that the rotors, plugboard, and reflector are based on
class Substitution:
    def __init__(self, key: str) -> None:
        self.key = key  # Key used for the substitution cipher
        self.reversedKey = self.reverseKey(key)  # The inverse mapping of the key

    def substitute(self, letter: str, k: str) -> str:
        """Uses the specified key (standard or reversed) to substitute the letter."""
        return k[alphabet.index(letter)]

    def reverseKey(self, key: str) -> str:
        """Returns the inverse mapping of the key (for backward signal flow)."""
        rev = [''] * 26
        for i, char in enumerate(key):
            rev[ord(char) - ord('A')] = chr(i + ord('A'))
        return ''.join(rev)


# The Rotor performs a simple substitution cipher with rotation capability
class Rotor(Substitution):
    def __init__(self, key: str, notch: str, starting_position: str = 'A') -> None:
        super().__init__(key)
        self.notch = notch  # The rotor's notch position, which triggers the next rotor
        # Position offset determines where the rotor starts in the alphabet (like turning it to a specific letter)
        self.position = alphabet.index(starting_position)  

    def rotate(self) -> None:
        """Simulates the rotor's circular rotation by incrementing the position offset."""
        self.position = (self.position + 1) % 26

    def should_rotate_next(self) -> bool:
        """Checks if this rotor should cause the next rotor to rotate (when at notch)."""
        return alphabet[self.position] == self.notch

    def forward_substitute(self, letter: str) -> str:
        """Substitutes letter going forward through the rotor with current position offset."""
        # Adjust for current rotor position
        index = (alphabet.index(letter) + self.position) % 26
        # Substitute using the key, then adjust back by position
        substituted = self.key[index]
        return alphabet[(alphabet.index(substituted) - self.position) % 26]

    def backward_substitute(self, letter: str) -> str:
        """Substitutes letter going backward through the rotor with current position offset."""
        # Adjust for current rotor position
        index = (alphabet.index(letter) + self.position) % 26
        # Substitute using the reversed key, then adjust back by position
        substituted = self.reversedKey[index]
        return alphabet[(alphabet.index(substituted) - self.position) % 26]


# The Plugboard performs a simple substitution cipher with letter pairs
class Plugboard(Substitution):
    def __init__(self, pairs: str = '') -> None:
        # Start with standard alphabet mapping
        key = list(alphabet)
        # Swap specified pairs in the key
        for i in range(0, len(pairs), 2):
            if i + 1 < len(pairs):
                a, b = pairs[i], pairs[i + 1]
                idx_a = alphabet.index(a)
                idx_b = alphabet.index(b)
                key[idx_a], key[idx_b] = b, a  # Swap the letter pair in the key
        super().__init__(''.join(key))


# The Reflector ensures reciprocal encryption (A↔B)
class Reflector(Substitution):
    def __init__(self, key: str = "YRUHQSLDPXNGOKMIEBFZCWVJAT") -> None: # Historical reflector B key
        super().__init__(key)


# The Assembly contains all rotors and manages their stepping
class Assembly:
    def __init__(self, r1: Rotor, r2: Rotor, r3: Rotor) -> None:
        # The rotors are arranged from rightmost to leftmost
        self.rotors = [r1, r2, r3]

    def advance_rotors(self) -> None:
        """Implements the double-stepping mechanism for rotor rotation."""
        # If the middle rotor is at its notch, rotate both the middle and left rotors
        if self.rotors[1].should_rotate_next():
            self.rotors[1].rotate()
            self.rotors[2].rotate()
        # If the right rotor is at its notch, rotate the middle rotor
        elif self.rotors[0].should_rotate_next():
            self.rotors[1].rotate()
        # Always rotate the rightmost rotor
        self.rotors[0].rotate()

    def rotor_encrypt(self, letter: str) -> str:
        """Passes a letter forward through the rotor assembly."""
        # The signal passes from right to left through each rotor
        for rotor in self.rotors:
            letter = rotor.forward_substitute(letter)
        return letter

    def rotor_reverse_encrypt(self, letter: str) -> str:
        """Passes a letter backward through the rotor assembly."""
        # The signal returns from left to right through each rotor
        for rotor in reversed(self.rotors):
            letter = rotor.backward_substitute(letter)
        return letter


# The Machine combines plugboard, rotor assembly, and reflector for full encryption
class Machine:
    def __init__(self, r1: Rotor, r2: Rotor, r3: Rotor, ref: Reflector, plugs: Plugboard) -> None:
        self.assembly = Assembly(r1, r2, r3)
        self.reflector = ref
        self.plugboard = plugs

    def encrypt(self, plaintext: str) -> str:
        """Encrypts or decrypts the plaintext by passing each letter through the Enigma components."""
        ciphertext = ""
        for char in plaintext:
            if char == ' ':  # Skip spaces in the plaintext
                ciphertext += ' '
                continue
            char = char.upper()
            if char not in alphabet:  # Skip non-alphabet characters
                ciphertext += char
                continue

            # Advance rotors before each letter encryption
            self.assembly.advance_rotors()

            # 1. Plugboard substitution
            char = self.plugboard.substitute(char, self.plugboard.key)
            # 2. Forward through the rotors
            char = self.assembly.rotor_encrypt(char)
            # 3. Reflector substitution
            char = self.reflector.substitute(char, self.reflector.key)
            # 4. Backward through the rotors
            char = self.assembly.rotor_reverse_encrypt(char)
            # 5. Final plugboard substitution
            char = self.plugboard.substitute(char, self.plugboard.key)

            ciphertext += char  # Append encrypted character to ciphertext
        return ciphertext

    def reset_rotors(self) -> None:
        """Resets each rotor to its starting position."""
        for rotor in self.assembly.rotors:
            rotor.position = 0  # Reset position to initial


# Test the machine
if __name__ == "__main__":
    # Define historical rotor settings and configurations
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", starting_position='A')  # Rotor I
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", starting_position='A')  # Rotor II
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", starting_position='A')  # Rotor III
    reflector = Reflector()  # Reflector B configuration
    plugboard = Plugboard("AMFINVPSTUWZ")  # Example plugboard pairs: A↔M, F↔I, etc.

    # Initialize the Enigma machine with rotors, reflector, and plugboard
    machine = Machine(rotor1, rotor2, rotor3, reflector, plugboard)
    
    # Encrypt the plaintext message
    plaintext = "HELLO WORLD"
    print("Plaintext:", plaintext)
    ciphertext = machine.encrypt(plaintext)
    print("Ciphertext:", ciphertext)

    # Reset rotors to initial state to decrypt
    machine.reset_rotors()
    decrypted_text = machine.encrypt(ciphertext)  # Decrypt by re-encrypting the ciphertext
    print("Decrypted text:", decrypted_text)
