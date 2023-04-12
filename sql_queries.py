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
        #the first is the name of the opponent while the second is the name of the battle
        name_opponent_and_battle = (selection_var + "  " +  text.get("1.0", "end")).split()
        #here we pass the test if all the fields are filled and all the ships positioned 
        #need to check here for teh battle name 
        with sqlite3.connect(path_to_db) as conn:
            query = 'SELECT * FROM battle_table WHERE name == (?)'
            name_there = (conn.execute(query, (text.get("1.0", "end") ))).fetchall()
            
            
        if len(list(cases_negative.keys())) == 0 and len( name_opponent_and_battle)==2 and name_there=="":
            print("all requirements satisfied to insert")
            #here i save to the db 
            #fist i update the table of the players and then the battle
            with sqlite3.connect(path_to_db) as conn:
            #needs to get the player id if the two players involved
                        values_to_search = (selection_var + "  " + name_creator).split()
                        #looking for the ids in teh table
                        print("values_to_search", values_to_search)
                        #i get the two users_ids here 
                        query = 'SELECT user_id FROM users WHERE name IN ({})'.format(', '.join('?' for _ in values_to_search))
                        ids = conn.execute(query, values_to_search)
                        #first i sname of opponent and the other the one of the creator 
                        #making the list without parenthesis and other strange punctuation
                        ids_int =[str(i) for i in list(ids.fetchall())]
                        #once the players ids have beeen inserted i can proceed with the retrieving of the battle id as it was created
                        #how do i upgrade the user_id? the one creating the table?
                        try:
                            command = "INSERT INTO battle_table(name, creator, opponent) VALUES (?,?,?)"
                            conn.execute(command, (name_opponent_and_battle[1], str(ids_int[1]).translate(translator), str(ids_int[0]).translate(translator)))
                        #committing the results
                            conn.commit()
                        except:
                            messagebox.showinfo("insert error", "battle already created")
                        #yhen i need to save the battle with the formation
                        # here I have to pass lists as some ships have mpre than one value
                        #need the battle id here + creator id) used above and the  
                        command = "SELECT battle_id FROM battle_table WHERE name = (?)"
                        #getting the values for the next query
                        print("what will be inserted", name_opponent_and_battle[0])
                        battle_id_creator_id = conn.execute(command, (str(name_opponent_and_battle[1]),))
                        #can i condense this in one 
                        battle_id_creator_id_fetched =  battle_id_creator_id.fetchall()
                        #now i should have all the elements i need 
                        #now i update using the created value of the battle id so i insert when creating
                        #user_id is te one of the creator that palys first
                        print(" battle_id_creator_id_fetched",  battle_id_creator_id_fetched)
                        command = "INSERT INTO Ships_1(battle_id, user_id, ship_1, ship_2, ship_3, ship_4, player_now_playing) VALUES (?,?,?,?,?,?, ?)"
                        conn.execute(command, (str(battle_id_creator_id_fetched).translate(translator), str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator)))
                        conn.commit()
            pass
        else:
            print("not entering as the condition wasn t satisfied")
            print(cases, cases_negative, name_opponent_and_battle)
        pass
    except Exception as e :
                    
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(e, exc_type, fname, exc_tb.tb_lineno)
                    messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
                    

def retrieve_battle():
    #need here to get the values of the battle back and get them displayed in a playable field
    
    pass
                    