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
        self.accounts = {}

    def generate_rotors(self, rotor1_offset=0, rotor2_offset=0):
        self.rotor1 = self.alphabet.copy()
        self.rotor2 = self.alphabet.copy()
        self.reflector = self.alphabet.copy() 
        random.shuffle(self.rotor1) 
        random.shuffle(self.rotor2)
        random.shuffle(self.reflector)

        self.plugboard = {'A':'#', '#':'A', 'B':'$','$':'B', 'C':'&','&':'C'}

        return {
            "rotor1": self.rotor1,
            "rotor2": self.rotor2,
            "reflector": self.reflector,
            "plugboard": self.plugboard,
            "rotor1_offset": 0,
            "rotor2_offset": 0
        }
    
    def add_account(self, account_name, initial_data):
        key = self.generate_rotors(self)
        self.accounts[account_name] = {"key": key, "data": initial_data}
        self.accounts[account_name]["encrypted"] = self.encrypt_text(initial_data, key)


    def encrypt_char(self, char, key):
        if char not in self.alphabet:
            return char

        char = key["plugboard"].get(char, char)
        idx = (self.alphabet.index(char) + key["rotor1_offset"]) % self.n
        char = key["rotor1"][idx]
        idx = (self.alphabet.index(char) + key["rotor2_offset"]) % self.n
        char = key["rotor2"][idx]
        idx = self.alphabet.index(char)
        char = key["reflector"][idx]
        idx = key["rotor2"].index(char)
        char = self.alphabet[(idx - key["rotor2_offset"]) % self.n]
        idx = key["rotor1"].index(char)
        char = self.alphabet[(idx - key["rotor1_offset"]) % self.n]
        char = key["plugboard"].get(char, char)

        # rotate rotors
        key["rotor1_offset"] = (key["rotor1_offset"] + 1) % self.n
        if key["rotor1_offset"] == 0:
            key["rotor2_offset"] = (key["rotor2_offset"] + 1) % self.n
        return char

    def encrypt(self, text):
        return ''.join(self.encrypt_char(c) for c in text)
    
    def save_account_to_file(self, account_name, new_data, filename="encrypted_data.bin"):
        key = self.accounts[account_name]["key"]
        key["rotor1_offset"] = 0
        key["rotor2_offset"] = 0
        self.accounts[account_name]["data"] = new_data
        self.accounts[account_name]["encrypted"] = self.encrypt_text(new_data, key)
        self.save_accounts_to_file(filename)
        print(f"Account {account_name} updated and saved.")

    def save_to_file(self, text, filename="encrypted_data.bin"):
        with open(filename, "wb") as f:
            for name, info in self.accounts.items():
                line = f"{name}:{info['encrypted']}\n"
                f.write(line.encode("utf-8"))

    def load_from_file(self, filename="encrypted_data.bin"):
        try:
            with open(filename, "rb") as f:
                lines = f.read().decode("utf-8").splitlines()
        except FileNotFoundError:
            return ""

        for line in lines:
            if ':' not in line:
                continue
            name, encrypted = line.split(":", 1)
            if name in self.accounts:
                key = self.accounts[name]["key"]
                key["rotor1_offset"] = 0
                key["rotor2_offset"] = 0
                decrypted = self.encrypt_text(encrypted, key)
                self.accounts[name]["data"] = decrypted
                self.accounts[name]["encrypted"] = encrypted