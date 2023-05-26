from tkinter import * 
root=Tk()
selected_option = StringVar(value="emmas")

option_menu = OptionMenu(root, selected_option, value="emmas")
option_menu.pack()
print(selected_option.get())
