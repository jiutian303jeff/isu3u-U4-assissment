# bank_app_full.py
import random
import time
import tkinter as tk
from tkinter import messagebox

# ---------------- Encryption ----------------
class MultiAccountEncrypt:
    def __init__(self):
        self.alphabet = [chr(i) for i in range(65, 91)] + [",", ".", "!", "/", "?", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]
        self.n = len(self.alphabet)
        self.accounts = {}

    def generate_key(self):
        rotor1 = self.alphabet.copy()
        rotor2 = self.alphabet.copy()
        reflector = self.alphabet.copy()
        random.shuffle(rotor1)
        random.shuffle(rotor2)
        random.shuffle(reflector)
        plugboard = {'A':'#', '#':'A', 'B':'$','$':'B', 'C':'&','&':'C'}
        return {
            "rotor1": rotor1,
            "rotor2": rotor2,
            "reflector": reflector,
            "plugboard": plugboard,
            "rotor1_offset": 0,
            "rotor2_offset": 0
        }

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
        key["rotor1_offset"] = (key["rotor1_offset"] + 1) % self.n
        if key["rotor1_offset"] == 0:
            key["rotor2_offset"] = (key["rotor2_offset"] + 1) % self.n
        return char

    def encrypt_text(self, text, key):
        return ''.join(self.encrypt_char(c, key) for c in text)

    def add_account(self, account_name, plain_text):
        if account_name in self.accounts:
            raise ValueError("account exists")
        key = self.generate_key()
        key["rotor1_offset"] = 0
        key["rotor2_offset"] = 0
        encrypted = self.encrypt_text(plain_text, key)
        self.accounts[account_name] = {"key": key, "data": plain_text, "encrypted": encrypted}
        return encrypted

    def update_account(self, account_name, plain_text):
        if account_name not in self.accounts:
            raise ValueError("no such account")
        key = self.accounts[account_name]["key"]
        key["rotor1_offset"] = 0
        key["rotor2_offset"] = 0
        encrypted = self.encrypt_text(plain_text, key)
        self.accounts[account_name]["data"] = plain_text
        self.accounts[account_name]["encrypted"] = encrypted
        return encrypted

    def load_account_cipher(self, account_name, encrypted_text):
        if account_name in self.accounts:
            key = self.accounts[account_name]["key"]
            key["rotor1_offset"] = 0
            key["rotor2_offset"] = 0
            plain = self.encrypt_text(encrypted_text, key)
            self.accounts[account_name]["data"] = plain
            self.accounts[account_name]["encrypted"] = encrypted_text
            return plain
        else:
            self.accounts[account_name] = {"key": None, "data": None, "encrypted": encrypted_text}
            return None

