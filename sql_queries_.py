import sqlite3
import io 
from PIL import ImageTk,  ImageFont, ImageDraw
#this addresses some display issues when it comes ot the picture of the user
import PIL.Image
from tkinter import *
from tkinter import messagebox
import string
import sys , os
import user_page_module



path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"
translator = str.maketrans("","", string.punctuation)
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
        user_list =[ i[0] for i in users.fetchall()]
        
        
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
        
        selection_var = options.get().translate(translator)
        #the first is the name of the opponent while the second is the name of the battle
        name_opponent_and_battle = (selection_var + "  " +  text.get("1.0", "end")).split()
        #here we pass the test if all the fields are filled and all the ships positioned 
        #need to check here for teh battle name 
        #needs to create the battle before we can save the data 
        if len(list(cases_negative.keys())) == 0 and len( name_opponent_and_battle)==2:
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
                    print("ids_int", ids_int)
                    #once the players ids have beeen inserted i can proceed with the retrieving of the battle id as it was created
                    #how do i upgrade the user_id? the one creating the table?
                    command = "INSERT INTO battle_table(name, creator, opponent) VALUES (?,?,?)"
                    #is this wrong here
                    conn.execute(command, (name_opponent_and_battle[1], str(ids_int[0]).translate(translator), str(ids_int[1]).translate(translator)))
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
                # CHECK HERE IF IT IS NEEDED OR NOT 
                #not sure this is needed anyway 
                    
                        print("id fetched", id_fetched)
                        try:
                            command = "UPDATE Ships_1 SET user_id = (?) , ship_1 = (?), ship_2 = (?), ship_3 = (?), ship_4 = (?), player_now_playing = (?) WHERE battle_id = (?)"
                            conn.execute(command, (str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched))
                            #adding also the battle of the opponent 
                            print("first insertion",(str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched) )
                            conn.commit()
                            
                        except Exception as e:
                            messagebox.showinfo("insert error", "battle already created")
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(e, exc_type, fname, exc_tb.tb_lineno)
                            messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
                        try:
                            command = "INSERT INTO Ships_1(battle_id, user_id, ship_1, ship_2, ship_3, ship_4, player_now_playing) VALUES(?,?,?,?,?,?,?)"
                            conn.execute(command, (*id_fetched, str(ids_int[0]).translate(translator),"", "", "", "", str(ids_int[1]).translate(translator)))
                            print("second insertion",((str(ids_int[0]).translate(translator),"", "", "", "", str(ids_int[1]).translate(translator), *id_fetched) ))
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
        else:
            messagebox.showerror("misplaced ships", "Please position all the ships or fill in name and opponent")
    except Exception as e :
                    
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(e, exc_type, fname, exc_tb.tb_lineno)
                    messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")



def continuing_battle():
    #gets the number of the pressed button
    #checks in it is in the saved ships or not
    #if not in the saved ships gets turned dark gray as it is a miss
    
    pass




def create_field_over(frame,all_ships):
    
    #once created we also assign the colors and the functionality
    for i in range(10):
        for j in range(10):
            #adding here the command 
            button = Button(frame, text=str(i)+str(j), command="")
            button.grid(row=i, column=j)
    frame.grid(row=0, column=0, padx=10, pady=10)
    color_ships = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in [i for i in all_ships]]
    configure_field = [i.configure(bg="grey", state=DISABLED) for i in frame.grid_slaves() if i["text"] not in [i for i in all_ships]]
    










def fetching_the_battle(id_of_battle):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT * FROM Ships_1 WHERE  battle_id = (?)"
        positioning = conn.execute(command, (id_of_battle[0],))
        fetching_positions = [i if i!=None else "" for i in positioning.fetchone()]
        return fetching_positions
    pass

def write_hit_miss_update(column, value, id_of_battle):
    with sqlite3.connect(path_to_db) as conn:


        command = "UPDATE Ships_1 SET {}={} || (?) WHERE battle_id = (?)".format(column, column)
        adding = conn.execute(command, (value,id_of_battle[0],))
        
        
        return None


