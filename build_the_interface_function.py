from tkinter import filedialog
from tkinter import *

root = Tk()
def open():
    file = filedialog.askopenfilename()
    return file
    
button_open = Button(text="open", command=open)
button_open.pack()


root.mainloop()