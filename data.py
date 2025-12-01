class Data:
    def __init__(self, username="", password="", balance=0, transaction_history=None,
                 encrypt_manager=None, filename_template="encrypted_{username}.txt"):

        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = transaction_history or []
        self.filename_template = filename_template
        self.manager = encrypt_manager

    def get_encrypted_filename(self):
        return self.filename_template.format(username=self.username)

    def save_data(self):
        encrypted_data = self.manager.encrypt(f"{self.username},{self.password},{self.balance},{';'.join(self.transaction_history)}")
        with open(self.get_encrypted_filename(), 'w') as file:
            file.write(encrypted_data)
        return True

    def pull_data(self, username):
        try:
            with open(self.get_encrypted_filename(), 'r') as file:
                encrypted_data = file.read()
                decrypted_data = self.manager.decrypt(encrypted_data)
                data_parts = decrypted_data.split(',')
                self.username = data_parts[0]
                self.password = data_parts[1]
                self.balance = float(data_parts[2])
                self.transaction_history = data_parts[3].split(';') if len(data_parts) > 3 else []
                return True
        except FileNotFoundError:
            return False

    def deposit(self, amount, note=""):
        if amount <= 0:
            return False
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount} - {note}")
        self.save_data()
        return True

    def withdraw(self, amount, note=""):
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append(f"Withdrew {amount} - {note}")
        self.save_data()
        return True

    def transfer(self, target_username, amount, note=""):
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append(f"Transferred {amount} to {target_username} - {note}")
        self.save_data()
        return True