import sqlite3
import io 
from PIL import ImageTk, Image, ImageFont, ImageDraw
from tkinter import *


def retieve_image(name):
    with sqlite3.connect("path_to_db") as conn:
                            command = "SELECT * FROM comments_table WHERE  id = (?)"
                            img = conn.execute(command, (line_to_change,))
                            #returns a tuple here
                            photo_tuple = img.fetchone()
                            photo = photo_tuple[3]
    fp = io.BytesIO(photo)
    image = Image.open(fp)
                    # convert the image : ata to file object
    render = ImageTk.PhotoImage(image)
                    #displaying it 
                    # Create a Label Widget to display the text or Image
    label_picture = Label( new_window_picture_display, image = render)
                    #needs to be recalled here as well
    label_picture.image = render # keep a reference!
    label_picture.pack()