from encrypt import Encrypt
import time

"""
Data model for account storage.
Stores: full_name, username, password, balance, account_number, date_opened,
transaction_history and interest_rate.

Files are stored encrypted using the provided Encrypt manager.
Filename template default: "encrypted_{username}.txt"
"""

class Data:
    def __init__(self, username="", password="", balance=0, transaction_history=None,
                 encrypt_manager=None, filename_template="encrypted_{username}.txt",
                 full_name="", account_number=None, date_opened=None, interest_rate=0.0225):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.balance = float(balance or 0.0)
        self.transaction_history = transaction_history or []
        # use underscore template by default for consistency
        self.filename_template = filename_template
        self.manager = encrypt_manager or Encrypt()
        self.account_number = account_number
        self.date_opened = date_opened
        self.interest_rate = float(interest_rate)
        # remember the exact file we loaded from so saves go back to same file
        self._loaded_filename = None

    def get_encrypted_filename(self):
        """Return the primary filename for this account."""
        return self.filename_template.format(username=self.username)

    def _possible_filenames(self, username):
        """Common filename variants to try."""
        return [
            f"encrypted_{username}.txt",
            f"encrypted {username}.txt",
            f"encrypted{username}.txt",
            f"encrypted-{username}.txt",
            self.filename_template.format(username=username),
        ]

    def save_data(self):
        """
        Serialize account fields, encrypt and write to file.
        Prefer writing back to the same filename we loaded from, if any.
        Format before encryption:
          full_name,username,password,balance,account_number,date_opened,tx1;tx2;...
        """
        if not self.date_opened:
            self.date_opened = time.strftime("%Y-%m-%d", time.localtime())
        account_number = self.account_number or ""
        txs = ";".join(self.transaction_history)
        plain = f"{self.full_name},{self.username},{self.password},{self.balance},{account_number},{self.date_opened},{txs}"
        ciphertext = self.manager.encrypt(plain)

        # prefer the originally loaded filename so we don't create duplicate files
        fname = self._loaded_filename if getattr(self, "_loaded_filename", None) else self.get_encrypted_filename()

        # try to write; if path has dirs and write fails, fallback to base name
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(ciphertext)
        except Exception:
            # fallback: write to base filename only (no os import)
            if "\\" in fname:
                base = fname.split("\\")[-1]
            elif "/" in fname:
                base = fname.split("/")[-1]
            else:
                base = fname
            with open(base, "w", encoding="utf-8") as f:
                f.write(ciphertext)
            # record that we saved to fallback name
            self._loaded_filename = base

        return True

    def find_encrypted_payload(self, username):
        """
        Locate and validate an encrypted payload for username.
        Returns (payload, filename) or (None, None).
        """
        if not self.manager:
            self.manager = Encrypt()

        # try variants
        for fname in self._possible_filenames(username):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    payload = f.read().strip()
                    if not payload:
                        continue
                    plain = self.manager.decrypt(payload)
                    if not plain or "," not in plain:
                        if hasattr(self.manager, "decrypt_old"):
                            plain = self.manager.decrypt_old(payload)
                    if plain and "," in plain:
                        return payload, fname
            except FileNotFoundError:
                continue
            except Exception:
                continue

        # fallback combined file
        try:
            with open("encrypted_users.txt", "r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    if ':' not in line:
                        continue
                    name, payload = line.split(':', 1)
                    if name.strip() != username:
                        continue
                    payload = payload.strip()
                    if not payload:
                        continue
                    plain = self.manager.decrypt(payload)
                    if not plain or "," not in plain:
                        if hasattr(self.manager, "decrypt_old"):
                            plain = self.manager.decrypt_old(payload)
                    if plain and "," in plain:
                        return payload, "encrypted_users.txt"
        except FileNotFoundError:
            pass
        except Exception:
            pass

        return None, None

    def pull_data(self, username):
        """
        Load account from disk. Populate fields.
        Returns True on success, False if no valid data found.
        """
        payload, fname = self.find_encrypted_payload(username)
        if not payload:
            return False

        # remember loaded filename so future saves go to same place
        self._loaded_filename = fname

        plain = self.manager.decrypt(payload)
        if (not plain or "," not in plain) and hasattr(self.manager, "decrypt_old"):
            plain = self.manager.decrypt_old(payload)
        if not plain or "," not in plain:
            return False
        parts = plain.split(',', 6)
        if len(parts) < 6:
            return False
        self.full_name = parts[0]
        self.username = parts[1]
        self.password = parts[2]
        try:
            self.balance = float(parts[3])
        except Exception:
            self.balance = 0.0
        self.account_number = parts[4] if parts[4] else None
        self.date_opened = parts[5] if parts[5] else None
        txs = parts[6] if len(parts) > 6 else ""
        self.transaction_history = txs.split(';') if txs else []
        return True

    def change_password(self, new_password):
        """Change password and persist."""
        self.password = new_password
        return self.save_data()

    def compute_savings_interest(self):
        """Compute interest since date_opened using daily compounding (time module)."""
        if not self.date_opened:
            return 0.0
        try:
            opened_struct = time.strptime(self.date_opened, "%Y-%m-%d")
            opened_ts = time.mktime(opened_struct)
            now_ts = time.time()
            days = int((now_ts - opened_ts) // 86400)
        except Exception:
            return 0.0
        if days <= 0:
            return 0.0
        daily = self.interest_rate / 365.0
        interest = self.balance * ((1 + daily) ** days - 1)
        return interest

    def get_savings_balance(self):
        """Return balance plus accrued interest (not applied)."""
        return self.balance + self.compute_savings_interest()

    def deposit(self, amount, note=""):
        try:
            amt = float(amount)
        except Exception:
            return False
        if amt <= 0:
            return False
        self.balance += amt
        entry = f"Deposited {amt:.2f}"
        if note:
            entry += f" - {note}"
        self.transaction_history.append(entry)
        return self.save_data()

    def withdraw(self, amount, note=""):
        try:
            amt = float(amount)
        except Exception:
            return False
        if amt <= 0 or amt > self.balance:
            return False
        self.balance -= amt
        entry = f"Withdrew {amt:.2f}"
        if note:
            entry += f" - {note}"
        self.transaction_history.append(entry)
        return self.save_data()

    def transfer(self, target_username, amount, note=""):
        try:
            amt = float(amount)
        except Exception:
            return False
        if amt <= 0 or amt > self.balance:
            return False
        self.balance -= amt
        entry = f"Transferred {amt:.2f} to {target_username}"
        if note:
            entry += f" - {note}"
        self.transaction_history.append(entry)
        return self.save_data()