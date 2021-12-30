import tkinter as tk
from tkinter import messagebox
from scrollframe import ScrollFrame
from database import Database
from functools import partial
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, SPACING, PRI_BG_COLOR, PRI_FT_COLOR, SEC_BG_COLOR, SEC_FT_COLOR


db = Database()


class Login(tk.Frame):
    def __init__(self, copii, master):
        super().__init__(master)
        self.copii = copii
        self.master = master
        self.username_enter = tk.StringVar()
        self.passcode_enter = tk.StringVar()
        self.passcode_reenter = tk.StringVar()
        self.login_view()

    def login(self):
        pcode_frm_db = db.get_passcode(self.username)
        if self.passcode_enter.get() == pcode_frm_db:
            self.copii.navigation('landing')
            self.master.unbind("<Return>")
        else:
            self.passcode_enter.set("")
            messagebox.showerror("Copii", "Wrong password!")

    def signup(self):
        # Validate both username and passcode has been filled in
        if (self.username_enter.get() == '') or (self.passcode_enter.get() == ''):
            messagebox.showerror("Copii", "Please fill in username & passcode!")
        else:
            if self.passcode_enter.get() == self.passcode_reenter.get():
                db.insert_data('credentials', username=self.username_enter.get(), passcode=self.passcode_enter.get())
                self.copii.navigation('landing')
                self.username_enter.set("")
                self.passcode_enter.set("")
                self.passcode_reenter.set("")
                self.master.unbind('<Return>')
            else:
                messagebox.showerror("Copii", "Wrong passcode!")
                self.passcode_enter.set("")
                self.passcode_reenter.set("")


    def login_view(self):
        # temp drop table everytime for testing purpose
        # if db.check_table_exists('credentials'):
        #     db.drop_table('credentials')
        if db.check_table_exists('credentials'):
            # Exising user - show welcome message and passcode page
            self.username = db.get_username()
            welcome_msg = "Hello {}! Welcome back to Copii!".format(self.username)
            tk.Label(self.master, text=welcome_msg, bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/3, y=100)
            tk.Label(self.master, text='Passcode: ', bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING)
            tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.passcode_enter, show='*').place(x=WINDOW_WIDTH/3 + SPACING, y=100+SPACING)
            tk.Button(self.master, text='Submit', command=self.login).place(x=WINDOW_WIDTH/2,y=100+SPACING*2)
            self.master.bind("<Return>", (lambda event: self.login()))
        else:
            # Create table and user
            db.create_table("credentials")
            welcome_msg = "Hello! Welcome to Copii!"
            tk.Label(self.master, text=welcome_msg, bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/3, y=100)
            tk.Label(self.master, text="Create your user account", bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/3, y=100+SPACING)
            tk.Label(self.master, text="Username: ", bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING*2)
            tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.username_enter).place(x=WINDOW_WIDTH/2.5, y=100+SPACING*2)
            tk.Label(self.master, text="Passcode: ", bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING*3)
            tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.passcode_enter, show='*').place(x=WINDOW_WIDTH/2.5, y=100+SPACING*3)
            tk.Label(self.master, text='Re-enter passcode: ', bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/6, y=100+SPACING*4)
            tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.passcode_reenter, show='*').place(x=WINDOW_WIDTH/2.5, y=100+SPACING*4)
            tk.Button(self.master, text='Submit', command=self.signup).place(x=WINDOW_WIDTH/2, y=100+SPACING*5)
            self.master.bind("<Return>", (lambda event: self.signup()))


class Landing(tk.Frame):
    def __init__(self, copii, master):
        super().__init__(master)
        self.copii = copii
        self.master = master
        self.scrollFrame = ScrollFrame(self)
        self.landing_view()

    def copy_secret_to_clipboard(self, tag, secret):
        self.master.clipboard_clear()
        self.master.clipboard_append(secret)
        msg = "Secret for {} has been copied to clipboard!".format(tag)
        msg_widget = tk.Label(self.scrollFrame.canvas, text=msg, bg=PRI_BG_COLOR, fg=PRI_FT_COLOR)
        msg_widget.pack()
        msg_widget.after(2000, lambda: msg_widget.destroy())

    def delete_tag(self, tag):
        delete_confirmation = messagebox.askokcancel("Delete", "Are you sure to delete {} ?".format(tag))
        if delete_confirmation:
            db.delete_data(tag)
            self.copii.navigation('landing')

    def landing_view(self):
        navigate_to_insert = partial(self.copii.navigation, 'insert')
        tk.Button(self.scrollFrame.viewPort, text='Add record', command=navigate_to_insert, height=2).grid(row=0, column=0)
        tags_secrets_list = db.get_all_tags('secrets')
        # max to be 28, min to be 19 when len increases by 2 -> range decreases by 1
        # window_height_range = 19 if 28 - (len(tags_secrets_list)  // 2) < 19 else 28 - (len(tags_secrets_list)  // 2)
        for i in range(17):
            tk.Label(self.scrollFrame.viewPort, bg=PRI_BG_COLOR, height=2).grid(row=i+1, column=100)
        for i in range(len(tags_secrets_list)):
            tag = tags_secrets_list[i][0]
            sec = tags_secrets_list[i][1]
            copy_secret_to_clipboard = partial(self.copy_secret_to_clipboard, tag, sec)
            delete_tag = partial(self.delete_tag, tag)
            navigate_to_edit_tag = partial(self.copii.navigation, 'edit_tag', tag)
            tk.Button(self.scrollFrame.viewPort, text=tag, command=copy_secret_to_clipboard, width=30, height=2).grid(row=i+1, column=1)
            tk.Label(self.scrollFrame.viewPort, width=10, bg=PRI_BG_COLOR).grid(row=i+1, column=2)
            tk.Button(self.scrollFrame.viewPort, text="Edit", command=navigate_to_edit_tag).grid(row=i+1, column=3)
            tk.Label(self.scrollFrame.viewPort, width=1, bg=PRI_BG_COLOR).grid(row=i+1, column=4)
            tk.Button(self.scrollFrame.viewPort, text="Delete", command=delete_tag).grid(row=i+1, column=5)
        self.scrollFrame.pack(side="top", fill="both", expand=True)


