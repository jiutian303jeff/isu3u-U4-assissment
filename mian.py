
import tkinter as tk
import time
import encrypt

class Base_page():
    def __init__(self):
        self.main_win = tk.Tk()
        self.big_frame = tk.Frame(self.main_win)
        self.big_frame.pack()

        #creating 4 frames to put labels, buttons and entries. 4 frames put in one big frame
        self.frame1 = tk.Frame(self.big_frame)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.big_frame)
        self.frame2.pack()
        self.frame3 = tk.Frame(self.big_frame)
        self.frame3.pack()
        self.frame4 = tk.Frame(self.big_frame)
        self.frame4.pack()


        #a welcome label
        self.label_welcome = tk.Label(self.frame1, text="Welcome", font=("Arial",20))
        self.label_welcome.pack(expand=True)


        #Lable to guide user entering a user name
        self.label_username = tk.Label(self.frame2, text="username:  ")
        self.label_username.pack(side="left")
        #Entry to input username
        self.enter_username = tk.Entry(self.frame2, width=20)
        self.enter_username.pack(side="right")


        #Label to guide user entering a password
        self.label_password = tk.Label(self.frame3, text="password:  ")
        self.label_password.pack(side="left")
        #Entry to input password
        self.enter_password = tk.Entry(self.frame3, width=20)
        self.enter_password.pack(side="right")

        #calling another function and page for login
        self.login = tk.Button(self.frame4, text="Login", command=self.logging)
        self.login.pack()
        
        #calling another function and page for creating new account
        self.create_account = tk.Button(self.frame4, text="Register", command=self.register)
        self.create_account.pack()


        self.main_win.mainloop()

    def register(self):
        #remove the last page and creating a new frame for register page
        self.big_frame.pack_forget()
        self.register_main = tk.Frame(self.main_win)
        self.register_main.pack()


        #a label that indicate here to register
        self.label_indicate = tk.Label(self.register_main, text="Here to register", font=("Arial",20))
        self.label_indicate.pack(expand=True)
        
        #first frame for username entering
        self.register_frame1 = tk.Frame(self.main_win)
        self.register_frame1.pack()

        #second frame for password entering
        self.register_frame2 = tk.Frame(self.main_win)
        self.register_frame2.pack()


        #label indicating here to register new username
        self.creating_username = tk.Label(self.register_frame1, text="Enter a username:  ")
        self.creating_username.pack(side="left")
        #entering new username
        self.enter_username = tk.Entry(self.register_frame1, width=20)
        self.enter_username.pack(side="right")

        #Label indicating here to register new password
        self.creating_password = tk.Label(self.register_frame2, text="Enter a password:  ")
        self.creating_password.pack(side="left")
        #entering new password
        self.enter_password = tk.Entry(self.register_frame2, width=20)
        self.enter_password.pack(side="right")

        #click to save the data
        self.register_button = tk.Button(self.register_main, text="Register a new account", command=self.save_account)



    def logging(self):
        pass

    def saving_account(self):
        pass

    def checking_account(self):
        pass
    
class Data :
    def __init__(self):
        self.username = ""
        self.password = ""
        self.balance = 0
        self.transaction_history = []

    def save_data(self):
        pass

    def balance(self):
        pass

    def trans_history(self):
        pass

    def error_handle(self):
        pass


    

mian = Base_page()
    