# ---------------- Data ----------------
class Data:
    INTEREST_RATE = 0.0225  # daily 2.25%
    def __init__(self, username="", password="", balance=0, transaction_history=None, encrypt_manager=None, filename_template="encrypted_{username}.txt"):
        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = transaction_history or []
        self.filename_template = filename_template
        self.manager = encrypt_manager
        self.last_update_time = time.time()

    def filename(self, username=None):
        u = username if username else self.username
        return self.filename_template.format(username=u)

    def pull_data(self, username=None):
        if username:
            self.username = username
        if not self.username or not self.manager:
            return False
        fname = self.filename()
        try:
            with open(fname,"r") as f:
                line=f.read().strip()
        except:
            return False
        if ":" not in line:
            return False
        name, encrypted=line.split(":",1)
        if name != self.username:
            return False
        if self.username in self.manager.accounts:
            key = self.manager.accounts[self.username]["key"]
            key["rotor1_offset"]=0
            key["rotor2_offset"]=0
            plain=self.manager.encrypt_text(encrypted,key)
            self._parse_plaintext(plain)
            self.manager.accounts[self.username]["data"]=plain
            self.manager.accounts[self.username]["encrypted"]=encrypted
            return True
        else:
            return False

    def save_data(self):
        if not self.manager or not self.username:
            return False
        plain=self._compose_plaintext()
        if self.username not in self.manager.accounts:
            encrypted=self.manager.add_account(self.username,plain)
        else:
            encrypted=self.manager.update_account(self.username,plain)
        fname=self.filename()
        try:
            with open(fname,"w") as f:
                f.write(f"{self.username}:{encrypted}")
        except:
            return False
        return True

    def apply_interest(self):
        now = time.time()
        days = int((now - self.last_update_time) // (24*60*60))
        if days > 0:
            for _ in range(days):
                self.balance *= (1+self.INTEREST_RATE)
            self.last_update_time += days*24*60*60
            self.save_data()

    def deposit(self, amount, note=None):
        try:
            amt=float(amount)
        except:
            return False
        if amt<=0:
            return False
        self.apply_interest()
        self.balance += amt
        ts=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transaction_history.append(f"Deposit ${amt:.2f} at {ts}" + (f" ({note})" if note else ""))
        return self.save_data()

    def withdraw(self, amount, note=None):
        try:
            amt=float(amount)
        except:
            return False
        self.apply_interest()
        if amt<=0 or self.balance<amt:
            return False
        self.balance -= amt
        ts=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transaction_history.append(f"Withdraw ${amt:.2f} at {ts}" + (f" ({note})" if note else ""))
        return self.save_data()

    def transfer(self,target_username,amount,note=None):
        try:
            amt=float(amount)
        except:
            return False
        self.apply_interest()
        if amt<=0 or self.balance<amt:
            return False
        target=Data(username=target_username,encrypt_manager=self.manager)
        if not target.pull_data(target_username):
            return False
        target.apply_interest()
        self.balance -= amt
        target.balance += amt
        ts=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transaction_history.append(f"Transfer to {target_username} ${amt:.2f} at {ts}" + (f" ({note})" if note else ""))
        target.transaction_history.append(f"Transfer from {self.username} ${amt:.2f} at {ts}" + (f" ({note})" if note else ""))
        return self.save_data() and target.save_data()

    def get_balance(self):
        self.apply_interest()
        return self.balance

    def get_history(self):
        return list(self.transaction_history)

    def set_password(self,new_password):
        if not isinstance(new_password,str) or not new_password:
            return False
        self.password=new_password
        return self.save_data()

    def _parse_plaintext(self,text):
        self.transaction_history=[]
        self.balance=0
        self.password=""
        parts=[p.strip() for p in text.split(";") if p.strip()]
        for p in parts:
            if p.lower().startswith("balance:"):
                val=p.split(":",1)[1].strip()
                digits="".join(ch for ch in val if ch.isdigit() or ch=="." or ch=="-")
                try:
                    if "." in digits:
                        self.balance=float(digits)
                    else:
                        self.balance=int(digits) if digits!="" else 0
                except:
                    self.balance=0
            elif p.lower().startswith("password:"):
                self.password=p.split(":",1)[1].strip()
            else:
                self.transaction_history.append(p)

    def _compose_plaintext(self):
        parts=[]
        parts.append(f"Balance: ${self.balance}")
        if self.password:
            parts.append(f"Password: {self.password}")
        parts.extend(self.transaction_history)
        return "; ".join(parts)

# ---------------- GUI ----------------
class BankApp:
    def __init__(self,root,manager):
        self.root=root
        self.manager=manager
        self.bg="#fde6a3"
        self.root.title("Bank App")
        self.root.geometry("480x360")
        self.root.configure(bg=self.bg)
        self.current_data=None
        self.show_login()

    def show_login(self):
        if hasattr(self,'last_frame') and self.last_frame:
            self.last_frame.destroy()
        frame=tk.Frame(self.root,bg=self.bg)
        frame.pack(padx=20,pady=20)
        tk.Label(frame,text="Username:",bg=self.bg).grid(row=0,column=0,pady=4)
        tk.Label(frame,text="Password:",bg=self.bg).grid(row=1,column=0,pady=4)
        self.entry_username=tk.Entry(frame)
        self.entry_username.grid(row=0,column=1,pady=4)
        self.entry_password=tk.Entry(frame,show="*")
        self.entry_password.grid(row=1,column=1,pady=4)
        tk.Button(frame,text="Login",command=self.login,bg=self.bg).grid(row=2,column=0,pady=6)
        tk.Button(frame,text="Register",command=self.show_register,bg=self.bg).grid(row=2,column=1,pady=6)
        self.last_frame=frame

    def show_register(self):
        if hasattr(self,'last_frame') and self.last_frame:
            self.last_frame.destroy()
        frame=tk.Frame(self.root,bg=self.bg)
        frame.pack(padx=20,pady=20)
        tk.Label(frame,text="New Username:",bg=self.bg).grid(row=0,column=0,pady=4)
        tk.Label(frame,text="New Password:",bg=self.bg).grid(row=1,column=0,pady=4)
        self.entry_new_user=tk.Entry(frame)
        self.entry_new_user.grid(row=0,column=1,pady=4)
        self.entry_new_pass=tk.Entry(frame,show="*")
        self.entry_new_pass.grid(row=1,column=1,pady=4)
        tk.Button(frame,text="Create Account",command=self.register,bg=self.bg).grid(row=2,column=0,pady=6)
        tk.Button(frame,text="Back",command=self.show_login,bg=self.bg).grid(row=2,column=1,pady=6)
        self.last_frame=frame

    def login(self):
        u=self.entry_username.get().strip()
        p=self.entry_password.get().strip()
        if not u or not p:
            messagebox.showerror("Error","Enter username and password")
            return
        d=Data(username=u,encrypt_manager=self.manager)
        if not d.pull_data(u):
            messagebox.showerror("Error","Username not found")
            return
        if d.password!=p:
            messagebox.showerror("Error","Incorrect password")
            return
        self.current_data=d
        self.show_account_home()

    def register(self):
        u=self.entry_new_user.get().strip()
        p=self.entry_new_pass.get().strip()
        if not u or not p:
            messagebox.showerror("Error","Enter username and password")
            return
        d=Data(username=u,password=p,encrypt_manager=self.manager)
        d.transaction_history.append(f"Account created at {time.strftime('%Y-%m-%d',time.localtime())}")
        if not d.save_data():
            messagebox.showerror("Error","Could not create account (maybe exists)")
            return
        messagebox.showinfo("Success",f"Account {u} created")
        self.show_login()

    def show_account_home(self):
        if hasattr(self,'last_frame') and self.last_frame:
            self.last_frame.destroy()
        frame=tk.Frame(self.root,bg=self.bg)
        frame.pack(padx=20,pady=20)
        bal=self.current_data.get_balance()
        tk.Label(frame,text=f"Hello {self.current_data.username}! Balance: ${bal:.2f}",bg=self.bg,font=("Arial",14)).pack(pady=6)
        tk.Button(frame,text="Deposit",command=self.ui_deposit,bg=self.bg).pack(pady=4)
        tk.Button(frame,text="Withdraw",command=self.ui_withdraw,bg=self.bg).pack(pady=4)
        tk.Button(frame,text="Transfer",command=self.ui_transfer,bg=self.bg).pack(pady=4)
        tk.Button(frame,text="History",command=self.show_history,bg=self.bg).pack(pady=4)
        tk.Button(frame,text="Logout",command=self.logout,bg=self.bg).pack(pady=6)
        self.last_frame=frame

    def ui_deposit(self):
        top=tk.Toplevel(self.root)
        top.configure(bg=self.bg)
        top.title("Deposit")
        tk.Label(top,text="Amount:",bg=self.bg).pack(padx=6,pady=4)
        entry=tk.Entry(top)
        entry.pack(padx=6,pady=4)
        def do_deposit():
            amt=entry.get().strip()
            if self.current_data.deposit(amt,"GUI"):
                messagebox.showinfo("Success",f"Deposited ${amt}")
                top.destroy()
                self.show_account_home()
            else:
                messagebox.showerror("Failed","Deposit failed")
        tk.Button(top,text="Confirm",command=do_deposit,bg=self.bg).pack(pady=4)

    def ui_withdraw(self):
        top=tk.Toplevel(self.root)
        top.configure(bg=self.bg)
        top.title("Withdraw")
        tk.Label(top,text="Amount:",bg=self.bg).pack(padx=6,pady=4)
        entry=tk.Entry(top)
        entry.pack(padx=6,pady=4)
        def do_withdraw():
            amt=entry.get().strip()
            if self.current_data.withdraw(amt,"GUI"):
                messagebox.showinfo("Success",f"Withdrew ${amt}")
                top.destroy()
                self.show_account_home()
            else:
                messagebox.showerror("Failed","Withdraw failed")
        tk.Button(top,text="Confirm",command=do_withdraw,bg=self.bg).pack(pady=4)

    def ui_transfer(self):
        top=tk.Toplevel(self.root)
        top.configure(bg=self.bg)
        top.title("Transfer")
        tk.Label(top,text="Target Username:",bg=self.bg).pack(padx=6,pady=2)
        entry_target=tk.Entry(top)
        entry_target.pack(padx=6,pady=2)
        tk.Label(top,text="Amount:",bg=self.bg).pack(padx=6,pady=2)
        entry_amt=tk.Entry(top)
        entry_amt.pack(padx=6,pady=2)
        def do_transfer():
            tgt=entry_target.get().strip()
            amt=entry_amt.get().strip()
            if self.current_data.transfer(tgt,amt,"GUI"):
                messagebox.showinfo("Success",f"Transferred ${amt} to {tgt}")
                top.destroy()
                self.show_account_home()
            else:
                messagebox.showerror("Failed","Transfer failed")
        tk.Button(top,text="Confirm",command=do_transfer,bg=self.bg).pack(pady=4)

    def show_history(self):
        top=tk.Toplevel(self.root)
        top.configure(bg=self.bg)
        top.title("History")
        txt=tk.Text(top,width=60,height=20)
        txt.pack()
        for line in self.current_data.get_history():
            txt.insert("end",line+"\n")

    def logout(self):
        if self.current_data:
            self.current_data.save_data()
        self.current_data=None
        self.show_login()

# ---------------- Main ----------------
if __name__=="__main__":
    manager=MultiAccountEncrypt()
    root=tk.Tk()
    app=BankApp(root,manager)
    root.mainloop()