class EditTagName(tk.Frame):
    def __init__(self, copii, master, tag_to_edit):
        super().__init__(master)
        self.copii = copii
        self.master = master
        self.tag_to_edit = tag_to_edit
        self.new_tag_name = tk.StringVar()
        self.edit_view()

    def edit_tag(self):
        db.update_data('secrets', new_tag=self.new_tag_name.get(), tag=self.tag_to_edit)
        self.copii.navigation('landing')

    def edit_view(self):
        navigate_to_landing = partial(self.copii.navigation, 'landing')
        tk.Label(self.master, text=self.tag_to_edit, bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/3, y=100)
        tk.Label(self.master, text="Enter new tag name: ", bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING)
        tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.new_tag_name).place(x=WINDOW_WIDTH/2, y=100+SPACING)
        tk.Button(self.master, text='Submit', command=self.edit_tag).place(x=WINDOW_WIDTH/2, y=100+SPACING*2)
        tk.Button(self.master, text='Cancel', command=navigate_to_landing).place(x=WINDOW_WIDTH/1.65, y=100+SPACING*2)

class InsertRecord(tk.Frame):
    def __init__(self, copii, master):
        super().__init__(master)
        self.copii = copii
        self.master = master
        self.new_tag = tk.StringVar()
        self.new_secret = tk.StringVar()
        self.secret_reenter = tk.StringVar()
        self.insert_view()

    def insert(self):
        if (self.new_tag.get() == '') or (self.new_secret.get() == ''):
            messagebox.showerror("Copii", "Please fill in tag & secret!")
        else:
            if self.new_secret.get() == self.secret_reenter.get():
                db.insert_data('secrets', tag=self.new_tag.get(), secret=self.new_secret.get())
                self.copii.navigation('landing')
                self.new_tag.set("")
                self.new_secret.set("")
                self.secret_reenter.set("")
            else:
                messagebox.showerror("Copii", "Secrets not matched!")

    def insert_view(self):
        navigate_to_landing = partial(self.copii.navigation, 'landing')
        tk.Label(self.master, text='Add a new record: ', bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING)
        tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.new_tag).place(x=WINDOW_WIDTH/2, y=100+SPACING)
        tk.Label(self.master, text="Secret: ", bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING*2)
        tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.new_secret, show='*').place(x=WINDOW_WIDTH/2, y=100+SPACING*2)
        tk.Label(self.master, text='Re-enter secret: ', bg=PRI_BG_COLOR, fg=PRI_FT_COLOR).place(x=WINDOW_WIDTH/4, y=100+SPACING*3)
        tk.Entry(self.master, bg=SEC_BG_COLOR, fg=SEC_FT_COLOR, textvariable=self.secret_reenter, show='*').place(x=WINDOW_WIDTH/2, y=100+SPACING*3)
        tk.Button(self.master, text='Submit', command=self.insert).place(x=WINDOW_WIDTH/2, y=100+SPACING*4)
        tk.Button(self.master, text='Cancel', command=navigate_to_landing).place(x=WINDOW_WIDTH/1.68, y=100+SPACING*4)


class Copii(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title('copii')
        # Width height
        self.master.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
        # Set background color of copii
        self.master.configure(background=PRI_BG_COLOR)
        # Disable window resizability for scrolling to work properly
        self.master.resizable(False, False)
        self.navigation('login')

    def call_login(self):
        login = Login(self, self.master)

    def call_landing(self):
        Landing(self, self.master).pack(side="top", fill="both", expand=True)

    def call_insert(self):
        insert = InsertRecord(self, self.master)

    def call_edit_tag(self, tag_to_edit):
        et = EditTagName(self, self.master, tag_to_edit)

    def navigation(self, to_page, tag_to_edit=None):
        for widget in self.master.winfo_children():
            widget.destroy()
        if to_page == 'login':
            self.call_login()
        elif to_page == 'landing':
            self.call_landing()
        elif to_page == 'insert':
            self.call_insert()
        elif to_page == 'edit_tag':
            self.call_edit_tag(tag_to_edit)


root = tk.Tk()
copii = Copii(master=root)
try:
    copii.mainloop()
finally:
    db.close_connection()
