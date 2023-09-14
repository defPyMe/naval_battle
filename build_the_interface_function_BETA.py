"""from tkinter import *
  
class ScrollBar:
     
    # constructor
    def __init__(self):
         
        # create root window
        root = Tk()
  
        # create a horizontal scrollbar by
        # setting orient to horizontal
        h = Scrollbar(root, orient = 'horizontal')
  
        # attach Scrollbar to root window at
        # the bootom
        h.pack(side = BOTTOM, fill = X)
  
        # create a vertical scrollbar-no need
        # to write orient as it is by
        # default vertical
        v = Scrollbar(root)
  
        # attach Scrollbar to root window on
        # the side
        v.pack(side = RIGHT, fill = Y)
          
  
        # create a Text widget with 15 chars
        # width and 15 lines height
        # here xscrollcomannd is used to attach Text
        # widget to the horizontal scrollbar
        # here yscrollcomannd is used to attach Text
        # widget to the vertical scrollbar
        t = Text(root, width = 15, height = 15, wrap = NONE,
                 xscrollcommand = h.set,
                 yscrollcommand = v.set)
  
        # insert some text into the text widget
        for i in range(20):
            t.insert(END,"this is some text\n")
  
        # attach Text widget to root window at top
        t.pack(side=TOP, fill=X)
  
        # here command represents the method to
        # be executed xview is executed on
        # object 't' Here t may represent any
        # widget
        h.config(command=t.xview)
  
        # here command represents the method to
        # be executed yview is executed on
        # object 't' Here t may represent any
        # widget
        v.config(command=t.yview)
  
        # the root window handles the mouse
        # click event
        root.mainloop()
 
# create an object to Scrollbar class
s = ScrollBar()"""

"""

from tkinter import *
root=Tk()
frame=Frame(root,width=300,height=300)
frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

root.mainloop()"""
from tkinter import *

root=Tk()
frame=Frame(root,width=50,height=300)
frame.pack(expand=True, fill=BOTH)
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,50,500))

bar=Scrollbar(frame,orient=VERTICAL)
bar.pack(side=RIGHT,fill=Y)
bar.config(command=canvas.yview)

canvas.config(width=50,height=300)
canvas.config(yscrollcommand=bar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

frame = Frame(root)
for _ in range(10):
    Button(frame, text=str(_)).grid(row=_)

canvas.create_window(0, 0, anchor='nw', window=frame)

root.mainloop()