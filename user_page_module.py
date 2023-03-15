from tkinter import *
import sqlite3
import io
from tkinter import filedialog
#from retrieve_user_image import retrieve_image
from sql_queries import insert_image
from tkinter import messagebox

def open(name):
    file = filedialog.askopenfilename(title='search images' , filetypes=(('png','*.png'),('jpeg', '*.jpg')))
    if file:
        insert_image(file, name)
    else:
        messagebox.showwarning("log_info", "wrong credentials")


def build_modify_profile(name):
    base_window = Toplevel()
    base_window.title("Profile detail : "+ name)
    label_username = Label(text="Name of the user")
    username = Text(height=1,width=10)
    username.insert("1.0", name)
    pic_to_change = Button(text="Select picture to change", command=lambda: open(name))
    #needs to show the pic here 
    
    

        
        
        
        
    


def build_user_page(name):
    base_window = Toplevel()
    base_window.geometry("500x300")
    base_window.title("Military Base : " + name )
    frame_pic = Frame(base_window)
    frame_buttons = Frame(base_window)
    frame_pic.grid(row=0, column=0)
    frame_buttons.grid(row=0, column=1)
    label_player_name = Label(frame_pic, text=name, width=7, padx=(70, ))
    #retrieve_image(name)
    button_new_battle = Button(frame_buttons, text="new battle",width=15, height=2,bg="red", command="")
    button_old_battles = Button(frame_buttons, text="show old battles",width=15, height=2,bg="red", command="")
    button_show_champions = Button(frame_buttons, text="show champions",width=15, height=2,bg="red", command="")
    button_change_profile = Button(frame_buttons, text="change profile",width=15, height=2,bg="red", command=lambda: build_modify_profile(name))
    
    label_player_name.grid(row=0, column=0)
    button_new_battle.grid(row=0, column=0,padx=(150,10), pady=20)
    button_old_battles.grid(row=1, column=0,padx=(150,10), pady=10 )
    button_show_champions.grid(row=2, column=0,padx=(150,10), pady=10)
    button_change_profile.grid(row=3, column=0,padx=(150,10), pady=10)
    