"""
Docstring for encrypt
"""


class Encrypt:
    def __init__(self, rotrol1_offset, rotrol2_offset):
        self.alphabet = [chr(i) for i in range(65, 91)] + [",", ".", "!", "/", "?",  "#", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]

        self.rotrol1_offset = rotrol1_offset
        self.rotrol2_offset = rotrol2_offset

    def encrypt_data(self):
        pass

    def decrypt_data(self):
        pass