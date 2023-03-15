from tkinter import filedialog
from tkinter import *

root = Tk()
root.title("ddddd")

def open():
    file = filedialog.askopenfilename()
    return file
def opentop():
    f = Toplevel()
    g = f.title(root.title())
    return g

button = Button(text="open", command=opentop)

button_open = Button(text="open", command=open)
button_open.pack()
button.pack()


root.mainloop()