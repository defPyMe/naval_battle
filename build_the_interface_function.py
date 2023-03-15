from tkinter import filedialog
from tkinter import *

root = Tk()
root.title("ddddd")

def open(button):
    button["state"]=DISABLED


def opentop():
    f = Toplevel()
    g = f.title(root.title())
    return g

button = Button(text="open", command=opentop)

button_open = Button(text="open butt", command=lambda: open(button))

button_open.pack()
button.pack()


root.mainloop()