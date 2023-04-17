import sqlite3
import io 
from PIL import ImageTk,  ImageFont, ImageDraw
#this addresses some display issues when it comes ot the picture of the user
import PIL.Image
from tkinter import *
from tkinter import messagebox
import string
import sys , os
from user_page_module import create_field

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
        #needs to create the battle before we can save the data 
        try:
            values_to_search = (selection_var + "  " + name_creator).split()
            #looking for the ids in teh tabl
            #i get the two users_ids here 
            with sqlite3.connect(path_to_db) as conn:
                query = 'SELECT user_id FROM users WHERE name IN ({})'.format(', '.join('?' for _ in values_to_search))
                ids = conn.execute(query, values_to_search)
                #first i sname of opponent and the other the one of the creator 
                #making the list without parenthesis and other strange punctuation
                ids_int =[str(i) for i in list(ids.fetchall())]
                #once the players ids have beeen inserted i can proceed with the retrieving of the battle id as it was created
                #how do i upgrade the user_id? the one creating the table?
                command = "INSERT INTO battle_table(name, creator, opponent) VALUES (?,?,?)"
                conn.execute(command, (name_opponent_and_battle[1], str(ids_int[1]).translate(translator), str(ids_int[0]).translate(translator)))
            #committing the results
                conn.commit()
                #storing the battle_id in a variable here 
                query = 'SELECT battle_id FROM battle_table WHERE name=(?)'
                id_to_index = conn.execute(query, (name_opponent_and_battle[1], ))
                id_fetched = id_to_index.fetchone()
        except Exception as e:
            messagebox.showerror("general error", "some error occurred while creating the battle")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
        try:
            with sqlite3.connect(path_to_db) as conn:
                
            #not sure this is needed anyway 
                if len(list(cases_negative.keys())) == 0 and len( name_opponent_and_battle)==2:
                    print("id fetched", id_fetched)
                    try:
                        command = "UPDATE Ships_1 SET user_id = (?) , ship_1 = (?), ship_2 = (?), ship_3 = (?), ship_4 = (?), player_now_playing = (?) WHERE battle_id = (?)"
                        conn.execute(command, (str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched))
                        conn.commit()
                    except Exception as e:
                        messagebox.showinfo("insert error", "battle already created")
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(e, exc_type, fname, exc_tb.tb_lineno)
                        messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
                    #yhen i need to save the battle with the formation
                    # here I have to pass lists as some ships have mpre than one value
                    #need the battle id here + creator id) used above and the  
                        ("not entering as the condition wasn t satisfied")
                        print(cases, cases_negative, name_opponent_and_battle)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
            messagebox.showerror("general error", "general error ")
        pass
    except Exception as e :
                    
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(e, exc_type, fname, exc_tb.tb_lineno)
                    messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
                    

#needs id of th eplayer 
def loading_battle(name_battle, id_of_battle):
    #here i need to pass in the values for the different 
    #gets the battle id starting from the name 
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT * FROM Ships_1 WHERE  battle_id = (?)"
        positioning = conn.execute(command, (id_of_battle,))
        fetching_positions =positioning.fetchone()
 #(6, 2, "['34']", "['22','23'] ", "['56','65','75']", "['13',14'','15','16']", None, None, None, None, None, '1')
    all_ships = { list(fetching_positions[2]): "orange" ,  list(fetching_positions[3]):"blue",  list(fetching_positions[4]):"purple", list(fetching_positions[5]):"pink"}
    #getting the hits as well 
    ship_1_hit = list(fetching_positions[6])
    ship_2_hit = list(fetching_positions[7])
    ship_3_hit = list(fetching_positions[8])
    ship_4_hit = list(fetching_positions[9])
    #getting the misses 
    misses = list(fetching_positions[10])
    #creating the dicrtionary with the colors 
    #all_colors = {"ship_1" : "orange" , "ship_2" : "blue", "ship_3" :  "purple", "ship_4" : "pink" }
    #creating the battle 
    base_window = Toplevel()
    frame_field = Frame(base_window)
    player_frame = Frame(base_window)
    base_window.title("New Battle of player :" + name_battle)
    #frame_ships = Frame(base_window)
    #creating the buttons 
    create_field(frame_field)
    #list comprehension to color all values 
    #configure(command=lambda color="orange",frame = frame_field,  button=ship_1, : ship_click(color, frame, button, 1))
    [i.configure(bg=all_ships[])]
    
    
    pass




def retrieve_battle(name, frame):

    #need here to get the values of the battle back and get them displayed in a playable field
    #the battles need to be index in case there is more than one 
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT user_id FROM users WHERE  name = (?)"
        result_of_name_fetch = conn.execute(command, (name,))
        fetching_the_user_id = result_of_name_fetch.fetchone()
        print("user_id fetchwed", fetching_the_user_id)
        conn.commit()
    #getting the battles
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT * FROM Ships_1 WHERE  user_id = (?)"
        result_of_name_fetch = conn.execute(command, (str(*fetching_the_user_id)))
        fetching_the_result = result_of_name_fetch.fetchall()
        conn.commit()
    print("fetching the result", fetching_the_result[0][0])
    #the result i get i sthe following , two lists 
    # [(5, 2, "['25']", "['42', '32']", "['39', '29', '19']", "['56', '46', '36', '26']", '', '', '', '', '', '2'), 
    # (6, 2, "['34']", "['22','23']", "['56','65','75']", "['13',14'','15','16']", None, None, None, None, None, '2')]
    # columns are --> battle_id, user_id, ship_1, ship_2, ship_3, ship_4, ship_1_hit, ship_2_hit, ship_3_hit, ship_4_hit, palyer_now_playing
    #getting the names 
    with sqlite3.connect(path_to_db) as conn:
        list_of_battles_ids = [i[0] for i in fetching_the_result]
        #
        query = 'SELECT name FROM battle_table WHERE battle_id IN ({})'.format(', '.join('?' for _ in list_of_battles_ids))
        ids = conn.execute(query, list_of_battles_ids)
        #first i sname of opponent and the other the one of the creator 
        #making the list without parenthesis and other strange punctuation
        battle_names  =[str(*i) for i in list(ids.fetchall())]
        #getting the lenght of teh list 
        print("battle_names", battle_names)
    for i in range(len(battle_names)):
        #i have the different ids right here in the first index 
        button = Button(frame, text=battle_names[i], command=lambda f=fetching_the_result[i][0]: loading_battle(battle_names, f ))
        button.grid(row=i, column=0)
    
    
    
    
    
    
    pass
                    