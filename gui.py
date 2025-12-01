"""


"""

from data import Data
import tkinter as tk
import time
import tkinter.messagebox as messagebox
from encrypt import Encrypt

class Animation:
    def __init__(self, manager=None):
        self.root = tk.Tk()
        self.root.title("Splash Screen")
        self.stop_animation = True

        # ensure a manager exists
        self.manager = manager or Encrypt()

        self.show_splash()

        self.root.mainloop()
        
    def show_splash(self):
        self.splash_frame = tk.Frame(self.root, bg="#fde6a3")
        self.splash_frame.pack(fill="both", expand=True)

        self.frames = []
        base_path = r"ezgif-split"

        for i in range(16): 
            filename = fr"{base_path}\frame_{i:02d}_delay-0.05s.gif"
            self.frames.append(tk.PhotoImage(file=filename))

        self.frame_index = 0
        self.splash_label = tk.Label(self.splash_frame, image=self.frames[0])
        self.splash_label.pack()
        self.label = tk.Label(self.splash_frame, text="Loading......", bg="#fde6a3")
        self.label.pack()

        self.animate_frames()
        self.root.after(5000, self.open_main)

    def animate_frames(self):
        if not self.stop_animation:
            return
        
        self.splash_label.config(image=self.frames[self.frame_index],bg="#fde6a3")

        self.frame_index = (self.frame_index + 1) % len(self.frames)

        self.root.after(120, self.animate_frames)

    def open_main(self):
        self.stop_animation = False
        self.splash_frame.destroy()
        # pass the manager to the main page
        Base_page(self.root, manager=self.manager)

