def log_in_function():
    global result, name_input
    list_of_users = ["teresa"]
    name_input = str(text_box.get("1.0", "end")).strip()
    print(name_input)
    if name_input in list_of_users:
        result = messagebox.showinfo("log_info", "log in successful")
        build_second_screen(result, name_input, query_db)
    else:
        messagebox.showwarning("log_info", "wrong credentials")