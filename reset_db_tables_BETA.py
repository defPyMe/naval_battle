import tkinter as tk
from tkinter import ttk
from tkinter import *
root = tk.Tk()
frame1 = ttk.Frame(root)
container = ttk.Frame(frame1)#frame_buttons
canvas = tk.Canvas(container)#canvas = canvas
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)


frame1.pack()
container.pack()#--
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()



root.mainloop()



"""
#--------------------------------------------------------------------------------------------------
frame_buttons_2 = Frame(base_window)
frame_buttons_2.grid(row=0, column=1, padx=10, pady=10)
#frame above to differentiate the page
#inside a new frame that i s the container
frame_buttons = Frame(frame_buttons_2)
#adding some propertiees 
#.grddddid(row=0,column=0)+
#canvas created and added to frame
canvas=Canvas(frame_buttons,bg='#FFFFFF',width=350,height=300,scrollregion=(0,0,500,500))
bar=Scrollbar(frame_buttons,orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas)
scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
            )
canvas.config(width=200,height=200)
canvas.config(yscrollcommand=bar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
    
    
    
bar.config(command=canvas.yview)                    
bar.pack(side=RIGHT,fill=Y)


frame_buttons_1 = Frame(base_window, padx = 10,width=350,height=300)
canvas.create_window(0, 0, anchor='nw', window=frame_buttons_1)
#creating a new frame here to position teh text and button
frame_buttons_4 = Frame(frame_buttons_2)
#positions it underneath
frame_buttons_4.pack()
frame_buttons.pack(expand=True, fill=BOTH)
text_message = Text(frame_buttons_4, width=20, height = 1)

send_message = Button(frame_buttons_4, text="send", command = lambda : send_message_funct(text_message, id_of_battle, id_player))

text_message.grid(row = 0, column=0, padx=6)
send_message.grid(row = 0, column=1)
print("in creating the chat the first time", id_of_battle)"""



