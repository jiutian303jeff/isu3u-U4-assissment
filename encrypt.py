class EncryptManager:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        encrypted_data = ''.join(chr(ord(char) + self.key) for char in data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        decrypted_data = ''.join(chr(ord(char) - self.key) for char in encrypted_data)
        return decrypted_data

    def save_encrypted_data(self, filename, data):
        encrypted_data = self.encrypt(data)
        with open(filename, 'w') as file:
            file.write(encrypted_data)

    def load_encrypted_data(self, filename):
        with open(filename, 'r') as file:
            encrypted_data = file.read()
        return self.decrypt(encrypted_data)