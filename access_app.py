#from user_page_module import build_user_page
from tkinter import messagebox
from build_first_screen import text_box


def logging_in():
    #need to add a connection to the list of users here 
    name_input = str(text_box.get("1.0", "end")).strip()
    list_of_users = []
    if name_input in list_of_users:
        result = messagebox.showinfo("log_info", "log in successful")
        #build_user_page()
    else:
        messagebox.showwarning("log_info", "wrong credentials")