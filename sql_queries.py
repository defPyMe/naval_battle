import sqlite3
import io 
from PIL import ImageTk,  ImageFont, ImageDraw
#this addresses some display issues when it comes ot the picture of the user
import PIL.Image
from tkinter import *
from tkinter import messagebox
import string
import sys , os


path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"

def checking_credentials(name):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT name FROM users WHERE  name = (?)"
        result_of_name_fetch = conn.execute(command, (name,))
        fetching_the_result = result_of_name_fetch.fetchone()
        conn.commit()

    return fetching_the_result

#converting the data into a blob
def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
                blobData = file.read()
        return blobData
    
def check_users(name):
    with sqlite3.connect(path_to_db) as conn:
            #needs changes in the query
        command = "SELECT name FROM users WHERE name IS NOT (?)"
        users = conn.execute(command, (name,))
        conn.commit()
        user_list = users.fetchall()
        
    return user_list
            
#inserting new image
def insert_image(filename, name):
        #returns a path
        img = filename
        #image needs to be converted to binary
        empPhoto = convertToBinaryData(img)
        
        with sqlite3.connect(path_to_db) as conn:
            #needs changes in the query
                        command = "UPDATE users SET user_pic = (?)  WHERE name = (?)"
                        conn.execute(command, (empPhoto, name))
                        conn.commit()
                        
                        
#checking here if i have any picture loaded for a certain name 
def check_if_image(name):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT user_pic FROM users WHERE  name = (?)"
        img = conn.execute(command, (name,))
        #returns a tuple here
        photo_tuple = img.fetchone()
    if photo_tuple == None:
        pass
        #need to add a default pic
    else:
        img="download.png"
        empPhoto = convertToBinaryData(img)
        #here i update a different pic
        with sqlite3.connect(path_to_db) as conn:
            #needs changes in the query
                command = "UPDATE users SET user_pic = (?)  WHERE name = (?)"
                conn.execute(command, (empPhoto, name))
                conn.commit()  
            
#retrieving the image
def retrieve_image(name, current_window ):
    with sqlite3.connect(path_to_db) as conn:
                            command = "SELECT user_pic FROM users WHERE  name = (?)"
                            img = conn.execute(command, (name,))
                            #returns a tuple here
                            photo_tuple = img.fetchone()
                            print("photo tuple", photo_tuple)
                            
                            photo = photo_tuple[0]
    fp = io.BytesIO(photo)
    image = PIL.Image.open(fp)
                    # convert the image : ata to file object
    render = ImageTk.PhotoImage(image)
                    #displaying it 
                    # Create a Label Widget to display the text or Image
    label_picture = Label( current_window, image = render, width=350, height=350)
                    #needs to be recalled here as well
    label_picture.image = render # keep a reference!
    #should i grid always in the same position so that i do not have any problems when using this in different screens 
    label_picture.grid(row=1, column=0)
    
    
def SaveBattle(name_creator, field, text, options):
    #should get the different ships we have placed
    try:
        #her ei get the texts to save in the database
        ship_1 = [i["text"] for i in field.grid_slaves() if i["bg"]=="orange"]
        ship_2 = [i["text"]  for i in field.grid_slaves() if i["bg"]=="blue"]
        ship_3 = [i["text"]  for i in field.grid_slaves() if i["bg"]=="purple"]
        ship_4 = [i["text"]  for i in field.grid_slaves() if i["bg"]=="pink"]
        
        checking_the_ship = {"ship_1": (bool(len(ship_1)==1)),  "ship_2": (bool(len(ship_2)==2)),
                            "ship_3":(bool(len(ship_3)==3)), "ship_4":(bool(len(ship_4)==4))}
        #i check for the trues in the dict 
        cases = {key: value for key, value in checking_the_ship.items() if value == True}
        cases_negative = {key: value for key, value in checking_the_ship.items() if value == False}
        #the conditions are that the elements on the textbox are taken and the list of the negative is ==0
        #now i clean the string building a translator
        #the first two are empty strings as we do not want to map any characters, the third is the constant containing what we want to remove 
        translator = str.maketrans("","", string.punctuation)
        selection_var = options.get().translate(translator)
        name_battle_and_opponent = (selection_var + "  " +  text.get("1.0", "end")).split()
        if len(list(cases_negative.keys())) == 0 and len( name_battle_and_opponent)==2:
            #here i save to the db 
            #fist i update the table of the players and then the battle
            with sqlite3.connect(path_to_db) as conn:
            #needs to get the player id if the two players involved
                        values_to_search = (selection_var + "  " + name_creator).split()
                        #looking for the ids in teh table
                        print("values_to_search", values_to_search)
                        query = 'SELECT user_id FROM users WHERE name IN ({})'.format(', '.join('?' for _ in values_to_search))
                        ids = conn.execute(query, values_to_search)
                        ids_int =ids.fetchall()
                        #now i can update the battle_table ith what i have 
                        

                        command = "UPDATE battle_table SET name = (?),  player1 = (?), player2 = (?)"
                        conn.execute(command, (name_battle_and_opponent[1], name_creator,  selection_var ))
                        #yhen i need to save the battle with the formation
                        # here I have to pass lists as some ships have mpre than one value
                        #need the battle id here
                        command = """UPDATE Ships_1 SET ship_1 = (?) , ship_2 = (?) , ship_3 = (?) , ship_4 = (?), player_now_playing = (?)
                        WHERE battle_id =(?) AND user_id = (?)"""
                        conn.execute(command , (ship_1, ship_2, ship_3, ship_4, ids_int[1]))
                        conn.commit()
            pass
        else:
            print(cases, cases_negative, name_battle_and_opponent)
        pass
    except Exception as e :
                    
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(e, exc_type, fname, exc_tb.tb_lineno)
                    messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")