# change Base_page to not inherit from Animation and accept manager
class Base_page:
    def __init__(self, root, manager=None):
        self.main_win = root
        self.manager = manager
        self.main_win.config(bg="#fde6a3")
        self.last_page = None
        current_time_struct = time.localtime()
        self.time_date = time.strftime("%Y-%m-%d", current_time_struct)
        self.time_time = time.strftime("%y-%m-%d, %H:%M:%S", current_time_struct)
        self.home_page()

    # helper: destroy any widget attributes before opening a new view
    def clear_frames(self):
        # find attributes that look like tkinter widgets (have destroy())
        names = [n for n, v in vars(self).items() if hasattr(v, "destroy")]
        for name in names:
            # avoid destroying the root window
            if name in ("main_win", "root"):
                continue
            try:
                widget = getattr(self, name)
                widget.destroy()
            except Exception:
                pass
            try:
                delattr(self, name)
            except Exception:
                pass

    def home_page(self):
        self.big_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.big_frame.pack()

        self.frame1 = tk.Frame(self.big_frame, bg="#fde6a3")
        self.frame1.pack()
        self.frame2 = tk.Frame(self.big_frame, bg="#fde6a3")
        self.frame2.pack()
        self.frame3 = tk.Frame(self.big_frame, bg="#fde6a3")
        self.frame3.pack()
        self.frame4 = tk.Frame(self.big_frame, bg="#fde6a3")
        self.frame4.pack()

        self.label_welcome = tk.Label(self.frame1, text="Welcome", font=("Arial", 20), bg="#fde6a3")
        self.label_welcome.pack(expand=True)

        self.label_username = tk.Label(self.frame2, text="username:  ", bg="#fde6a3")
        self.label_username.pack(side="left")
        self.enter_username = tk.Entry(self.frame2, width=20)
        self.enter_username.pack(side="right")

        self.label_password = tk.Label(self.frame3, text="password:  ", bg="#fde6a3")
        self.label_password.pack(side="left")
        self.enter_password = tk.Entry(self.frame3, width=20, show='*')
        self.enter_password.pack(side="right")

        self.login = tk.Button(self.frame4, text="Login", command=self.logging, bg="#fde6a3")
        self.login.pack(side="left")
        
        self.create_account = tk.Button(self.frame4, text="Register", command=self.register, bg="#fde6a3")
        self.create_account.pack(side="right")

    def register(self):
        self.big_frame.pack_forget()
        self.register_main = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.register_main.pack()

        self.last_page = self.register_main

        self.label_indicate = tk.Label(self.register_main, text="Here to register", font=("Arial", 20), bg="#fde6a3")
        self.label_indicate.pack(expand=True)
        
        self.register_frame1 = tk.Frame(self.register_main, bg='#fde6a3')
        self.register_frame1.pack()

        self.register_frame2 = tk.Frame(self.register_main, bg="#fde6a3")
        self.register_frame2.pack()

        self.creating_username = tk.Label(self.register_frame1, text="Enter a username:  ", bg="#fde6a3")
        self.creating_username.pack(side="left")
        self.enter_username = tk.Entry(self.register_frame1, width=20)
        self.enter_username.pack(side="right")

        self.creating_password = tk.Label(self.register_frame2, text="Enter a password:  ", bg='#fde6a3')
        self.creating_password.pack(side="left")
        self.enter_password = tk.Entry(self.register_frame2, width=20, show='*')
        self.enter_password.pack(side="right")

        # Always show the register button; validation happens when the
        # user clicks it (in `creating_account`).
        self.register_button = tk.Button(self.register_main, text="Register a new account", command=self.creating_account, bg='#fde6a3')
        self.register_button.pack()
        
        self.back_to_main = tk.Button(self.register_main, text="Back to main page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack()

    def logging(self):
        username = self.enter_username.get().strip()
        password = self.enter_password.get().strip()

        d = Data(username=username, encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")
        ok = d.pull_data(username)
        if not ok:
            messagebox.showerror("login failed", "Username not found")
            return

        if d.password != password:
            messagebox.showerror("login failed", "Incorrect password")
            return

        self.current_data = d
        self.show_account_home()

    def save_check(self):
        # ensure previous frames are removed before creating the account chooser
        self.clear_frames()

        self.choosing_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.choosing_frame.pack()

        self.time = tk.Label(self.choosing_frame, text=self.time_date, font=("Arial", 20), bg='#fde6a3')
        self.time.pack()
        self.saving = tk.Button(self.choosing_frame, text="Saving account", command=self.saving_account, bg='#fde6a3')
        self.saving.pack()
        self.checking = tk.Button(self.choosing_frame, text="Checking account", command=self.checking_account, bg="#fde6a3")
        self.checking.pack()

        self.quit = tk.Button(self.choosing_frame, text="Quit", command=self.quiting, bg="#fde6a3")
        self.quit.pack()    

    def saving_account(self, balance=None):
        # use current account balance if available
        if balance is None and hasattr(self, "current_data"):
            balance = self.current_data.balance

        # safe username lookup: prefer current_data, fallback to entry (guarded)
        if hasattr(self, "current_data") and getattr(self, "current_data") is not None:
            username_display = self.current_data.username
        else:
            try:
                username_display = self.enter_username.get()
            except Exception:
                username_display = ""

        # remove previous chooser frame and build saving view
        try:
            self.choosing_frame.pack_forget()
        except Exception:
            pass

        self.saving_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.saving_frame.pack() 

        self.show_save_info = tk.Frame(self.saving_frame, bg="#fde6a3")
        self.show_save_info.pack()

        self.sav_choosing = tk.Frame(self.saving_frame, bg="#fde6a3")
        self.sav_choosing.pack()

        self.quit_leave = tk.Frame(self.saving_frame, bg="#fde6a3")
        self.quit_leave.pack()

        self.last_page = self.saving_frame

        self.balance_label = tk.Label(self.show_save_info, text="Hello %s!! Your balance is: %.2f" % (username_display, balance), bg="#fde6a3")
        self.balance_label.pack()

        self.interest_label = tk.Label(self.show_save_info, text="Your interest rate is: 2.25%", bg="#fde6a3")
        self.interest_label.pack()

        self.asking = tk.Label(self.sav_choosing, text="Would you like to......", bg="#fde6a3")
        self.asking.pack()

        self.transfer = tk.Button(self.sav_choosing, text="Transfer funds", command=self.transfering, bg="#fde6a3")
        self.transfer.pack()

        self.quit = tk.Button(self.quit_leave, text="Quit the program", command=self.quiting, bg="#fde6a3")
        self.quit.pack(side="left")

        self.back_to_main = tk.Button(self.quit_leave, text="Back to main page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack(side="right")

        # new: add button to return to account choosing page
        self.back_to_accounts = tk.Button(self.quit_leave, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.back_to_accounts.pack(side="right")

    def checking_account(self, balance=None):
        # use current account balance if available
        if balance is None and hasattr(self, "current_data"):
            balance = self.current_data.balance

        # safe username lookup: prefer current_data, fallback to entry (guarded)
        if hasattr(self, "current_data") and getattr(self, "current_data") is not None:
            username_display = self.current_data.username
        else:
            try:
                username_display = self.enter_username.get()
            except Exception:
                username_display = ""

        try:
            self.choosing_frame.pack_forget()
        except Exception:
            pass

        self.checking_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.checking_frame.pack()

        self.show_check_info = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.show_check_info.pack()

        self.chec_choose = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.chec_choose.pack()

        self.quit_and_leave = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.quit_and_leave.pack()

        self.last_page = self.checking_frame

        self.c_balance_label = tk.Label(self.show_check_info, text="Hello %s!! Your balance is: %.2f" % (username_display, balance), bg="#fde6a3")
        self.c_balance_label.pack()

        self.c_asking = tk.Label(self.chec_choose, text="Would you like to......", bg="#fde6a3")
        self.c_asking.pack()

        self.withdraw_money = tk.Button(self.chec_choose, text="Withdraw money", command=self.withdraw, bg="#fde6a3")
        self.withdraw_money.pack()
        
        self.deposit_money = tk.Button(self.chec_choose, text="Deposit money", command=self.deposit, bg="#fde6a3")
        self.deposit_money.pack()

        self.quit = tk.Button(self.quit_and_leave, text="Quit the program", command=self.quiting, bg="#fde6a3")
        self.quit.pack(side="left")

        self.back_to_main = tk.Button(self.quit_and_leave, text="Back to home page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack(side="right")

        # new: add button to return to account choosing page
        self.back_to_accounts = tk.Button(self.quit_and_leave, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.back_to_accounts.pack(side="right")

    def back_main(self):
        if self.last_page is not None:
            self.last_page.pack_forget()
        self.last_page = None
        self.home_page()

    def quiting(self):
        self.main_win.quit()
        self.main_win.destroy()
        
    def transfering(self):
        # Build transfer UI: target account, amount, current user's password
        try:
            self.last_page.pack_forget()
        except Exception:
            pass

        self.transfer_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.transfer_frame.pack()

        self.transfer_top = tk.Frame(self.transfer_frame, bg="#fde6a3")
        self.transfer_top.pack()

        self.transfer_mid = tk.Frame(self.transfer_frame, bg="#fde6a3")
        self.transfer_mid.pack()

        self.transfer_bot = tk.Frame(self.transfer_frame, bg="#fde6a3")
        self.transfer_bot.pack()

        self.to_label = tk.Label(self.transfer_top, text="Account transfer to:", bg="#fde6a3")
        self.to_label.pack(side="left")
        self.to_entry = tk.Entry(self.transfer_top, width=20)
        self.to_entry.pack(side="right")

        self.amount_label = tk.Label(self.transfer_mid, text="Amount:", bg="#fde6a3")
        self.amount_label.pack(side="left")
        self.amount_entry = tk.Entry(self.transfer_mid, width=20)
        self.amount_entry.pack(side="right")

        self.pw_label = tk.Label(self.transfer_bot, text="Your password:", bg="#fde6a3")
        self.pw_label.pack(side="left")
        self.pw_entry = tk.Entry(self.transfer_bot, width=20, show='*')
        self.pw_entry.pack(side="right")

        self.confirm_transfer = tk.Button(self.transfer_frame, text="Confirm Transfer", command=self.start_transfer, bg="#fde6a3")
        self.confirm_transfer.pack()

        self.transfer_back = tk.Button(self.transfer_frame, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.transfer_back.pack()

        self.last_page = self.transfer_frame

    def start_transfer(self):
        # Validate current_data
        if not hasattr(self, "current_data") or self.current_data is None:
            messagebox.showerror("Error", "No account loaded.")
            return

        target_username = self.to_entry.get().strip()
        amt_text = self.amount_entry.get().strip()
        entered_pw = self.pw_entry.get().strip()

        if not target_username:
            messagebox.showerror("Transfer Failed", "Target account cannot be empty.")
            return

        if not amt_text:
            messagebox.showerror("Transfer Failed", "Amount cannot be empty.")
            return

        try:
            amount = float(amt_text)
        except ValueError:
            messagebox.showerror("Transfer Failed", "Please enter a valid number for amount.")
            return

        if amount <= 0:
            messagebox.showerror("Transfer Failed", "Amount must be greater than zero.")
            return

        # verify password
        if entered_pw != self.current_data.password:
            messagebox.showerror("Transfer Failed", "Incorrect password for current account.")
            return

        # ensure sufficient funds
        if amount > self.current_data.balance:
            messagebox.showerror("Transfer Failed", "Insufficient funds.")
            return

        # load target account
        target = Data(username=target_username, encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")
        ok = target.pull_data(target_username)
        if not ok:
            messagebox.showerror("Transfer Failed", "Target account not found.")
            return

        # perform transfer: deduct from current, add to target
        note = f"Transfer to {target_username} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        ok1 = self.current_data.transfer(target_username, amount, note=note)
        if not ok1:
            messagebox.showerror("Transfer Failed", "Could not withdraw from current account.")
            return

        # deposit into target (deposit saves file)
        note_target = f"Received from {self.current_data.username} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        ok2 = target.deposit(amount, note=note_target)
        if not ok2:
            # try to rollback current (best-effort)
            self.current_data.deposit(amount, note=f"Rollback of failed transfer to {target_username}")
            messagebox.showerror("Transfer Failed", "Could not credit target account. Transfer rolled back.")
            return

        messagebox.showinfo("Transfer Successful", f"Transferred {amount:.2f} to {target_username}.")

        # return to checking view with updated balance
        try:
            self.transfer_frame.pack_forget()
        except Exception:
            pass
        self.checking_account(self.current_data.balance)
        
    def withdraw(self):
        self.checking_frame.pack_forget()
        self.withdraw_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.withdraw_frame.pack()

        self.withdraw_amount = tk.Frame(self.withdraw_frame, bg="#fde6a3")
        self.withdraw_amount.pack()

        self.confirm_withdraw = tk.Frame(self.withdraw_frame, bg="#fde6a3")
        self.confirm_withdraw.pack()

        self.withdraw_label = tk.Label(self.withdraw_amount, text="How much do you want to withdraw?", bg="#fde6a3")
        self.withdraw_label.pack(side="left")

        self.withdraw_enter = tk.Entry(self.withdraw_amount, width=20)
        self.withdraw_enter.pack(side='right')

        self.withdraw_confirm = tk.Button(self.confirm_withdraw, text="Confirm Withdraw", command=self.start_withdraw, bg="#fde6a3")
        self.withdraw_confirm.pack()

    def deposit(self):
        self.checking_frame.pack_forget()
        self.deposit_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.deposit_frame.pack()

        self.deposit_amount = tk.Frame(self.deposit_frame, bg="#fde6a3")
        self.deposit_amount.pack()

        self.confirm_deposit = tk.Frame(self.deposit_frame, bg="#fde6a3")
        self.confirm_deposit.pack()

        self.deposit_label = tk.Label(self.deposit_amount, text="How much do you want to deposit?", bg="#fde6a3")
        self.deposit_label.pack(side="left")

        self.deposit_enter = tk.Entry(self.deposit_amount, width=20)
        self.deposit_enter.pack(side='right')

        self.deposit_confirm = tk.Button(self.confirm_deposit, text="Confirm Deposit", command=self.start_deposit, bg="#fde6a3")
        self.deposit_confirm.pack()
        self.back_to_accounts = tk.Button(self.confirm_deposit, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.back_to_accounts.pack()
        

    def creating_account(self):
        username = self.enter_username.get().strip()
        password = self.enter_password.get().strip()
        initial_balance = 0

        # Validate inputs: do not allow empty username or password
        if not username or not password:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty.")
            return

        d = Data(username=username, password=password, balance=initial_balance,
                encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")

        d.transaction_history.append(f"Account created at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

        ok = d.save_data()
        if ok:
            messagebox.showinfo("Registration Successful", f"{username} has been created")
            self.back_main()
        else:
            messagebox.showerror("Registration Failed", "Could not create account.")

    def start_withdraw(self):
        amt = self.withdraw_enter.get().strip()
        try:
            amount = float(amt)
        except ValueError:
            messagebox.showerror("Invalid amount", "Please enter a valid number.")
            return

        if not hasattr(self, "current_data"):
            messagebox.showerror("Error", "No account loaded.")
            return

        ok = self.current_data.withdraw(amount, note=f"ATM withdraw at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if ok:
            messagebox.showinfo("Success", f"Withdrew {amount:.2f}")
        else:
            messagebox.showerror("Failed", "Insufficient funds or invalid amount.")

        # return to checking account view with updated balance
        self.withdraw_frame.pack_forget()
        self.checking_account(self.current_data.balance)

    def start_deposit(self):
        amt = self.deposit_enter.get().strip()
        try:
            amount = float(amt)
        except ValueError:
            messagebox.showerror("Invalid amount", "Please enter a valid number.")
            return

        if not hasattr(self, "current_data"):
            messagebox.showerror("Error", "No account loaded.")
            return

        ok = self.current_data.deposit(amount, note=f"ATM deposit at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if ok:
            messagebox.showinfo("Success", f"Deposited {amount:.2f}")
        else:
            messagebox.showerror("Failed", "Invalid amount.")

        # return to checking account view with updated balance
        self.deposit_frame.pack_forget()
        self.checking_account(self.current_data.balance)

    def show_account_home(self):
        """
        Called after successful login. Hide any login/register frames and show the
        account chooser (save_check). Ensures no AttributeError when invoked.
        """
        # safely hide known possible previous frames
        for name in ("big_frame", "register_main", "choosing_frame", "saving_frame", "checking_frame", "withdraw_frame", "deposit_frame"):
            if hasattr(self, name):
                try:
                    getattr(self, name).pack_forget()
                except Exception:
                    pass

        # update username entry used in other views (keep displayed username)
        if hasattr(self, "current_data"):
            # ensure the login username entry still reflects the current account
            try:
                self.enter_username.delete(0, tk.END)
                self.enter_username.insert(0, self.current_data.username)
            except Exception:
                pass

        # show the account chooser
        self.save_check()

main = Animation()