#assuming the js here are only the clickable buttons as the others are disabled 
def boom_trial(j, frame, all_ships,all_ships_tuples,  id_of_battle, fetching_positions):
    #checking if the button is present in the all_ships_list
    j_comma  = j+","
 
    if j in all_ships:
        #writing to hits here
        write_hit_miss_update('hits', j_comma , id_of_battle)
        update = fetching_the_battle(id_of_battle)
        [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"]==j]
        #update sunk
        #what is what here??
        # Example: Check if all tuple members are in a list using list comprehension
     #from user_page_module import build_user_page
        # is the hits already fetched or not? yes it is in the fetching positions --> 6--> should be saved as list
        #[7, 1, "['34']", "['22','23']", "['55','65','75']", "['13','14','15','16']", '', "'34','22','23','55','65','75','13','14','15','16'", '1']
        print("fetching positions [6]", update[6].split(","))
        results = [all(member in update[6].split(",") for member in tpl) for tpl in all_ships_tuples]

        matching_tuples = [tpl for tpl, result in zip(all_ships_tuples, results) if result]
        #matching tuples should now be whai i need 
        #coloring all the values we have in the tuples darck red
        
        ff = [i.configure(bg="red4", state=DISABLED) for i in frame.grid_slaves() if i["text"] in [value for tpl in  matching_tuples for value in tpl]]
        #l = [(1, 2), (4, 3), (5, 7), (9, 13)]#all_ships_tuples
        #values = [1, 2, 5, 6, 8, 9, 0]#hits
        print("matching tuples", results, matching_tuples, ff)
        #results = [all(member in values for member in tpl) for tpl in l]
        #print(results)  # Output: [True, False, True, False]
        #matching_tuples = [tpl for tpl, result in zip(l, results) if result]
        
        
    else:
        write_hit_miss_update('misses', j_comma , id_of_battle)
        #write and update the field settings for single button miss
        [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"]==j]

    pass
       
       
       
#here i need to design the different commands. checking if the pressed button is in the ships ones           
#this is teh field initialization, so i can keep the first values static
def create_field_ongoing(frame,all_ships, all_ships_tuples, all_common, all_pressed, base_window,name_battle, fetching_positions, id_of_battle):
    #all common  needs to be recalculated, the only thing i keep static are the ships
    for i in range(10):
        for j in range(10):
            #adding here the command for all
            button = Button(frame, text=str(i)+str(j), command=lambda j=str(i)+str(j): boom_trial(j, frame,  all_ships, all_ships_tuples, id_of_battle, fetching_positions))
            button.grid(row=i, column=j)
    frame.grid(row=0, column=0, padx=10, pady=10)
    #all the common ones if present are configured here
    configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_pressed]
    configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_common]
    base_window.title("Battle of player:" + name_battle[0])
    
            
            
#needs id of th eplayer , user_id should be the one playing
def loading_battle(id_of_battle, user_id):

    #here i need to pass in the values for the different 
    #gets the battle id starting from the name 
    fetching_positions = fetching_the_battle(id_of_battle)
    
    print("fetching tuples name and id check",  id_of_battle)
    all_ships = [(fetching_positions[2][2:4]) ,  (fetching_positions[3][2:4]),(fetching_positions[3][8:10]),
                 (fetching_positions[4][2:4]), (fetching_positions[4][8:10]),(fetching_positions[4][14:16]),
                 (fetching_positions[5][2:4]), (fetching_positions[5][8:10]), (fetching_positions[5][14:16]), (fetching_positions[5][20:22])]
    print("all_ships------------->", all_ships)
    #getting the hits as well 
    #the first one is not recognized as tuple if not inserted the ast railing comma
    all_ships_tuples = [(all_ships[0],),(all_ships[1],all_ships[2]),(all_ships[3],all_ships[4],all_ships[5]),(all_ships[6],all_ships[7],all_ships[8], all_ships[9])]
    print("all_ships_tuples------------->", all_ships_tuples)
    #getting the misses --> needs further eleboration as i should have the data in a list 
    # all_ships_hits = all_ships_keys_isolated 
    all_pressed = [fetching_positions[6]]
    # i need to create the difference between the two lists, the starting position are the all_ships
    all_common = [i for i in all_ships if i in all_pressed]
    #creating the dicrtionary with the colors 
    #all_colors = {"ship_1" : "orange" , "ship_2" : "blue", "ship_3" :  "purple", "ship_4" : "pink" }
    #creating the battle 
    base_window = Toplevel()
    frame_field_retr = Frame(base_window)
    player_frame = Frame(base_window)
    all_common_no_null = [i for i in all_common if i!=""]
    if len(all_common_no_null)==10:
        #here i need to create the field as it is in the initial option but saved ships are not clickable
        create_field_over(frame_field_retr, all_ships)
        # coloring all retrieved ships
        #need to display the winner- maybe putting a new column with the winner 
        base_window.title("Winner  of the battle is:" + id_of_battle[1])
        #case in which the ships have been positioned only by the opponent 
    elif len(all_common_no_null)==0:
        print("entering all common, args",fetching_positions )
        #building page with no ships but already created
        user_page_module.new_battle(id_of_battle[1], 1, id_of_battle[1], id_of_battle[2])
       
        #case it is less it is still an active battle
        #need to isolate the different buttons if they where hit and where ships
        pass

