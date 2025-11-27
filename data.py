"""
Docstring for data
"""

class Data:
    def __init__(self, username="", password="", balance=0, transaction_history=None, encrypt_manager=None, filename="encrypted_data.txt"):
        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = transaction_history or []
        self.filename = filename
        if encrypt_manager is not None:
            self.manager = encrypt_manager
        else:
            try:
                from encrypt import Encrypt
                self.manager = Encrypt()
            except Exception:
                self.manager = None

    def pull_data(self, username=None):
        if username:
            self.username = username
        if not self.manager:
            return False
        try:
            self.manager.load_from_file(self.filename)
        except Exception:
            pass
        acct = self.manager.accounts.get(self.username)
        if not acct:
            return False
        data = acct.get("data")
        if not data:
            return False
        self._parse_plaintext(data)
        return True

    def save_data(self):
        if not self.manager:
            return False
        if self.username == "":
            return False
        plain = self._compose_plaintext()
        if "add_account" in dir(self.manager):
            if self.username not in self.manager.accounts:
                try:
                    self.manager.add_account(self.username, plain)
                except Exception:
                    keygen = getattr(self.manager, "generate_key", None) or getattr(self.manager, "generate_rotors", None)
                    if keygen:
                        k = keygen()
                        self.manager.accounts[self.username] = {"key": k, "data": plain, "encrypted": self.manager.encrypt_text(plain, k)}
            else:
                try:
                    update = getattr(self.manager, "update_account", None)
                    if update:
                        update(self.username, plain, filename=self.filename)
                    else:
                        key = self.manager.accounts[self.username]["key"]
                        key["rotor1_offset"] = 0
                        key["rotor2_offset"] = 0
                        self.manager.accounts[self.username]["data"] = plain
                        self.manager.accounts[self.username]["encrypted"] = self.manager.encrypt_text(plain, key)
                except Exception:
                    return False
        else:
            keygen = getattr(self.manager, "generate_key", None) or getattr(self.manager, "generate_rotors", None)
            if keygen:
                k = keygen()
                self.manager.accounts[self.username] = {"key": k, "data": plain, "encrypted": self.manager.encrypt_text(plain, k)}
            else:
                return False
        saver = getattr(self.manager, "save_to_file", None) or getattr(self.manager, "save_accounts_to_file", None)
        if saver:
            try:
                saver(self.filename)
            except TypeError:
                saver()
        return True

    def balance_amount(self):
        return self.balance

    def trans_history(self):
        return list(self.transaction_history)

    def error_handle(self):
        if not isinstance(self.username, str) or self.username == "":
            return "invalid username"
        if not isinstance(self.password, str) or self.password == "":
            return "invalid password"
        if not isinstance(self.balance, (int, float)):
            return "invalid balance"
        return None

    def _parse_plaintext(self, text):
        self.transaction_history = []
        self.balance = 0
        self.password = ""
        parts = [p.strip() for p in text.split(";") if p.strip()]
        for p in parts:
            if p.lower().startswith("balance:"):
                val = p.split(":",1)[1].strip()
                digits = "".join(ch for ch in val if (ch.isdigit() or ch == "." or ch == "-"))
                try:
                    if "." in digits:
                        self.balance = float(digits)
                    else:
                        self.balance = int(digits) if digits != "" else 0
                except:
                    self.balance = 0
            elif p.lower().startswith("password:"):
                self.password = p.split(":",1)[1].strip()
            else:
                self.transaction_history.append(p)

    def _compose_plaintext(self):
        parts = []
        parts.append(f"Balance: ${self.balance}")
        if self.password:
            parts.append(f"Password: {self.password}")
        parts.extend(self.transaction_history)
        return "; ".join(parts)
