
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# parent class for the basic substitution cipher that both the rotors and reflector board are based on
class Substitution:
    def __init__(self, key: str) -> None:
        self.key = key # key used for the substitution cipher

    def substitute(self, letter: str) -> str:
        return self.key[alphabet.index(letter)]


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

    def rotorEncrypt(self, letter: str) -> str:
        for rotor in self.rotors:
            letter = rotor.substitute(letter)
        return letter

class Machine:
    def __init__(self, r1: Rotor, r2: Rotor, r3: Rotor, ref: Reflector, plugs: Plugboard) -> None:
        self.assembly = Assembly(r1, r2, r3)
        self.reflector = ref
        self.plugboard = plugs

    def encrypt(self, plaintext: str) -> str:
        pass


# Testing
if __name__ == "__main__":
    # Initialising the rotors
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "J")
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "O")

    for i in range(26):
        print(rotor1.key[0])
        print(rotor1.rotateNext)
        rotor1.rotate()

    message = "HELLOWORLD"
    ciphertext = ""

    for letter in message:
        ciphertext += rotor1.substitute(letter)
    
    print(ciphertext)
