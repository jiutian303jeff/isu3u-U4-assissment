
import tkinter as tk
import time

class Gui:
    def __init__(self):
        self.main_win = tk.Tk()
        self.frame1 = tk.Frame(self.main_win).pack()
        self.frame2 = tk.Frame(self.main_win).pack()
        self.frame3 = tk.Frame(self.main_win).pack()
        self.frame4 = tk.Frame(self.main_win).pack()


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


        self.main_win.mainloop()

mian = Gui()
    