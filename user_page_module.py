from tkinter import *
import sqlite3
import io
#from retrieve_user_image import retrieve_image

def build_user_page(name):
    base_window = Toplevel()
    base_window.title("Military Base :" + name )
    frame_pic = Frame(base_window)
    frame_buttons = Frame(base_window)
    frame_pic.grid(row=0, col=0)
    frame_buttons.grid(row=0, col=1)
    label_player_name = Label(text=name, width=7)
    #retrieve_image(name)
    
   
    