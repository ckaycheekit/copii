import tkinter as tk
from database import Database


class Copii(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title('copii')
        # Width height
        self.master.geometry("600x700")
        # Set background color of copii
        self.master.configure(background='black')
        # Create widgets/grid
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.master, text="testing")
        label.pack()


if __name__ == '__main__':
    root = tk.Tk()
    copii = Copii(master=root)
    copii.mainloop()
