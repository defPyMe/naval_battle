from build_user_page_module import buid_user_page




def log_in_function():
    #need to add a connection to the list of users here 
    name_input = str(text_box.get("1.0", "end")).strip()
    print(name_input)
    list_of_users = []
    if name_input in list_of_users:
        result = messagebox.showinfo("log_info", "log in successful")
        build_user_page()
    else:
        messagebox.showwarning("log_info", "wrong credentials")