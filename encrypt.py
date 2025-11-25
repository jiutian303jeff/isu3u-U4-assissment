"""
author : 
date :
description : this module contains Encrypt class to encrypt and decrypt data, using rotor-based encryption similar to Enigma machine.
"""

import random

class Encrypt:
    def __init__(self, rotor1_offset=0, rotor2_offset=0):
        self.alphabet = [chr(i) for i in range(65, 91)] + [",", ".", "!", "/", "?", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]
        self.n = len(self.alphabet)

        self.rotor1 = self.alphabet.copy()
        self.rotor2 = self.alphabet.copy()
        random.shuffle(self.rotor1) 
        random.shuffle(self.rotor2)

        self.reflector = self.alphabet.copy() 
        random.shuffle(self.reflector)

        self.plugboard = {'A':'#', '#':'A', 'B':'$','$':'B', 'C':'&','&':'C'}

        self.rotor1_offset = rotor1_offset
        self.rotor2_offset = rotor2_offset

    def encrypt_char(self, char):
        if char not in self.alphabet:
            return char

        # pass through plugboard
        char = self.plugboard.get(char, char)

        # encrypt through rotors
        idx = (self.alphabet.index(char) + self.rotor1_offset) % self.n 
        char = self.rotor1[idx]

        idx = (self.alphabet.index(char) + self.rotor2_offset) % self.n 
        char = self.rotor2[idx]

        # pass through reflector
        idx = self.alphabet.index(char)
        char = self.reflector[idx]

        # decrypt through rotors
        idx = self.rotor2.index(char)
        char = self.alphabet[(idx - self.rotor2_offset) % self.n]

        idx = self.rotor1.index(char)
        char = self.alphabet[(idx - self.rotor1_offset) % self.n]

        # pass through plugboard again
        char = self.plugboard.get(char, char)

        # rotate rotors
        self.rotor1_offset = (self.rotor1_offset + 1) % self.n
        if self.rotor1_offset == 0:
            self.rotor2_offset = (self.rotor2_offset + 1) % self.n

        return char

    def encrypt(self, text):
        return ''.join(self.encrypt_char(c) for c in text)

    def save_to_file(self, text, filename="encrypted_data.bin"):
        encrypted = self.encrypt(text)
        with open(filename, "wb") as f:
            f.write(encrypted.encode("utf-8"))

    def load_from_file(self, filename="encrypted_data.bin"):
        try:
            with open(filename, "rb") as f:
                encrypted = f.read().decode("utf-8")
        except FileNotFoundError:
            return ""

        # reset offsets for proper decryption
        self.rotor1_offset = 0
        self.rotor2_offset = 0

        decrypted = self.encrypt(encrypted)
        return decrypted
