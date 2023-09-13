import customtkinter
#defaults to the user one, otherwise if we specify one it will always stay the same 
customtkinter.set_appearance_mode("dark")#system, dark, light
customtkinter.set_default_color_theme("dark-blue")#blue, green, dark-blue


root = customtkinter.Ctk()
root.geometry("500x300")


root.mainloop()