from tkinter import *
from tkinter import messagebox
from user_page_module import build_user_page
from sql_queries_ import checking_credentials


def logging_in(text_box):
    #need to add a connection to the list of users here 
    name_input = str(text_box.get("1.0", "end")).strip()
    #should look here into the users table
    print("name input --> ",name_input)
    if checking_credentials(name_input):
        messagebox.showinfo("log_info", "log in successful")
        build_user_page(name_input)
    else:
        messagebox.showwarning("log_info", "wrong credentials")





def build_first_screen():  
    root=Tk()
    root.geometry("200x200")
    root.resizable(False, False)
    label = Label(text = "", width=3, height=3)
    label1 = Label(text = "insert username")
    label_space = Label(text = "", width=1, height=1)
    label_space1 = Label(text = "", width=1, height=1)
    text_box = Text(height=1,width=10)
    #giving the function som earguments without executing it directly with lambd
    button_log = Button(text = "log in", command = lambda: logging_in(text_box))
    label.pack()
    label1.pack()
    label_space.pack()
    text_box.pack()
    label_space1.pack()
    button_log.pack()
    root.mainloop()


build_first_screen()