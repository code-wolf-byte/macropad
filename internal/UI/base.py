from tkinter import *

class BaseUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Macro Tools")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.mainloop()

    