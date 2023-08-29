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
import ast



path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"
translator = str.maketrans("","", string.punctuation)



def getting_user_id_from_name(name):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT user_id FROM users WHERE  name = (?)"
        result_of_name_fetch = conn.execute(command, (name,))
        fetching_the_user_id = result_of_name_fetch.fetchone()
        conn.commit()
        return fetching_the_user_id

def getting_name_from_id(id_):
    with sqlite3.connect(path_to_db) as conn:
        if type(id_) is tuple:
            print("what the passed id is and it should be a tuple---->", id_)
            id_=id_[0]
        else:
            pass
        command = "SELECT name FROM users WHERE  user_id = (?)"
        result_of_name_fetch = conn.execute(command, str(id_))
        fetching_the_user_id = result_of_name_fetch.fetchone()
        conn.commit()
        return fetching_the_user_id





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
    
    
def SaveBattle(name_creator, field, text, options, flag):
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
        #need to verify the condition here , once i have all the conditions i do not need also to create a new battle
        
        
        if len(list(cases_negative.keys())) == 0 and len( name_opponent_and_battle)==2:
            
            try:
                values_to_search = (selection_var + "  " + name_creator).split()
                #looking for the ids in teh tabl
                #i get the two users_ids here 
                print("values to seearch ", values_to_search)
                with sqlite3.connect(path_to_db) as conn:
                    query = 'SELECT user_id FROM users WHERE name IN ({})'.format(', '.join('?' for _ in values_to_search))
                    ids = conn.execute(query, values_to_search)
                    #first i sname of opponent and the other the one of the creator 
                    #making the list without parenthesis and other strange punctuation
                    ids_int =[str(i) for i in list(ids.fetchall())]
                    print("ids_int", ids_int)
                    if flag==0:
                        #once the players ids have beeen inserted i can proceed with the retrieving of the battle id as it was created
                        #how do i upgrade the user_id? the one creating the table?
                        command = "INSERT INTO battle_table(name, creator, opponent) VALUES (?,?,?)"
                        #is this wrong here
                        print("checking wjhat is inserted when crearting a table", name_opponent_and_battle[1], str(ids_int[0]).translate(translator), str(ids_int[1]).translate(translator))
                        conn.execute(command, (name_opponent_and_battle[1], str(ids_int[0]).translate(translator), str(ids_int[1]).translate(translator)))
                    #committing the results
                        conn.commit()
                    else:
                        pass
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
                            if flag==0:
                                #here something happening differently if is the opponent or the user inserting , as i do not need to qupdate the information i have already there
                                # info already inserted = battle_id, user_id, player now playing
                                command = "UPDATE Ships_1 SET user_id = (?) , ship_1 = (?), ship_2 = (?), ship_3 = (?), ship_4 = (?), player_now_playing = (?) WHERE battle_id = (?)"
                                conn.execute(command, (str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched))
                                #adding also the battle of the opponent 
                                print("first insertion",(str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched) )
                                conn.commit()
                            else:
                                #here something happening differently if is the opponent or the user inserting , as i do not need to qupdate the information i have already there
                                # info already inserted = battle_id, user_id, player now playing
                                print("first insertion",(str(ship_1), str(ship_2), str(ship_3), str(ship_4),id_fetched[0], ids_int[0].translate(translator), "isolating the battle id", id_fetched[0]  ))
                                command = "UPDATE Ships_1 SET ship_1 = (?), ship_2 = (?), ship_3 = (?), ship_4 = (?) WHERE battle_id = (?) AND user_id = (?)"
                                conn.execute(command, (str(ship_1), str(ship_2), str(ship_3), str(ship_4), *id_fetched, ids_int[0].translate(translator)))
                                messagebox.showinfo("inserted ships", "battle now playing")
                                #adding also the battle of the opponent 
                                
                                conn.commit()
                        except Exception as e:
                            messagebox.showinfo("insert error", "battle already created")
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(e, exc_type, fname, exc_tb.tb_lineno)
                            messagebox.showinfo(message=str(e)+ "/n" + str(exc_type)+ "/n" + str(fname)+ "/n" + str(exc_tb.tb_lineno)+ "/n")
                        try:
                            if flag==0:
                                command = "INSERT INTO Ships_1(battle_id, user_id, ship_1, ship_2, ship_3, ship_4, player_now_playing) VALUES(?,?,?,?,?,?,?)"
                                conn.execute(command, (*id_fetched, str(ids_int[0]).translate(translator),"", "", "", "", str(ids_int[1]).translate(translator)))
                                print("second insertion",((str(ids_int[0]).translate(translator),"", "", "", "", str(ids_int[1]).translate(translator), *id_fetched) ))
                                conn.commit()
                            else:
                                pass
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
            messagebox.showerror("misplaced ships or missing element", "Please position all the ships or fill in name of the battle and opponent")
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
    










