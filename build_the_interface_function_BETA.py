from tkinter import *

root = Tk()
def retrieve(text):
    print(text.get())

tex = Entry(root)
b = Button(root, text="click", command = lambda : retrieve(tex))


root.bind("<Return>", retrieve(tex))





tex.pack()
b.pack()


root.mainloop()