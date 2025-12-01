"""


"""

import time

class Data:
    def __init__(self, username="", password="", balance=0, transaction_history=None,
                 encrypt_manager=None, filename_template="encrypted_{username}.txt"):

        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = transaction_history or []
        self.filename_template = filename_template

        
        self.manager = encrypt_manager

    def filename(self, username=None):
        u = username if username else self.username
        return self.filename_template.format(username=u)

    def pull_data(self, username=None):
        if username:
            self.username = username
        if not self.username:
            return False
        if not self.manager:
            return False

        fname = self.filename()

        loaded = False
        for loader_name in ("load_from_file", "load_accounts_from_file", "load_accounts", "load_all"):
            loader = getattr(self.manager, loader_name, None)
            if callable(loader):
                try:
                    try:
                        loader(fname)
                    except TypeError:
                        loader()
                    loaded = True
                    break
                except Exception:
                    pass

        if not loaded:
            return False

        acct = None
        if hasattr(self.manager, "accounts"):
            acct = self.manager.accounts.get(self.username)

        if acct is None and hasattr(self.manager, "accounts") and len(self.manager.accounts) == 1:
            acct = next(iter(self.manager.accounts.values()))

        if acct is None:
            return False

        data_plain = acct.get("data")
        if not data_plain:
            encrypted = acct.get("encrypted", "")
            key = acct.get("key")
            if key:
                key["rotor1_offset"] = 0
                key["rotor2_offset"] = 0

            data_plain = None
            for fn in ("encrypt_text", "encrypt", "decrypt"):
                method = getattr(self.manager, fn, None)
                if callable(method):
                    try:
                        if fn == "encrypt_text" and key:
                            data_plain = method(encrypted, key)
                        else:
                            data_plain = method(encrypted)
                        break
                    except:
                        pass
            if data_plain is None:
                return False

        self._parse_plaintext(data_plain)
        return True

    def save_data(self):
        if not self.manager:
            return False
        if not self.username:
            return False
        if self.error_handle():
            return False

        plain = self._compose_plaintext()

        try:
            if hasattr(self.manager, "add_account") and self.username not in self.manager.accounts:
                self.manager.add_account(self.username, plain)
            else:
                if hasattr(self.manager, "update_account"):
                    try:
                        self.manager.update_account(self.username, plain, filename=self.filename())
                    except TypeError:
                        self.manager.update_account(self.username, plain)
                else:
                    key = self.manager.accounts[self.username]["key"]
                    key["rotor1_offset"] = 0
                    key["rotor2_offset"] = 0
                    if hasattr(self.manager, "encrypt_text"):
                        enc = self.manager.encrypt_text(plain, key)
                    else:
                        enc = self.manager.encrypt(plain)
                    self.manager.accounts[self.username]["data"] = plain
                    self.manager.accounts[self.username]["encrypted"] = enc

        except Exception:
            return False

        saver = (
            getattr(self.manager, "save_to_file", None)
            or getattr(self.manager, "save_accounts_to_file", None)
        )

        if callable(saver):
            try:
                saver(self.filename())
            except TypeError:
                saver()
        else:
            enc = self.manager.accounts[self.username]["encrypted"]
            with open(self.filename(), "wb") as f:
                f.write(f"{self.username}:{enc}\n".encode("utf-8"))

        return True


    def deposit(self, amount, note=None):
        try:
            amt = float(amount)
        except:
            return False
        if amt <= 0:
            return False

        self.balance += amt
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transaction_history.append(
            f"Deposit ${amt:.2f} at {ts}" + (f" ({note})" if note else "")
        )
        return self.save_data()

    def withdraw(self, amount, note=None):
        try:
            amt = float(amount)
        except:
            return False
        if amt <= 0 or amt > self.balance:
            return False

        self.balance -= amt
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transaction_history.append(
            f"Withdraw ${amt:.2f} at {ts}" + (f" ({note})" if note else "")
        )
        return self.save_data()

    def transfer(self, target_username, amount, note=None):
        try:
            amt = float(amount)
        except:
            return False
        if amt <= 0 or amt > self.balance:
            return False

        from data import Data 

        target = Data(
            username=target_username,
            encrypt_manager=self.manager,
            filename_template=self.filename_template
        )

        if not target.pull_data(target_username):
            return False

        self.balance -= amt
        target.balance += amt

        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.transaction_history.append(
            f"Transfer to {target_username} ${amt:.2f} at {ts}" + (f" ({note})" if note else "")
        )
        target.transaction_history.append(
            f"Transfer from {self.username} ${amt:.2f} at {ts}" + (f" ({note})" if note else "")
        )

        return self.save_data() and target.save_data()

    def get_balance(self):
        return self.balance

    def get_history(self):
        return list(self.transaction_history)
    def set_password(self, new_password):
        if not new_password:
            return False
        self.password = new_password
        return self.save_data()

    def error_handle(self):
        if not self.username:
            return "invalid username"
        if not self.password:
            return "invalid password"
        return None

    def _parse_plaintext(self, text):
        self.transaction_history = []
        self.balance = 0
        self.password = ""

        parts = [p.strip() for p in text.split(";") if p.strip()]

        for p in parts:
            if p.lower().startswith("balance:"):
                val = "".join(ch for ch in p if ch.isdigit() or ch == "." or ch == "-")
                try:
                    self.balance = float(val)
                except:
                    self.balance = 0

            elif p.lower().startswith("password:"):
                self.password = p.split(":", 1)[1].strip()

            else:
                self.transaction_history.append(p)

    def _compose_plaintext(self):
        parts = [
            f"Balance: ${self.balance}",
            f"Password: {self.password}",
        ]
        parts.extend(self.transaction_history)
        return "; ".join(parts)
