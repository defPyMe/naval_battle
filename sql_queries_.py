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
import time


path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"
translator = str.maketrans("","", string.punctuation)


#refreshing_function 
def refresh(*args):
    #with args[0]=id_of_battle, args[1][0]=user_id[0]
    #fetching_positions = fetching_the_battle(args[0], args[1][0])
    #if all ships are positioned for me then i can load the battle with no names and buttons
    #all values for the player
    #result = processing_fetched_results(fetching_positions, 0)
    print("frame considered  ---------------------------->, ", args[2])
   # need to get the opponent id here 
    id_opponent = getting_opponent_id_from_battle_id(args[0][0], args[1])
    #print("opponent id in the loading battle --> ", id_opponent)
    fetching_positions_opponent = fetching_the_battle(args[0], id_opponent)
    #getting results for opponent , flag 1 for opponent
    result_opponent = processing_fetched_results(fetching_positions_opponent, 1)
    while True:
        #it does nothing if the user id is the same as that of the player now playingz
        time.sleep(3)
        #here result or result opponent are the same, as we write in both when pressing
        if args[1][0] != int(result_opponent["player_now_playing"]):
            #frame field as args[2]
            print("in refreshing, player different from the one that has played in db", args[1][0] ,type(args[1][0]), result_opponent["player_now_playing"], type(result_opponent["player_now_playing"]))
            coloring(args[2], result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'], 0,"")
        else:
            coloring(args[2], result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'], 3,"")
            print("in refreshing, player equal from the one that has played in db", args[1][0] ,result_opponent["player_now_playing"])
        print("refreshe")
    pass

#user id here is the player id, so we can get the opposite 
def getting_opponent_id_from_battle_id(battle_id, user_id):
    #getting opponent id rgardless of whom gets into teh battle
   
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT * FROM battle_table WHERE  battle_id = (?)"
        result_of_battle_fetch = conn.execute(command, (str(battle_id),))
        fetching_the_battle =result_of_battle_fetch.fetchone()
        conn.commit()
        #case in which the creator is accessing
 
    if fetching_the_battle[2]==user_id[0]:
        opponent_id = fetching_the_battle[3]
        
    else:
        opponent_id = fetching_the_battle[2]
        
    return opponent_id




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
            #print("what the passed id is and it should be a tuple---->", id_)
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
                            #print("photo tuple", photo_tuple)
                            
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
                #print("values to seearch ", values_to_search)
                with sqlite3.connect(path_to_db) as conn:
                    query = 'SELECT user_id FROM users WHERE name IN ({})'.format(', '.join('?' for _ in values_to_search))
                    ids = conn.execute(query, values_to_search)
                    #first i sname of opponent and the other the one of the creator 
                    #making the list without parenthesis and other strange punctuation
                    ids_int =[str(i) for i in list(ids.fetchall())]
                    #print("ids_int", ids_int)
                    if flag==0:
                        #once the players ids have beeen inserted i can proceed with the retrieving of the battle id as it was created
                        #how do i upgrade the user_id? the one creating the table?
                        command = "INSERT INTO battle_table(name, creator, opponent) VALUES (?,?,?)"
                        #is this wrong here
                        #print("checking wjhat is inserted when crearting a table", name_opponent_and_battle[1], str(ids_int[0]).translate(translator), str(ids_int[1]).translate(translator))
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
                    
                        #print("id fetched", id_fetched)
                        try:
                            if flag==0:
                                #here something happening differently if is the opponent or the user inserting , as i do not need to qupdate the information i have already there
                                # info already inserted = battle_id, user_id, player now playing
                                command = "UPDATE Ships_1 SET user_id = (?) , ship_1 = (?), ship_2 = (?), ship_3 = (?), ship_4 = (?), player_now_playing = (?) WHERE battle_id = (?)"
                                conn.execute(command, (str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched))
                                #adding also the battle of the opponent 
                                #print("first insertion",(str(ids_int[1]).translate(translator),str(ship_1), str(ship_2), str(ship_3), str(ship_4), str(ids_int[1]).translate(translator), *id_fetched) )
                                conn.commit()
                            else:
                                #here something happening differently if is the opponent or the user inserting , as i do not need to qupdate the information i have already there
                                # info already inserted = battle_id, user_id, player now playing
                               #print("first insertion",(str(ship_1), str(ship_2), str(ship_3), str(ship_4),id_fetched[0], ids_int[0].translate(translator), "isolating the battle id", id_fetched[0]  ))
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
                                #print("second insertion",((str(ids_int[0]).translate(translator),"", "", "", "", str(ids_int[1]).translate(translator), *id_fetched) ))
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
                            #print(cases, cases_negative, name_opponent_and_battle)
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



#needs to have the difference in the player and opponent 
#flag to be used depending on the player or opponent at call
def processing_fetched_results(fetched_results, flag):
    #print("fetched results", fetched_results)
  
    #actually getting the values 
    all_ships_player = [(fetched_results[2][2:4]) ,  (fetched_results[3][2:4]),(fetched_results[3][8:10]),
                    (fetched_results[4][2:4]), (fetched_results[4][8:10]),(fetched_results[4][14:16]),
                    (fetched_results[5][2:4]), (fetched_results[5][8:10]), (fetched_results[5][14:16]), (fetched_results[5][20:22])]
        #fetching the all hits on my side
    all_hits_player = [fetched_results[6]]
    #all the hits on the side of the opponent
    #getting id of player
    all_misses_player = [fetched_results[7]]
    all_ships_tuples = [(all_ships_player[0],),(all_ships_player[1],all_ships_player[2]),(all_ships_player[3],
                        all_ships_player[4],all_ships_player[5]),(all_ships_player[6],
                        all_ships_player[7],all_ships_player[8], all_ships_player[9])]
    
    all_common_player_no_null = [i for i in all_ships_player if i in all_hits_player and i!=""]
    player_now_playing = fetched_results[8]
    #after the values have been set 
    #
    #ADDING ZERO HERE AS TO GET THE CORRECT NUMBERS
    #
    #
    
    
    
    
    if flag == 0:
        variable_dict = {"all_ships_player":all_ships_player, "all_hits_player":all_hits_player[0], "all_misses_player":all_misses_player[0], 
                         "all_ships_tuples":all_ships_tuples, "all_common_player_no_null":all_common_player_no_null, "player_now_playing":player_now_playing}
    
   #case of opponent
    else:
        variable_dict = {"all_ships_opponent":all_ships_player, "all_hits_opponent":all_hits_player[0], "all_misses_opponent":all_misses_player[0], 
                         "all_ships_opponents_tuples":all_ships_tuples, "all_common_opponent_no_null":all_common_player_no_null, "player_now_playing":player_now_playing}
    
    #returning a dict so as to access values with the key requested 
    return variable_dict
    
    
    
    
    
# "['', '31', '42', '52', '62', '32', '43', '53', '63', '72']"
def checking_ast(checking_input):
    #remove all the characters not needed
    try:
        pre_result = checking_input.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        result = list(pre_result.split(","))
    except:
        result = checking_input 
        if result=="":
            result=[]


    return result
    
    
    
    
#adding a flag to see if it is coloring a retrieve dbattle ot a new one , also if it is ongoing
def coloring(frame, all_ships_opponent, all_hits_opponent, all_misses_opponent, flag, j):
    
    all_hits_opponent_ = checking_ast(all_hits_opponent)
    all_misses_opponent_ = checking_ast(all_misses_opponent)
    #turn
    #print("all lists to color pre processing ", all_hits_opponent, type(all_hits_opponent),all_misses_opponent ,type(all_misses_opponent), all_ships_opponent)            
    #coloring the ships
    # flag == 0 then coloring at loadingy, battle not ended   ---- [i for i in all_ships]
    if flag==0:
        print("entering flag 0 in coloring, it is the palyers' turn, to color ", all_misses_opponent_, all_hits_opponent_)
        configure_all = [i.configure(bg="azure2") for i in frame.grid_slaves()]
        #print("entering the coloring 0 flag that should color all the already pressed buttons, ", "all_hits_opponent", all_hits_opponent_, "all misses opponent", all_misses_opponent_)
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_misses_opponent_]#[i for i in all_misses_opponent_]]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]#[i for i in all_hits_opponent_]]
        #print("went through with coloring flag == 0", all_hits_opponent_, all_misses_opponent_, len(all_misses_opponent_))
    #coloring when loading ended
    elif flag == 1:
        #all the buttons are colored , hits red, misses in gray
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] not in all_hits_opponent_]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]
    #at pressing when battle ongoing and hit
    elif flag==2:
        #check the format here 
        
             [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"]==j]
    elif flag==3:
        #here i have the case in which it is not the palyers' turn 
        print("entered flag 3", all_hits_opponent_, all_misses_opponent_)
        #configure_all = [i.configure(bg="azure2") for i in frame.grid_slaves()]
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in  all_misses_opponent_]#[i for i in all_misses_opponent_]]
        configure_ships_hits = [i.configure(bg="firebrick4", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]
        #coloring al the remeining colors 
        configure_rest_of_ships = [i.configure(bg="grey73", state=DISABLED) for i in frame.grid_slaves() if i["state"]!=DISABLED]#grey73
        #messagebox.showinfo("Not your turn", "Waiting for ove from other player")




#needs to write on the column chosen updating the field and nto deleting the values already there
# hit_or_misses can be all_misses or all_hits deopending on the case 

def write_hit_miss_update(column1, column2, value, id_of_battle, opponent_id, hit_or_misses, now_playing):
    #first selecting value and then updating and rewriting 
    #print("now playing in the write hit miss for the update of the db, should be the id of the user", now_playing[0], opponent_id)
    #
    #NEEDS TO BE A LIST EVERY TIME! after the first appends the folowing
    # ["['', '65', '75', '76', '66', '67']", '87']  with value 87
    #print("checking what i spassed with hits or misses ", type(hit_or_misses), hit_or_misses, value)
    #print("hit or misses in write hit or miss", hit_or_misses,type(hit_or_misses),list(hit_or_misses), value, type(value) )
    if hit_or_misses == "":
        hit_or_misses = []
    else:
        try:
                hit_or_misses = ast.literal_eval(hit_or_misses)
                #print("ast hit or misses --> ", hit_or_misses, value)
                hit_or_misses.append(value)
                #print("processing_ast")
                #print("higt or misses post appending", hit_or_misses)

        except:
                hit_or_misses.append(value)
            #print("processing normal string")

    #changing here !!! maye it is getting written twice 
    #hit_or_misses.append(value)

    #using already inserted to add 
    with sqlite3.connect(path_to_db) as conn:
        #setting the user_id equal to the opponent_id
        command = f"UPDATE Ships_1 SET {column1} = (?), {column2} = (?) WHERE battle_id = (?) AND user_id = (?)"
        #column passed in directly in teh function?
        #printing out teh values passd 
        #print("values passed on to the command  ",column,value,  type(value), type(id_of_battle), id_of_battle, type(opponent_id), opponent_id )
        #changing teh column in teh opponent battle
        adding = conn.execute(command, ( str(hit_or_misses),now_playing[0], id_of_battle[0], opponent_id ))
        #now changing the user part of the battle
        command = f"UPDATE Ships_1 SET {column2} = (?) WHERE battle_id = (?) AND user_id = (?)"
        adding = conn.execute(command, ( now_playing[0], id_of_battle[0], now_playing[0] ))
        print("in hit or misses ---> ",str(hit_or_misses), id_of_battle[0], opponent_id, "user_id=", now_playing[0], column1, column2)
        return hit_or_misses
    
#WHERE IS THIS TAKING FROM???

#assuming the js here are only the clickable buttons as the others are disabled 
#removing all hits and all misses so that it becomes dynamic 
def boom_trial(j, frame,  all_ships_opponent, id_opponent, id_of_battle, id_player):
    #checking if the button is present in the all_ships_list
    #creating j comma as i need to create a list
    j_comma  = j
    #CHANGED HERE SO IT IS DYNAMIC WITH THE THINGS TO GET
    #looking for updates in the lists all misses, all hits
    #getting the fetched battle
    fetched_result = fetching_the_battle(id_of_battle, id_opponent)
    result_opponent = processing_fetched_results(fetched_result, 0)
    # variable_dict = {"all_ships_opponent":all_ships_player, "all_hits_opponent":all_hits_player, "all_misses_opponent":all_misses_player, 
    #                     "all_ships_opponents_tuples":all_ships_tuples, "all_common_opponent_no_null":all_common_player_no_null}
    #
    #print("result opponent in the boom trial", result_opponent)
    if j in all_ships_opponent:
       
        #writing to hits here, neeed the id of the palyer now playing from his interface
        result_hit = write_hit_miss_update('hits','player_now_playing', j_comma , id_of_battle, id_opponent, result_opponent["all_hits_player"] , id_player)
        #coloring needs to be refreshed
        coloring(frame, all_ships_opponent, result_hit, result_opponent["all_misses_player"], 2, j)
    else:
        
        #writing to hits here, ALL HITS STILL STATIC
        result_miss = write_hit_miss_update('misses','player_now_playing', j_comma , id_of_battle, id_opponent,  result_opponent["all_misses_player"], id_player)
        #, nowwwwupdate sunk
        #what is what here??
        coloring(frame, all_ships_opponent,  result_opponent["all_hits_player"], result_miss, 3, j)
        

       
#here i need to design the different commands. checking if the pressed button is in the ships ones           

   
    

            
#needs id of th eplayer , user_id should be the one playing
def loading_battle(id_of_battle, user_id, flag, name):
    #what is it that i am passing 
    #this needs to return all teh needed info to be accessed by its name 
    fetching_positions = fetching_the_battle(id_of_battle, user_id[0])
    #if all ships are positioned for me then i can load the battle with no names and buttons
    #all values for the player
    result = processing_fetched_results(fetching_positions, 0)
   # need to get the opponent id here 
    id_opponent = getting_opponent_id_from_battle_id(id_of_battle[0], user_id)
    #print("opponent id in the loading battle --> ", id_opponent)
    fetching_positions_opponent = fetching_the_battle(id_of_battle, id_opponent)
    #getting results for opponent , flag 1 for opponent
    result_opponent = processing_fetched_results(fetching_positions_opponent, 1)
    #one of the two battles has ended
    #print("fetching_positions_player ", fetching_positions,"id_of_battle", id_of_battle,"user_id[0]" , user_id[0],
    #      "id_opponent ", id_opponent ," fetching_positions_opponent",  fetching_positions_opponent, "result_opponent", result_opponent, "now playing")
    if len(result_opponent['all_common_opponent_no_null'])==10:
        #print("entering opponent won")
    #opponent won
    #id_of_battle[2][0] --> opponent _name
    #all hits palyer shold show what i have hit in te opponent field 
        user_page_module.new_battle(id_of_battle[2][0], 2,result['all_hits_player'], result['all_misses_player'], id_opponent, id_of_battle, user_id)
        #base_window.title("Winner  of the battle is: " + id_of_battle[2][0])
    elif len(result['all_common_player_no_null'])==10:
        #print("entering player won")
        #player won
        user_page_module.new_battle(name[0], 2,result['all_hits_player'], result['all_misses_player'] ,
                                    result_opponent['all_ships_opponent'],  id_opponent, id_of_battle, user_id)
        #case of non ended game, just started or not started
    else:  
    #need to take into consideration here what happens when the turn is not right
        print("confrontation between the user ids:     ", user_id[0], type(user_id[0]), result["player_now_playing"], type(result["player_now_playing"]) )
        if user_id[0] == int(result["player_now_playing"]):
            print("user playing the same playing in db")
    #result opponent {'all_ships_opponent': ['21', '39', '29', '35', '25', '15', '76', '75', '74', '73'], 'all_hits_opponent': [''], 'all_misses_opponent': [''], 
    #'all_ships_opponents_tuples': [('21',), ('39', '29'), ('35', '25', '15'), ('76', '75', '74', '73')], 'all_common_opponent_no_null': []
    #result {'all_ships_player': ['21', '39', '29', '35', '25', '15', '76', '75', '74', '73'], 'all_hits_player': [''], 'all_misses_player': [''],
    #'all_ships_tuples': [('21',), ('39', '29'), ('35', '25', '15'), ('76', '75', '74', '73')], 'all_common_player_no_null': []}
    #"""
            # [[all_ships_player, all_hits_player, all_misses_player, all_ships_tuples, all_common_player_no_null] ]
            #(name, flag, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player)
            wid = user_page_module.new_battle(name[0], 1,result_opponent['all_hits_opponent'],result_opponent['all_misses_opponent'], result_opponent['all_ships_opponent'],
                                            id_opponent, id_of_battle, user_id)
            #print("entering battle still ongoing",result['all_hits_player'], result_opponent['all_hits_opponent'], result['all_misses_player'], result_opponent['all_misses_opponent'], 
            #      result_opponent['all_ships_opponent'],id_opponent, id_of_battle)
            #print("waht we are pasing to coloring", result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'])
            #coloring as it is ongoing
            coloring(wid, result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'], 3,"")
 
        else:
            print("user playing different from the one in db")
            wid = user_page_module.new_battle(name[0], 1,result_opponent['all_hits_opponent'],result_opponent['all_misses_opponent'], result_opponent['all_ships_opponent'],
                                            id_opponent, id_of_battle, user_id)
    #need probably to introduce a new instance in coloring to disable all the field , coloring darker grey the misses, dark grey the misses and light grey all the others
            coloring(wid, result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'], 0,"")
            pass










def retrieve_battle(name, frame, user_id):
    #print("user_id----------->    ", user_id)
    #need here to get the values of the battle back and get them displayed in a playable field
    #the battles need to be index in case there is more than one 
    #getting the battles, all the battle s of a player
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT * FROM Ships_1 WHERE  user_id = (?)"
        result_of_name_fetch = conn.execute(command, (str(*user_id)))
        fetching_the_result = result_of_name_fetch.fetchall()
        conn.commit()
    #print("fetching the result", fetching_the_result)
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
        #print("fetche ----->d", fetched)
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
                    

