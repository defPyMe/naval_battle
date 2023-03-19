from tkinter import filedialog
from tkinter import *

root = Tk()
frame = Frame(root)
def check_color(frame):
    colored = [i for i in frame.grid_slaves() if i["bg"]=="red"]
    print(len(colored))
    return colored
for i in range(10):
    for j in range(10):
        button = Button(frame, text=str(i)+ "," +str(j), command=lambda: check_color(frame), bg="red")
        button.grid(row=i, column=j)
        
frame.grid(row=0, column=0)





root.mainloop()
