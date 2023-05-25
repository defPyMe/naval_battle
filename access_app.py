import tkinter as tk
from tkinter import ttk

def get_selected_option():
    selected_option = option_var.get()
    print("Selected option:", selected_option)

root = tk.Tk()

# Create a StringVar to hold the selected option
option_var = tk.StringVar()

# Create the OptionMenu widget
option_menu = ttk.OptionMenu(root, option_var, "Option 1", "Option 2", "Option 3")
option_menu.pack()

# Create a button to retrieve the selected option
button = tk.Button(root, text="Get Selected Option", command=get_selected_option)
button.pack()

root.mainloop()
