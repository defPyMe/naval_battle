from tkinter import *
from tkinter import messagebox
from user_page_module import build_user_page
from sql_queries_ import checking_credentials, delete_widgets


def logging_in(name_input, root):
    #need to add a connection to the list of users here 

    #should look here into the users table
    print("name input --> ",name_input)
    if checking_credentials(name_input):
        messagebox.showinfo("log_info", "log in successful")
        #here called with the delete widget function
        build_user_page(delete_widgets(root),name_input, root )
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
    text_box = Entry(root)
    #giving the function som earguments without executing it directly with lambd
    button_log = Button(text = "log in", command = lambda: logging_in(text_box.get().strip(), root))
    #lambda needs lambda event here to work
    text_box.bind('<Return>',  lambda event: logging_in(text_box.get().strip(), root))
    label.pack()
    label1.pack()
    label_space.pack()
    text_box.pack()
    label_space1.pack()
    button_log.pack()
    root.mainloop()


build_first_screen()


#change the loading battle back