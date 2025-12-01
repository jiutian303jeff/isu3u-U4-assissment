"""

"""

from data import Data
import tkinter as tk
import time

class Animation:
    def __init__(self, manager=None):
        # ONE root window only
        self.root = tk.Tk()
        self.root.title("Splash Screen")
        self.stop_animation = True

        self.manager = manager

        # Show splash
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
        self.label = tk.Label(self.splash_frame, text="Loading......",bg="#fde6a3")
        self.label.pack()

        self.animate_frames()
        self.root.after(5000, self.open_main)

    def animate_frames(self):
        if not self.stop_animation:
            return
        
        self.splash_label.config(image=self.frames[self.frame_index])

        self.frame_index = (self.frame_index + 1) % len(self.frames)

        self.root.after(120, self.animate_frames)

    def open_main(self):
        self.stop_animation = False
        self.splash_frame.destroy()
        Base_page(self.root)

class Base_page(Animation):
    def __init__(self,root):
        self.main_win = root
        self.main_win.config(bg="#fde6a3")
        self.last_page = None
        current_time_struct = time.localtime()
        self.time_date = time.strftime("%Y-%m-%d", current_time_struct)
        self.time_time = time.strftime("%y-%m-%d, %H:%M:%S", current_time_struct)
        self.home_page()

    def home_page(self):
        self.big_frame = tk.Frame(self.main_win,width=300, height=200, bg="#fde6a3")
        self.big_frame.pack()

        #creating 4 frames to put labels, buttons and entries. 4 frames put in one big frame
        self.frame1 = tk.Frame(self.big_frame,bg="#fde6a3")
        self.frame1.pack()
        self.frame2 = tk.Frame(self.big_frame,bg="#fde6a3")
        self.frame2.pack()
        self.frame3 = tk.Frame(self.big_frame,bg="#fde6a3")
        self.frame3.pack()
        self.frame4 = tk.Frame(self.big_frame, bg="#fde6a3")
        self.frame4.pack()


        #a welcome label
        self.label_welcome = tk.Label(self.frame1, text="Welcome", font=("Arial",20), bg="#fde6a3")
        self.label_welcome.pack(expand=True)


        #Lable to guide user entering a user name
        self.label_username = tk.Label(self.frame2, text="username:  ",bg="#fde6a3")
        self.label_username.pack(side="left")
        #Entry to input username
        self.enter_username = tk.Entry(self.frame2, width=20)
        self.enter_username.pack(side="right")


        #Label to guide user entering a password
        self.label_password = tk.Label(self.frame3, text="password:  ", bg="#fde6a3")
        self.label_password.pack(side="left")
        #Entry to input password
        self.enter_password = tk.Entry(self.frame3, width=20)
        self.enter_password.pack(side="right")

        #calling another function and page for login
        self.login = tk.Button(self.frame4, text="Login", command=self.logging, bg="#fde6a3")
        self.login.pack(side="left")
        
        #calling another function and page for creating new account
        self.create_account = tk.Button(self.frame4, text="Register", command=self.register, bg="#fde6a3")
        self.create_account.pack(side="right")


        self.main_win.mainloop()

    def register(self):
        #remove the last page and creating a new frame for register page
        self.big_frame.pack_forget()
        self.register_main = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.register_main.pack()

        self.last_page = self.register_main

        #a label that indicate here to register
        self.label_indicate = tk.Label(self.register_main, text="Here to register", font=("Arial",20),bg="#fde6a3")
        self.label_indicate.pack(expand=True)
        
        #first frame for username entering
        self.register_frame1 = tk.Frame(self.register_main, bg='#fde6a3')
        self.register_frame1.pack()

        #second frame for password entering
        self.register_frame2 = tk.Frame(self.register_main,bg="#fde6a3")
        self.register_frame2.pack()


        #label indicating here to register new username
        self.creating_username = tk.Label(self.register_frame1, text="Enter a username:  ",bg="#fde6a3")
        self.creating_username.pack(side="left")
        #entering new username
        self.enter_username = tk.Entry(self.register_frame1, width=20)
        self.enter_username.pack(side="right")

        #Label indicating here to register new password
        self.creating_password = tk.Label(self.register_frame2, text="Enter a password:  ",bg='#fde6a3')
        self.creating_password.pack(side="left")
        #entering new password
        self.enter_password = tk.Entry(self.register_frame2, width=20)
        self.enter_password.pack(side="right")

        #click to save the data
        self.register_button = tk.Button(self.register_main, text="Register a new account", command=self.creating_account, bg='#fde6a3')
        self.register_button.pack()

        self.back_to_main = tk.Button(self.register_main, text="Back to main page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack()


    def logging(self):
        #some function taht checking if the user name and password exist and correct
        username = self.enter_username.get().strip()
        password = self.enter_password.get().strip()

        d = Data(username=username, encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")
        ok = d.pull_data(username)
        if not ok:
            tk.messagebox.showerror("login failed", "Username not found")
            return

        if d.password != password:
            tk.messagebox.showerror("login failed", "Incorrect password")
            return

        # successful login
        self.current_data = d
        self.show_account_home()

    def save_check(self):

        #remove last frame, creating a new frame that 
        self.big_frame.pack_forget()
        self.choosing_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.choosing_frame.pack()

        self.time = tk.Label(self.choosing_frame, text = self.time_date , font=("Arial",20 ), bg='#fde6a3')
        self.time.pack()
        self.saving = tk.Button(self.choosing_frame, text="Saving account", command=self.saving_account,bg='#fde6a3')
        self.saving.pack()
        self.checking = tk.Button(self.choosing_frame, text="checking account",command=self.checking_account,bg="#fde6a3")
        self.checking.pack()

        self.quit = tk.Button(self.choosing_frame, text="Quit", command=self.quiting, bg="#fde6a3")
        self.quit.pack()    



    def saving_account(self, balance=0):

        #remove last frame, creating a few new frames
        self.choosing_frame.pack_forget()
        self.saving_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.saving_frame.pack() 

        self.show_save_info = tk.Frame(self.saving_frame, bg="#fde6a3")
        self.show_save_info.pack()

        self.sav_choosing = tk.Frame(self.saving_frame, bg="#fde6a3")
        self.sav_choosing.pack()

        self.quit_leave = tk.Frame(self.saving_frame, bg="#fde6a3")
        self.quit_leave.pack()

        #setting this page as the "last page"
        self.last_page = self.saving_frame


        
        #showing balance and interest and transferring choice
        self.balance_label = tk.Label(self.show_save_info, text="Hello %s!! Your balance is: %d"%(self.enter_username.get(),balance), bg="#fde6a3")
        self.balance_label.pack()

        self.interest_label = tk.Label(self.show_save_info, text="your interest rate  is: 2.25%", bg="#fde6a3")
        self.interest_label.pack()

        self.asking = tk.Label(self.sav_choosing, text="Whould you like to......", bg="#fde6a3")
        self.asking.pack()

        self.transfer = tk.Button(self.sav_choosing, text="Transfer founds", command=self.transfering,bg="#fde6a3")
        self.transfer.pack()


        #showing the user to quit the program or back to main page
        self.quit = tk.Button(self.quit_leave, text="quit the program", command=self.quiting,bg="#fde6a3" )
        self.quit.pack(side="left")

        self.back_to_main = tk.Button(self.quit_leave, text="Back to home page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack(side="right")

    
    def checking_account(self,balance=0):
        self.choosing_frame.pack_forget()
        self.checking_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.checking_frame.pack()

        self.show_check_info = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.show_check_info.pack()

        self.chec_choose = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.chec_choose.pack()

        self.quit_and_leave = tk.Frame(self.checking_frame, bg="#fde6a3")
        self.quit_and_leave.pack()

        #setting this page as the "last page"
        self.last_page = self.checking_frame


        self.c_balance_label = tk.Label(self.show_check_info, text="Hello %s!! Your balance is: %d"%(self.enter_username.get(),balance), bg="#fde6a3")
        self.c_balance_label.pack()

        self.c_asking = tk.Label(self.chec_choose, text="Whould you like to......", bg="#fde6a3")
        self.c_asking.pack()

        self.withdraw_money = tk.Button(self.chec_choose, text="Withdraw money", command=self.withdraw,bg="#fde6a3")
        self.withdraw_money.pack()
        
        self.deposit_money = tk.Button(self.chec_choose, text="Deposit money", command=self.deposit,bg="#fde6a3")
        self.deposit_money.pack()


        self.quit = tk.Button(self.quit_and_leave, text="quit the program", command=self.quiting,bg="#fde6a3" )
        self.quit.pack(side="left")

        self.back_to_main = tk.Button(self.quit_and_leave, text="Back to home page", command=self.back_main, bg="#fde6a3")
        self.back_to_main.pack(side="right")

    
    def back_main(self):
        # destroy previous page if it exists
        if self.last_page is not None:
            self.last_page.pack_forget()
        self.last_page = None
        self.home_page()

    def quiting(self):
        self.main_win.quit()
        self.main_win.destroy()
        
    def transfering(self):
        pass
        
    def withdraw(self):
        self.checking_frame.pack_forget()
        self.withdraw_frame = tk.Frame(self.main_win, width=300, height=200, bg="#fde6a3")
        self.withdraw_frame.pack()

        self.withdraw_amount = tk.Frame(self.withdraw_frame, bg="#fde6a3")
        self.withdraw_amount.pack()

        self.confirm_withdraw = tk.Frame(self.withdraw_frame, bg="#fde6a3")
        self.confirm_withdraw.pack()



        self.withdraw_label = tk.Label(self.withdraw_amount, text="how much you want to with draw?",bg="#fde6a3")
        self.withdraw_label.pack(side="left")

        self.withdraw_enter = tk.Entry(self.withdraw_amount, width= 20)
        self.withdraw_enter.pack(side='right')


        self.withdraw_confirm = tk.Button(self.confirm_withdraw, text="Confirm Withdraw",command=self.start_withdraw,bg="#fde6a3")
        self.withdraw_confirm.pack()


    def deposit(self):
        self.checking_frame.pack_forget()
        self.deposit_frame = tk.Frame(self.main_win,width=300, height=200, bg="#fde6a3")
        self.deposit_frame.pack()

        self.deposit_amount = tk.Frame(self.deposit_frame, bg="#fde6a3")
        self.deposit_amount.pack()

        self.confirm_deposit = tk.Frame(self.deposit_frame, bg="#fde6a3")
        self.confirm_deposit.pack()



        self.deposit_label = tk.Label(self.deposit_amount, text="how much you want to deposit?",bg="#fde6a3")
        self.deposit_label.pack(side="left")

        self.deposit_enter = tk.Entry(self.deposit_amount, width= 20)
        self.deposit_enter.pack(side='right')


        self.deposit_confirm = tk.Button(self.confirm_deposit, text="Confirm Withdraw",command=self.start_deposit,bg="#fde6a3")
        self.deposit_confirm.pack()

    def ui_deposit(self):
        def do_deposit():
            amt = entry.get().strip()
            ok = self.current_data.deposit(amt, note="GUI deposit")
            if ok:
                tk.messagebox.showinfo("Success", f"Deposited ${amt}")
                # 更新顯示（刷新頁面或更新 label）
                top.destroy()
                self.show_account_home()
            else:
                tk.messagebox.showerror("failed", "Deposit failed (invalid amount)")

        top = tk.Toplevel(self.main_win)
        top.title("Deposit")
        entry = tk.Entry(top)
        entry.pack()
        btn = tk.Button(top, text="Confirm", command=do_deposit)
        btn.pack()


    def ui_transfer(self):
        def do_transfer():
            target = entry_target.get().strip()
            amt = entry_amt.get().strip()
            ok = self.current_data.transfer(target, amt, note="GUI transfer")
            if ok:
                tk.messagebox.showinfo("Success", f"Transferred ${amt} to {target}")
                top.destroy()
                self.show_account_home()
            else:
                tk.messagebox.showerror("Failed", "Transfer failed (insufficient balance or account does not exist)")

        top = tk.Toplevel(self.main_win)
        top.title("Transfer")
        entry_target = tk.Entry(top)
        entry_target.pack()
        entry_amt = tk.Entry(top)
        entry_amt.pack()
        btn = tk.Button(top, text="Confirm", command=do_transfer)
        btn.pack()


    
    def creating_account(self):
        username = self.enter_username.get().strip()
        password = self.enter_password.get().strip()
        # the initial balance is set to 0
        initial_balance = 0

        d = Data(username=username, password=password, balance=initial_balance,
                encrypt_manager=self.manager, filename_template="encrypted_{username}.txt")

        # Add a record for account creation
        d.transaction_history.append(f"Account created at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

        ok = d.save_data()
        if ok:
            try:
                saver = getattr(self.manager, "save_keys", None)
                if callable(saver):
                    saver("multi_accounts_keys.txt")
            except:
                pass
            tk.messagebox.showinfo("Registration Successful", f"{username} has been created")
            self.back_main()
        else:
            tk.messagebox.showerror
    

    def start_withdraw(self):


        #add the withdraw proccess function here, bro

        self.withdraw_confirm.pack_forget()

        self.last_page = self.withdraw_frame

        self.withdraw_success = tk.Label(self.confirm_withdraw, text="Withdraw Success!", bg="#fde6a3")
        self.withdraw_success.pack()

        self.back_to_main = tk.Button(self.confirm_withdraw, text="Back to main page",bg="#fde6a3",command=self.back_main)
        self.back_to_main.pack()

    def start_deposit(self):
        #add the deposit proccess function here, bro

        self.deposit_confirm.pack_forget()

        self.last_page = self.deposit_frame

        self.deposit_success = tk.Label(self.confirm_deposit, text="Deposit Success!", bg="#fde6a3")
        self.deposit_success.pack()

        self.back_to_main = tk.Button(self.confirm_deposit, text="Back to main page",bg="#fde6a3",command=self.back_main)
        self.back_to_main.pack()


    



main = Animation()

    