#    if len(all_ships)==10:
#        messagebox.showinfo("ended battle", "BAttle has ended and the winner is")
#    else:
#        messagebox.showinfo("battle still pending", "Battle has not ended and it is turn :")   
#    pass


def starting_battle_command():
    
    pass

def getting_user_id_from_name(name):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT user_id FROM users WHERE  name = (?)"
        result_of_name_fetch = conn.execute(command, (name,))
        fetching_the_user_id = result_of_name_fetch.fetchone()
        conn.commit()
        return fetching_the_user_id

def getting_name_from_id(id):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT name FROM users WHERE  user_id = (?)"
        result_of_name_fetch = conn.execute(command, (id,))
        fetching_the_user_id = result_of_name_fetch.fetchone()
        conn.commit()
        return fetching_the_user_id



def retrieve_battle(name, frame, user_id):
    print("user_id----------->    ", user_id)
    #need here to get the values of the battle back and get them displayed in a playable field
    #the battles need to be index in case there is more than one 
    #getting the battles, all the battle s of a player
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT * FROM Ships_1 WHERE  user_id = (?)"
        result_of_name_fetch = conn.execute(command, (str(*user_id)))
        fetching_the_result = result_of_name_fetch.fetchall()
        conn.commit()
    print("fetching the result", fetching_the_result)
    #the result i get i sthe following
    # [(5, 2, "['25']", "['42', '32']", "['39', '29', '19']", "['56', '46', '36', '26']", '', '', '', '', '', '2'), 
    # (6, 2, "['34']", "['22','23']", "['56','65','75']", "['13',14'','15','16']", None, None, None, None, None, '2')]
    # columns are --> battle_id, user_id, ship_1, ship_2, ship_3, ship_4, ship_1_hit, ship_2_hit, ship_3_hit, ship_4_hit, palyer_now_playing
    #getting the names 
    with sqlite3.connect(path_to_db) as conn:
        list_of_battles_ids = [i[0] for i in fetching_the_result]
        query = 'SELECT name,opponent FROM battle_table WHERE battle_id IN ({})'.format(', '.join('?' for _ in list_of_battles_ids))
        ids = conn.execute(query, list_of_battles_ids)
        #first i sname of opponent and the other the one of the creator 
        #making the list without parenthesis and other strange punctuation
        #needs an obj to be iterable
        fetched = ids.fetchall()
        print("fetche ----->d", fetched)
        battle_names  = [i[0] for i in fetched] 
        opponent_ids = [i[1] for i in fetched]
        #getting who is playing now with the id
        player_now_playing = [i[8] for i in fetching_the_result]
        
  
        #getting the lenght of teh list 
        #PROCESSED VALUES
        








    for i in range(len(battle_names)):
        #getting the name from the id
        opponent_current_battle = getting_name_from_id(opponent_ids[i])
        #i have the different ids right here in the first index ??
        #which one is the name of the chosen battle
        #f is now a tuple with the name and id
        button = Button(frame, text=battle_names[i], command=lambda f=(fetching_the_result[i][0],battle_names[i],opponent_current_battle): loading_battle(f , user_id))
        button.grid(row=i, column=0)
    pass
                    

