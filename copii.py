import tkinter as tk
from database import Database


# Global variables
PRI_BG_COLOR = 'black'
SEC_BG_COLOR = 'white'
PRI_FT_COLOR = 'white'
SEC_FT_COLOR = 'black'

db = Database()

class Landing(tk.Frame):
    def __init__(self, copii, master):
        super().__init__(master)
        self.copii = copii
        self.master = master
        self.passcode_enter = tk.StringVar()
        self.login_view()

    def login(self):
        pcode_frm_db = db.get_passcode(self.username)
        if self.passcode_enter.get() == pcode_frm_db:
            self.copii.navigation('insert')
        self.master.unbind("<Return>")

    def login_view(self):
        if db.check_table_exists('credentials'):
            # Exising user - show welcome message and passcode page
            self.username = db.get_username()
            welcome_msg = "Hello {}! Welcome back to Copii!".format(self.username)
            tk.Label(self.master, text=welcome_msg, bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).pack()
            tk.Label(self.master, text='Passcode: ', bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).pack()
            tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.passcode_enter, show='*').pack()
            tk.Button(self.master, text='Submit', command=self.login).pack()
            self.master.bind("<Return>", (lambda event: self.login()))


class InsertRecord(tk.Frame):
    def __init__(self, copii, master):
        super().__init__(master)
        self.copii = copii
        self.master = master
        self.insert()

    def insert(self):
        label = tk.Label(self.master, text='tis is insert')
        label.pack()


class Copii(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title('copii')
        # Width height
        self.master.geometry("600x700")
        # Set background color of copii
        self.master.configure(background=PRI_BG_COLOR)
        self.navigation('landing')

    def call_landing(self):
        landing = Landing(self, self.master)

    def call_insert(self):
        insert = InsertRecord(self, self.master)

    def navigation(self, to_page):
        for widget in self.master.winfo_children():
            widget.destroy()
        if to_page == 'landing':
            self.call_landing()
        elif to_page == 'insert':
            self.call_insert()


if __name__ == '__main__':
    # Start running app
    root = tk.Tk()
    copii = Copii(master=root)
    copii.mainloop()