def fetching_the_battle(id_of_battle, id_user):
    with sqlite3.connect(path_to_db) as conn:
        #adding also the id of the user to fetch that of the opponet 
        command = "SELECT * FROM Ships_1 WHERE  battle_id = (?) AND user_id= (?)"
        positioning = conn.execute(command, (id_of_battle[0], id_user))
        fetching_positions = [i if i!=None else "" for i in positioning.fetchone()]
        return fetching_positions
    
#adding a flag to see if it is coloring a retrieve dbattle ot a new one , also if it is ongoing
def coloring(frame, all_ships_opponent, all_hits_opponent, all_misses_opponent, flag, j):
    #turn
    print("all lists to color ", all_hits_opponent, all_misses_opponent , all_ships_opponent)


    #coloring the ships
    # flag == 0 then coloring at loadingy, battle not ended   ---- [i for i in all_ships]
    if flag==0:
        all_ships_opponent_ = ast.literal_eval(all_ships_opponent[0])
        all_misses_opponent_ = ast.literal_eval(all_misses_opponent[0])
        all_hits_opponent_ = ast.literal_eval(all_hits_opponent[0])
        print("all buttons??", frame.grid_slaves(), frame.winfo_class())
        print("entering the coloring 0 flag that should color all the already pressed buttons, ", "all_hits_opponent", all_hits_opponent, "all misses opponent", all_misses_opponent)
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in [i for i in all_misses_opponent_]]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in [i for i in all_hits_opponent_]]

    #coloring when loading ended
    elif flag == 1:
        #all the buttons are colored , hits red, misses in gray
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] not in all_hits_opponent]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent]
    #at pressing when battle ongoing and hit
    elif flag==2:
        #check the format here 
        
             [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"]==j]
    else:
            [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"]==j]
    pass    


#needs to write on the column chosen updating the field and nto deleting the values already there
# hit_or_misses can be all_misses or all_hits deopending on the case 

def write_hit_miss_update(column, value, id_of_battle, opponent_id, hit_or_misses):
    #first selecting value and then updating and rewriting 
    
    str(hit_or_misses.append(value)).replace("[","").replace("]","").replace("\"", "")
    print("checking what i spassed with hits or misses ", type(hit_or_misses), hit_or_misses, value)
    #using already inserted to add 
    with sqlite3.connect(path_to_db) as conn:
        #setting the user_id equal to the opponent_id
        command = f"UPDATE Ships_1 SET {column} = (?) WHERE battle_id = (?) AND user_id = (?)" 
        #column passed in directly in teh function?
        #printing out teh values passd 
        #print("values passed on to the command  ",column,value,  type(value), type(id_of_battle), id_of_battle, type(opponent_id), opponent_id )
        
        adding = conn.execute(command, ( str(hit_or_misses),id_of_battle[0], opponent_id ))
        
        
        return None
    
#boom_trial(j, )

#assuming the js here are only the clickable buttons as the others are disabled 
def boom_trial(j, frame, all_hits_opponent, all_misses_opponent,  all_ships_opponent, id_opponent, id_of_battle):
    #checking if the button is present in the all_ships_list
    #creating j comma as i need to create a list
    j_comma  = j
 
    if j in all_ships_opponent:
        print("checking what we pass in the boom trial case of hit", all_hits_opponent, type(all_hits_opponent))
        #writing to hits here
        write_hit_miss_update('hits', j_comma , id_of_battle, id_opponent, all_hits_opponent)
        coloring(frame, all_ships_opponent, all_hits_opponent, all_misses_opponent, 2, j)
    else:
        print("checking what we pass in the boom trial case of miss", all_misses_opponent, type(all_misses_opponent))
        #writing to hits here
        write_hit_miss_update('misses', j_comma , id_of_battle, id_opponent,  all_misses_opponent)
        #update sunk
        #what is what here??
        coloring(frame, all_ships_opponent, all_hits_opponent, all_misses_opponent, 3, j)
        

       
#here i need to design the different commands. checking if the pressed button is in the ships ones           

   
    

            
#needs id of th eplayer , user_id should be the one playing
def loading_battle(id_of_battle, user_id, flag, name):
    #what is it that i am passing 
    print("two arguments ---->",id_of_battle, user_id )
    base_window = Toplevel()
    frame_field_retr = Frame(base_window)
    player_frame = Frame(base_window)
    #here i need to pass in the values for the different 
    #gets the battle id starting from the name ,fetches all the ships 
    fetching_positions = fetching_the_battle(id_of_battle, user_id[0])
    #if all ships are positioned for me then i can load the battle with no names and buttons
    print("fetching tuples name and id check",  id_of_battle)
    all_ships_player = [(fetching_positions[2][2:4]) ,  (fetching_positions[3][2:4]),(fetching_positions[3][8:10]),
                 (fetching_positions[4][2:4]), (fetching_positions[4][8:10]),(fetching_positions[4][14:16]),
                 (fetching_positions[5][2:4]), (fetching_positions[5][8:10]), (fetching_positions[5][14:16]), (fetching_positions[5][20:22])]
    #fetching the all hits on my side
    all_hits_player = [fetching_positions[6]]
    #all the hits on the side of the opponent
    #getting id of player
    all_misses_player = [fetching_positions[7]]
    all_ships_tuples = [(all_ships_player[0],),(all_ships_player[1],all_ships_player[2]),(all_ships_player[3],
                        all_ships_player[4],all_ships_player[5]),(all_ships_player[6],
                        all_ships_player[7],all_ships_player[8], all_ships_player[9])]
    
    all_common_player_no_null = [i for i in all_ships_player if i in all_hits_player and i!=""]
    #all_common_player_no_null = [i for i in all_common_player if i!=""]
    
    
    
    
    id_opponent = (getting_user_id_from_name(id_of_battle[2][0]))[0]

    fetching_positions_opponent = fetching_the_battle(id_of_battle, id_opponent)
    
    all_ships_opponent = [(fetching_positions_opponent[2][2:4]) ,  (fetching_positions_opponent[3][2:4]),(fetching_positions_opponent[3][8:10]),
                 (fetching_positions_opponent[4][2:4]), (fetching_positions_opponent[4][8:10]),(fetching_positions_opponent[4][14:16]),
                 (fetching_positions_opponent[5][2:4]), (fetching_positions_opponent[5][8:10]), (fetching_positions_opponent[5][14:16]), (fetching_positions_opponent[5][20:22])]
    all_hits_opponent = [fetching_positions_opponent[6]]
    all_misses_opponent = [fetching_positions_opponent[7]]
    #need to add a checìking mechanism to see what the case is at the moment, such as ended, ongoing
    all_ships_opponent_tuples = [(all_ships_opponent[0],),(all_ships_opponent[1],all_ships_opponent[2]),(all_ships_opponent[3],
                    all_ships_opponent[4],all_ships_opponent[5]),(all_ships_opponent[6],
                        all_ships_opponent[7],all_ships_opponent[8], all_ships_opponent[9])]
    #all_common_opponent = [i for i in all_ships_opponent if i in all_hits_opponent]
    all_common_opponent_no_null = [i for i in all_ships_opponent if i in all_hits_opponent and i!=""]
    
    #getting the hits as well 

    
    
    #the first one is not recognized as tuple if not inserted the ast railing comma
    #getting the misses --> needs further eleboration as i should have the data in a list 
    # all_ships_hits = all_ships_keys_isolated 
    # i need to create the difference between the two lists, the starting position are the all_ships
    #creating the dicrtionary with the colors 
    #all_colors = {"ship_1" : "orange" , "ship_2" : "blue", "ship_3" :  "purple", "ship_4" : "pink" }
    #creating the battle 

    #one of the two battles has ended
    if len(all_common_opponent_no_null)==10:
        print("entering opponent won")
    #opponent won
    #id_of_battle[2][0] --> opponent _name
        user_page_module.new_battle(id_of_battle[2][0], 2,all_hits_player, all_misses_player, id_opponent, id_of_battle)
        base_window.title("Winner  of the battle is: " + id_of_battle[2][0])
    
    elif len(all_common_player_no_null)==10:
        print("entering player won")
        #player won
        user_page_module.new_battle(name[0], 2,all_hits_player, all_misses_player,  all_ships_opponent, id_opponent, id_of_battle)
        
        #here i need to create the field as it is in the initial option but saved ships are not clickable
        
        # coloring all retrieved ships
        #need to display the winner- adding it to the name of the window
        base_window.title("Winner of the battle is:" + name)
        #case in which the ships have been positioned only by the opponent 
        #case of non ended game, just started or not started
    else:  
        wid = user_page_module.new_battle(name[0], 1,all_hits_player, all_misses_player,  all_ships_opponent, id_opponent, id_of_battle)
        print("entering battle still ongoing")
        #coloring as it is ongoing
        coloring(wid, all_ships_opponent, all_hits_opponent, all_misses_opponent, 0,"")
 
 
        pass

#    if len(all_ships)==10:
#        messagebox.showinfo("ended battle", "BAttle has ended and the winner is")
#    else:
#        messagebox.showinfo("battle still pending", "Battle has not ended and it is turn :")   
#    pass


def starting_battle_command():
    
    pass




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
        button = Button(frame, text=battle_names[i], command=lambda f=(fetching_the_result[i][0],battle_names[i],opponent_current_battle): loading_battle(f , user_id, 0, name))
        button.grid(row=i, column=0)
    pass
                    

