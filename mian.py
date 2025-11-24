
import tkinter as tk
import time

class Gui:
    def __init__(self):
        self.main_win = tk.Tk()
        self.frame1 = tk.Frame(self.main_win)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.main_win)
        self.frame2.pack()
        self.frame3 = tk.Frame(self.main_win)
        self.frame3.pack()
        self.frame4 = tk.Frame(self.main_win)
        self.frame4.pack()


        self.label_welcome = tk.Label(self.frame1, text="Welcome", font=("Arial",20))
        self.label_welcome.pack(expand=True)


        self.label_username = tk.Label(self.frame2, text="username:  ")
        self.label_username.pack(side="left")

        self.enter_username = tk.Entry(self.frame2, width=20)
        self.enter_username.pack(side="right")


        self.label_password = tk.Label(self.frame3, text="password:  ")
        self.label_password.pack(side="left")

        self.enter_password = tk.Entry(self.frame3, width=20)
        self.enter_password.pack(side="right")

        #calling another function and page for login
        self.login = tk.Button(self.frame4, text="Login", command=self.logging)
        self.login.pack()
        
        #calling another function and page for creating new account
        self.create_account = tk.Button(self.frame4, text="Create an account", command=self.create)



    def logging(self):
        pass
    def create(self):
        pass


        self.main_win.mainloop()

mian = Gui()
    