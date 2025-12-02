"""
author : Leo L. and jeff J.
date   : oct 30
desc   : Tkinter GUI for account manager/encryption demo.
       - Animation: splash screen showing GIF frames then opens Base_page
       - Base_page: main application class with views for login, register,
         account choosing, saving/checking, transfer, withdraw, deposit.
       Comments describe intent of major UI builders and helper functions.
"""
from data import Data
import tkinter as tk
import tkinter.messagebox as messagebox
import time
from encrypt import Encrypt

class Animation:
    """
    Splash screen animation class:
    - builds a small window, loads GIF frames, animates them
    - after a delay opens the main Base_page and hands manager instance
    """
    def __init__(self, manager=None):
        self.root = tk.Tk()
        self.root.title("Splash Screen")
        self.stop_animation = True

        # ensure a manager exists (Encrypt instance by default)
        self.manager = manager or Encrypt()

        self.show_splash()
        self.root.mainloop()
        
    def show_splash(self):
        """Build splash UI, preload frames and schedule animation/opening of main page."""
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
        """Cycle through preloaded frames until open_main cancels animation."""
        if not self.stop_animation:
            return
        
        self.splash_label.config(image=self.frames[self.frame_index], bg="#fde6a3")
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(120, self.animate_frames)

    def open_main(self):
        """Stop splash and open the Base_page (main UI)."""
        self.stop_animation = False
        self.splash_frame.destroy()
        Base_page(self.root, manager=self.manager)

