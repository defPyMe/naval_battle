
from tkinter import *


def log_in_function():
    pass



def build_first_screen():  
    root=Tk()
    root.geometry("200x200")
    root.resizable(False, False)
    label = Label(text = "", width=3, height=3)
    label1 = Label(text = "insert username")
    label_space = Label(text = "", width=1, height=1)
    label_space1 = Label(text = "", width=1, height=1)
    text_box = Text(height=1,width=10)
    button_log = Button(text = "log in", command = log_in_function)
    label.pack()
    label1.pack()
    label_space.pack()
    text_box.pack()
    label_space1.pack()
    button_log.pack()
    root.mainloop()


