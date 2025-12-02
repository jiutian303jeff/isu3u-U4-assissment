"""
author : Leo L.
date   : oct 30
desc   : Data model for simple account storage. The Data class wraps:
         - username, password, balance, transaction_history
         - file storage using an Encrypt manager (provided via dependency)
         Methods handle loading, saving and basic account operations.
"""
class Data:
    def __init__(self, username="", password="", balance=0, transaction_history=None,
                 encrypt_manager=None, filename_template="encrypted_{username}.txt"):
        """
        Initialize Data object.
        - username/password: credentials (strings)
        - balance: float representing account balance
        - transaction_history: list of strings (notes)
        - encrypt_manager: object providing encrypt/decrypt methods
        - filename_template: template for per-user file storage
        """
        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = transaction_history or []
        self.filename_template = filename_template
        self.manager = encrypt_manager

    def get_encrypted_filename(self):
        """Return the filename used to persist this account (formatted template)."""
        return self.filename_template.format(username=self.username)

    def save_data(self):
        """
        Serialize and encrypt account data, then write to file.
        Format stored (plain before encrypt): username,password,balance,tx1;tx2;...
        Returns True on success.
        """
        encrypted_data = self.manager.encrypt(f"{self.username},{self.password},{self.balance},{';'.join(self.transaction_history)}")
        with open(self.get_encrypted_filename(), 'w') as file:
            file.write(encrypted_data)
        return True

    def pull_data(self, username):
        """
        Load and decrypt account data from disk. Populate this instance's fields.
        Returns True if file found and parsed, False if file missing.
        """
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
        """
        Deposit amount into account. Amount must be > 0.
        Append transaction note and persist data. Returns True on success.
        """
        if amount <= 0:
            return False
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount} - {note}")
        self.save_data()
        return True

    def withdraw(self, amount, note=""):
        """
        Withdraw amount from account. Must be > 0 and <= balance.
        Append transaction note and persist data. Returns True on success.
        """
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append(f"Withdrew {amount} - {note}")
        self.save_data()
        return True

    def transfer(self, target_username, amount, note=""):
        """
        Deduct amount for a transfer to another account. This method only
        performs withdrawal side and saves. Caller should deposit to target.
        Returns True on success.
        """
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append(f"Transferred {amount} to {target_username} - {note}")
        self.save_data()
        return True