class Base_page:
    """
    Main application UI and logic:
    - manages multiple pages (home, register, account chooser, saving/checking)
    - holds current_data (Data instance) after login
    - interacts with Encrypt manager for persisting account files
    """
    def __init__(self, root, manager=None):
        self.main_win = root
        self.manager = manager
        self.main_win.config(bg="#fde6a3")
        self.last_page = None
        current_time_struct = time.localtime()
        self.time_date = time.strftime("%Y-%m-%d", current_time_struct)
        self.time_time = time.strftime("%y-%m-%d, %H:%M:%S", current_time_struct)
        self.home_page()

    def clear_frames(self):
        """
        Destroy widget attributes on this instance that look like Tk widgets.
        This helps avoid orphaned widgets when switching views.
        """
        names = [n for n, v in vars(self).items() if hasattr(v, "destroy")]
        for name in names:
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

    def validate_password(self, password: str):
        """
        Policy check for registration passwords.
        Returns (True, '') if ok, otherwise (False, message).
        """
        reasons = []
        if not (6 <= len(password) <= 16):
            reasons.append("Password must be 6-16 characters long.")
        if not any(c.isupper() for c in password):
            reasons.append("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in password):
            reasons.append("Password must contain at least one lowercase letter.")
        allowed_symbols = set("!@#$%^&*()_-+={[}]|\"':;?/>.<,}")
        if not any(c in allowed_symbols for c in password):
            reasons.append("Password must contain at least one symbol: ! @ # $ % ^ & * ( ) _ - + = { [ ] } | \" ' : ; ? / > . < , }")
        if reasons:
            return False, "\n".join(reasons)
        return True, ""

    def debug_login(self):
        # simple debug helper: prints to console then calls logging() if present
        try:
            print("Login button clicked")
        except Exception:
            pass
        if hasattr(self, "logging"):
            try:
                self.logging()
            except Exception as e:
                print("logging() raised:", e)
        else:
            try:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Error", "logging() not implemented")
            except Exception:
                pass

    def home_page(self):
        """Build the initial home/login UI."""
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
        self.frame5 = tk.Frame(self.big_frame, bg="#fde6a3")
        self.frame5.pack()

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

        # replace the Login button command with debug wrapper
        self.login = tk.Button(self.frame4, text="Login", command=self.debug_login, bg="#fde6a3")
        self.login.pack(side="left")
        
        self.create_account = tk.Button(self.frame4, text="Register", command=self.register, bg="#fde6a3")
        self.create_account.pack(side="right")

        self.quit = tk.Button(self.frame5, text="Quit", command=self.quiting, bg="#fde6a3")
        self.quit.pack(side="bottom") 

    def register(self):
        """Show registration UI: full name, username, password, initial balance."""
        self.big_frame.pack_forget()
        self.register_main = tk.Frame(self.main_win, width=360, height=240, bg="#fde6a3")
        self.register_main.pack()
        self.last_page = self.register_main

        self.label_indicate = tk.Label(self.register_main, text="Register new account", font=("Arial", 16), bg="#fde6a3")
        self.label_indicate.pack(pady=6)

        # full name row
        row_full = tk.Frame(self.register_main, bg='#fde6a3')
        row_full.pack(pady=2)
        tk.Label(row_full, text="Full name:", bg="#fde6a3").pack(side="left")
        self.enter_fullname = tk.Entry(row_full, width=30)
        self.enter_fullname.pack(side="right")

        # username row
        row_user = tk.Frame(self.register_main, bg='#fde6a3')
        row_user.pack(pady=2)
        tk.Label(row_user, text="Username:", bg="#fde6a3").pack(side="left")
        self.enter_username = tk.Entry(row_user, width=30)
        self.enter_username.pack(side="right")

        # password row
        row_pw = tk.Frame(self.register_main, bg='#fde6a3')
        row_pw.pack(pady=2)
        tk.Label(row_pw, text="Password:", bg="#fde6a3").pack(side="left")
        self.enter_password = tk.Entry(row_pw, width=30, show='*')
        self.enter_password.pack(side="right")

        # initial balance row
        row_bal = tk.Frame(self.register_main, bg='#fde6a3')
        row_bal.pack(pady=2)
        tk.Label(row_bal, text="Initial balance:", bg="#fde6a3").pack(side="left")
        self.enter_initial_balance = tk.Entry(row_bal, width=20)
        self.enter_initial_balance.insert(0, "0.00")
        self.enter_initial_balance.pack(side="right")

        # buttons
        self.register_button = tk.Button(self.register_main, text="Create account", command=self.creating_account, bg='#fde6a3')
        self.register_button.pack(pady=6)
        self.back_to_main = tk.Button(self.register_main, text="Back to main page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack()

    def creating_account(self):
        """Create and persist a new account after validation. Enforce unique username."""
        full_name = getattr(self, "enter_fullname", tk.Entry()).get().strip()
        username = getattr(self, "enter_username", tk.Entry()).get().strip()
        password = getattr(self, "enter_password", tk.Entry()).get().strip()
        initial_balance_text = getattr(self, "enter_initial_balance", tk.Entry()).get().strip()
        try:
            initial_balance = float(initial_balance_text)
        except Exception:
            messagebox.showerror("Registration Failed", "Initial balance must be a number.")
            return

        if not username or not password or not full_name:
            messagebox.showerror("Registration Failed", "Full name, username and password cannot be empty.")
            return

        ok, msg = self.validate_password(password)
        if not ok:
            messagebox.showerror("Registration Failed", msg)
            return

        # check uniqueness: try to load existing file (use consistent underscore template)
        check = Data(username=username, encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")
        exists = check.pull_data(username)
        if exists:
            messagebox.showerror("Registration Failed", "That username already exists. Pick another.")
            return

        # generate simple account number
        import random
        account_number = str(random.randint(10**7, 10**8 - 1))
        # use time module to produce date string
        date_opened = time.strftime("%Y-%m-%d", time.localtime())

        d = Data(username=username, password=password, balance=initial_balance,
                 encrypt_manager=self.manager, filename_template="encrypted_{username}.txt",
                 full_name=full_name, account_number=account_number, date_opened=date_opened)

        d.transaction_history.append(f"Account created at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

        ok = d.save_data()
        if ok:
            messagebox.showinfo("Registration Successful", f"{username} has been created\nAccount #: {account_number}")
            self.back_main()
        else:
            messagebox.showerror("Registration Failed", "Could not create account.")

    def save_check(self):
        """Show account chooser (saving/checking) after login. Show account info and change-password."""
        # clear previous widgets
        self.clear_frames()
        self.choosing_frame = tk.Frame(self.main_win, width=360, height=240, bg="#fde6a3")
        self.choosing_frame.pack(padx=6, pady=6)

        # remember this as the current page so other views can hide it safely
        self.last_page = self.choosing_frame

        # show account number and date
        if hasattr(self, "current_data"):
            acct_no = self.current_data.account_number or ""
            opened = self.current_data.date_opened or ""
            full = self.current_data.full_name or ""
        else:
            acct_no = opened = full = ""

        tk.Label(self.choosing_frame, text=f"Account: {acct_no}", font=("Arial", 12), bg="#fde6a3").pack()
        tk.Label(self.choosing_frame, text=f"Name: {full}", font=("Arial", 10), bg="#fde6a3").pack()
        tk.Label(self.choosing_frame, text=f"Opened: {opened}", font=("Arial", 10), bg="#fde6a3").pack()

        self.time = tk.Label(self.choosing_frame, text=self.time_date, font=("Arial", 12), bg='#fde6a3')
        self.time.pack(pady=4)

        # select account type (checking / saving)
        self.saving = tk.Button(self.choosing_frame, text="Saving account", command=self.saving_account, bg='#fde6a3')
        self.saving.pack(fill='x')
        self.checking = tk.Button(self.choosing_frame, text="Checking account", command=self.checking_account, bg='#fde6a3')
        self.checking.pack(fill='x')

        # change password button
        self.change_pw_btn = tk.Button(self.choosing_frame, text="Change password", command=self.change_password_ui, bg='#fde6a3')
        self.change_pw_btn.pack(fill='x', pady=4)

        self.quit = tk.Button(self.choosing_frame, text="Exit program", command=self.quiting, bg='#fde6a3')
        self.quit.pack(side="left", padx=6, pady=6)

        # Log out button
        self.logout_button = tk.Button(self.choosing_frame, text="Log out", command=self.logout, bg='#fde6a3')
        self.logout_button.pack(side="right", padx=6, pady=6)

    def change_password_ui(self):
        """Prompt for old and new password and update account if correct."""
        self.clear_frames()
        self.pw_frame = tk.Frame(self.main_win, bg="#fde6a3")
        self.pw_frame.pack(padx=6, pady=6)

        tk.Label(self.pw_frame, text="Change Password", font=("Arial", 14), bg="#fde6a3").pack(pady=4)

        row_old = tk.Frame(self.pw_frame, bg="#fde6a3"); row_old.pack(pady=2)
        tk.Label(row_old, text="Current password:", bg="#fde6a3").pack(side="left")
        self.enter_old_pw = tk.Entry(row_old, show='*', width=25); self.enter_old_pw.pack(side="right")

        row_new = tk.Frame(self.pw_frame, bg="#fde6a3"); row_new.pack(pady=2)
        tk.Label(row_new, text="New password:", bg="#fde6a3").pack(side="left")
        self.enter_new_pw = tk.Entry(row_new, show='*', width=25); self.enter_new_pw.pack(side="right")

        tk.Button(self.pw_frame, text="Apply", command=self.change_password_apply, bg='#fde6a3').pack(pady=6)
        tk.Button(self.pw_frame, text="Back to accounts", command=self.save_check, bg='#fde6a3').pack()

    def change_password_apply(self):
        old = getattr(self, "enter_old_pw", tk.Entry()).get().strip()
        new = getattr(self, "enter_new_pw", tk.Entry()).get().strip()
        if not hasattr(self, "current_data"):
            messagebox.showerror("Error", "No account loaded.")
            return
        if old != self.current_data.password:
            messagebox.showerror("Failed", "Current password incorrect.")
            return
        ok, msg = self.validate_password(new)
        if not ok:
            messagebox.showerror("Failed", msg)
            return
        self.current_data.change_password(new)
        messagebox.showinfo("Success", "Password changed.")
        self.save_check()

    def saving_account(self, balance=None):
        """Show saving account view. Display accrued interest and provide transfer."""
        if not hasattr(self, "current_data"):
            messagebox.showerror("Error", "No account loaded.")
            return
        # compute balances and interest
        interest = self.current_data.compute_savings_interest()
        total = self.current_data.get_savings_balance()

        # clear chooser and show
        try:
            self.choosing_frame.pack_forget()
        except Exception:
            pass

        self.saving_frame = tk.Frame(self.main_win, width=360, height=240, bg="#fde6a3")
        self.saving_frame.pack(padx=6, pady=6)

        tk.Label(self.saving_frame, text=f"Saving Account - {self.current_data.full_name}", bg="#fde6a3").pack()
        tk.Label(self.saving_frame, text=f"Balance: {self.current_data.balance:.2f}", bg="#fde6a3").pack()
        tk.Label(self.saving_frame, text=f"Interest earned since opened: {interest:.4f}", bg="#fde6a3").pack()
        tk.Label(self.saving_frame, text=f"Total if interest applied: {total:.2f}", bg="#fde6a3").pack()

        # transfer and back buttons
        tk.Button(self.saving_frame, text="Transfer funds", command=self.transfering, bg="#fde6a3").pack(pady=4)
        tk.Button(self.saving_frame, text="Back to accounts", command=self.save_check, bg="#fde6a3").pack()

    def checking_account(self, balance=None):
        # hide only the previous page instead of destroying all widget attributes
        try:
            if getattr(self, "last_page", None) is not None:
                try:
                    self.last_page.pack_forget()
                except Exception:
                    pass
        except Exception:
            pass

        if balance is None and hasattr(self, "current_data"):
            balance = self.current_data.balance

        if hasattr(self, "current_data") and getattr(self, "current_data") is not None:
            username_display = self.current_data.full_name or self.current_data.username
        else:
            try:
                username_display = self.enter_username.get()
            except Exception:
                username_display = ""

        # main checking frame
        self.checking_frame = tk.Frame(self.main_win, width=360, height=240, bg="#fde6a3")
        self.checking_frame.pack(padx=6, pady=6, fill='both', expand=True)

        # remember this page as last_page so future views can hide it
        self.last_page = self.checking_frame

        # info and controls
        self.show_check_info = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.show_check_info.pack(fill='x', pady=4)

        self.chec_choose = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.chec_choose.pack(fill='x', pady=4)

        self.quit_and_leave = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.quit_and_leave.pack(fill='x', pady=4)

        # clear text using f-string for safety
        self.c_balance_label = tk.Label(self.show_check_info, text=f"Hello {username_display}!! Your balance is: {balance:.2f}", bg="#fde6a3")
        self.c_balance_label.pack()

        self.c_asking = tk.Label(self.chec_choose, text="Would you like to......", bg="#fde6a3")
        self.c_asking.pack()

        # make buttons visible by using fill and padding
        self.withdraw_money = tk.Button(self.chec_choose, text="Withdraw money", command=self.withdraw, bg="#fde6a3")
        self.withdraw_money.pack(fill='x', pady=2)

        self.deposit_money = tk.Button(self.chec_choose, text="Deposit money", command=self.deposit, bg="#fde6a3")
        self.deposit_money.pack(fill='x', pady=2)

        # navigation / exit buttons
        self.quit = tk.Button(self.quit_and_leave, text="Quit the program", command=self.quiting, bg="#fde6a3")
        self.quit.pack(side="left", padx=6)

        self.back_to_main = tk.Button(self.quit_and_leave, text="Back to home page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack(side="right", padx=6)

        self.back_to_accounts = tk.Button(self.quit_and_leave, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.back_to_accounts.pack(side="right", padx=6)

    def back_main(self):
        """Return to main home page from a subpage."""
        if self.last_page is not None:
            self.last_page.pack_forget()
        self.last_page = None
        self.home_page()

    def logout(self):
        """Log out current user, clear session and return to home page."""
        if hasattr(self, "current_data"):
            try:
                del self.current_data
            except Exception:
                self.current_data = None

        messagebox.showinfo("Logged out", "You have been logged out.")
        try:
            self.clear_frames()
        except Exception:
            pass
        self.home_page()

    def quiting(self):
        """Close the application window and quit mainloop."""
        self.main_win.quit()
        self.main_win.destroy()
        
    def transfering(self):
        """Build transfer funds UI (target account, amount, password entry).
        Destroy any existing page/frame first to avoid leftover widgets.
        """
        # destroy known frames / last page before creating transfer UI
        for name in ("transfer_frame", "last_page", "choosing_frame", "saving_frame",
                     "checking_frame", "withdraw_frame", "deposit_frame", "register_main", "big_frame"):
            if hasattr(self, name):
                try:
                    widget = getattr(self, name)
                    if hasattr(widget, "destroy"):
                        widget.destroy()
                except Exception:
                    pass
                try:
                    delattr(self, name)
                except Exception:
                    try:
                        setattr(self, name, None)
                    except Exception:
                        pass

        # create transfer UI
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

        self.confirm_transfer = tk.Button(self.transfer_frame, text="Confirm Transfer", command=self.start_transfer, bg='#fde6a3')
        self.confirm_transfer.pack()

        self.transfer_back = tk.Button(self.transfer_frame, text="Back to accounts", command=self.save_check, bg='#fde6a3')
        self.transfer_back.pack()

        self.last_page = self.transfer_frame

    def start_transfer(self):
        """Validate transfer inputs and perform transfer between accounts."""
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

        if entered_pw != self.current_data.password:
            messagebox.showerror("Transfer Failed", "Incorrect password for current account.")
            return

        if amount > self.current_data.balance:
            messagebox.showerror("Transfer Failed", "Insufficient funds.")
            return

        # use underscore filename template for target
        target = Data(username=target_username, encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")
        ok = target.pull_data(target_username)
        if not ok:
            messagebox.showerror("Transfer Failed", "Target account not found.")
            return

        note = f"Transfer to {target_username} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        ok1 = self.current_data.transfer(target_username, amount, note=note)
        if not ok1:
            messagebox.showerror("Transfer Failed", "Could not withdraw from current account.")
            return

        note_target = f"Received from {self.current_data.username} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        ok2 = target.deposit(amount, note=note_target)
        if not ok2:
            # rollback
            self.current_data.deposit(amount, note=f"Rollback of failed transfer to {target_username}")
            messagebox.showerror("Transfer Failed", "Could not credit target account. Transfer rolled back.")
            return

        messagebox.showinfo("Transfer Successful", f"Transferred {amount:.2f} to {target_username}.")

        try:
            self.transfer_frame.pack_forget()
        except Exception:
            pass
        self.checking_account(self.current_data.balance)
        
    def withdraw(self):
        """Show withdraw UI. Ensure controls are packed and visible."""
        try:
            if getattr(self, "last_page", None) is not None:
                try:
                    self.last_page.pack_forget()
                except Exception:
                    pass
        except Exception:
            pass

        self.withdraw_frame = tk.Frame(self.main_win, width=360, height=200, bg="#fde6a3")
        self.withdraw_frame.pack(padx=6, pady=6, fill='both', expand=True)

        self.withdraw_amount = tk.Frame(self.withdraw_frame, bg="#fde6a3")
        self.withdraw_amount.pack(fill='x', pady=4)

        self.confirm_withdraw = tk.Frame(self.withdraw_frame, bg="#fde6a3")
        self.confirm_withdraw.pack(fill='x', pady=4)

        self.withdraw_label = tk.Label(self.withdraw_amount, text="How much do you want to withdraw?", bg="#fde6a3")
        self.withdraw_label.pack(side="left", padx=4)

        self.withdraw_enter = tk.Entry(self.withdraw_amount, width=20)
        self.withdraw_enter.pack(side='right', padx=4)

        # Confirm and Back buttons packed so they are visible
        self.withdraw_confirm = tk.Button(self.confirm_withdraw, text="Confirm Withdraw", command=self.start_withdraw, bg="#fde6a3")
        self.withdraw_confirm.pack(fill='x', pady=4, padx=6)

        # changed: Back to accounts button (same as deposit page)
        self.withdraw_back = tk.Button(self.confirm_withdraw, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.withdraw_back.pack(fill='x', pady=2, padx=6)

        self.last_page = self.withdraw_frame

    def deposit(self):
        """Show deposit UI. Ensure controls are packed and visible."""
        try:
            if getattr(self, "last_page", None) is not None:
                try:
                    self.last_page.pack_forget()
                except Exception:
                    pass
        except Exception:
            pass

        self.deposit_frame = tk.Frame(self.main_win, width=360, height=200, bg="#fde6a3")
        self.deposit_frame.pack(padx=6, pady=6, fill='both', expand=True)

        self.deposit_amount = tk.Frame(self.deposit_frame, bg="#fde6a3")
        self.deposit_amount.pack(fill='x', pady=4)

        self.confirm_deposit = tk.Frame(self.deposit_frame, bg="#fde6a3")
        self.confirm_deposit.pack(fill='x', pady=4)

        self.deposit_label = tk.Label(self.deposit_amount, text="How much do you want to deposit?", bg="#fde6a3")
        self.deposit_label.pack(side="left", padx=4)

        self.deposit_enter = tk.Entry(self.deposit_amount, width=20)
        self.deposit_enter.pack(side='right', padx=4)

        self.deposit_confirm = tk.Button(self.confirm_deposit, text="Confirm Deposit", command=self.start_deposit, bg="#fde6a3")
        self.deposit_confirm.pack(fill='x', pady=4, padx=6)

        self.back_to_accounts = tk.Button(self.confirm_deposit, text="Back to accounts", command=self.save_check, bg="#fde6a3")
        self.back_to_accounts.pack(fill='x', pady=2, padx=6)

        self.last_page = self.deposit_frame

    # Ensure start handlers exist and persist changes
    def start_withdraw(self):
        amt = getattr(self, "withdraw_enter", tk.Entry()).get().strip()
        try:
            amount = float(amt)
        except Exception:
            messagebox.showerror("Invalid amount", "Please enter a valid number.")
            return
        if not hasattr(self, "current_data") or self.current_data is None:
            messagebox.showerror("Error", "No account loaded.")
            return
        ok = self.current_data.withdraw(amount, note=f"ATM withdraw at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if ok:
            messagebox.showinfo("Success", f"Withdrew {amount:.2f}")
        else:
            messagebox.showerror("Failed", "Insufficient funds or invalid amount.")
        try:
            self.withdraw_frame.pack_forget()
        except Exception:
            pass
        self.checking_account(self.current_data.balance)

    def start_deposit(self):
        amt = getattr(self, "deposit_enter", tk.Entry()).get().strip()
        try:
            amount = float(amt)
        except Exception:
            messagebox.showerror("Invalid amount", "Please enter a valid number.")
            return
        if not hasattr(self, "current_data") or self.current_data is None:
            messagebox.showerror("Error", "No account loaded.")
            return
        ok = self.current_data.deposit(amount, note=f"ATM deposit at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if ok:
            messagebox.showinfo("Success", f"Deposited {amount:.2f}")
        else:
            messagebox.showerror("Failed", "Invalid amount.")
        try:
            self.deposit_frame.pack_forget()
        except Exception:
            pass
        self.checking_account(self.current_data.balance)

    def logging(self):
        """
        Robust login:
        - first check whether an encrypted payload exists for the entered username
        - if not found -> "Username not found"
        - if found but pull_data fails -> "Account data corrupt"
        - if password wrong -> "Incorrect password"
        - otherwise login successful
        """
        username = self.enter_username.get().strip() if hasattr(self, "enter_username") else ""
        password = self.enter_password.get().strip() if hasattr(self, "enter_password") else ""

        if not username or not password:
            messagebox.showerror("Login failed", "Username and password required.")
            return

        # use consistent underscore filename template when creating Data for login
        d = Data(username=username, encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")

        # quick check for existence/decryptability
        payload, fname = d.find_encrypted_payload(username)
        if not payload:
            messagebox.showerror("Login failed", "Username not found.")
            return

        # now try to fully load
        ok = d.pull_data(username)
        if not ok:
            messagebox.showerror("Login failed", "Account data corrupt.")
            return

        # check password
        if d.password != password:
            messagebox.showerror("Login failed", "Incorrect password.")
            return

        # success
        self.current_data = d
        self.show_account_home()

    def show_account_home(self):
        """
        Called after successful login. Hide any login/register frames and show the
        account chooser (save_check). Keeps the displayed username in the login
        entry in case other code uses it.
        """
        # safely hide known possible previous frames
        for name in ("big_frame", "register_main", "choosing_frame", "saving_frame",
                     "checking_frame", "withdraw_frame", "deposit_frame", "transfer_frame",
                     "pw_frame"):
            if hasattr(self, name):
                try:
                    getattr(self, name).pack_forget()
                except Exception:
                    pass

        # update username entry used elsewhere (keep displayed username)
        if hasattr(self, "current_data"):
            try:
                self.enter_username.delete(0, tk.END)
                self.enter_username.insert(0, self.current_data.username)
            except Exception:
                pass

        # show the account chooser
        self.save_check()
maain = Animation()