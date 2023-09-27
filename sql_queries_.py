import sqlite3
import io 
from PIL import ImageTk,  ImageFont, ImageDraw
#this addresses some display issues when it comes ot the picture of the user
import PIL.Image
from tkinter import *
from tkinter import messagebox
import string
import sys , os
import ast
import time


path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"
translator = str.maketrans("","", string.punctuation)

#but2 = Button(root, text="button 2", command = lambda :  delete_widgets(root) )

def message_history(battle_id, frame):
    #getting the messages stored in the db as teh table
    with sqlite3.connect(path_to_db) as conn:
        # getting the messages from the table
        command = "SELECT messages FROM battle_table WHERE battle_id = (?)"
        # if no messages are found we return an empty string 
        result_of_battle_fetch = conn.execute(command, (str(battle_id[0]),))
        fetching_the_message =result_of_battle_fetch.fetchone()
        #cleaning from commas 
        fetching_the_message_ = (str(fetching_the_message).replace(")", "").replace("\"","").replace("(","").replace("'", "").replace(",", "").replace(":",",")).split("-")
        #replacing the : with a comma to create a tuple 
        #creating the tuples , by slicing each string
        fetching_the_message_tuples = [(i[0:1], i[1:]) for i in fetching_the_message_]
        print("fetching_the_message in the message history", fetching_the_message_tuples)
        if fetching_the_battle!="":
            #"[(1, adding first message),(2, adding second),(1, adding message),(2, adding reply),(1, adding message),(2, adding reply)]"
            processing = fetching_the_battle.replace("[", "").replace("]", "").replace(")", "").replace("(", "").split(",")
            processing_list = [((processing[i]).strip(), (processing[i+1]).strip()) for i in range(0,len(processing)-1,2)]
            #placing the widgets both on the right and left
            
            
            pass
        else:pass
        conn.commit()
    




def send_message_funct(text, battle_id, user_id):
    #getting the text of the widget 
    #adding here a semicolon so that the replace method is not compromised
    message = str(user_id[0])+":"+text.get("1.0", END).strip()
    if message!="":
        #register the message , not working here 
        with sqlite3.connect(path_to_db) as conn:
            command = f"SELECT messages FROM battle_table WHERE battle_id = (?)"
            result_of_history_fetched = conn.execute(command, (str(battle_id[0]),))
            result_of_history_fetched_ = result_of_history_fetched.fetchone()
            #cleaning the result 
            if result_of_history_fetched_ == ("",):
                result_of_history_fetched_= ""
                result_of_history_fetched_ = message + "-"  #i use here a separator that is not added directy  
            else:
                result_of_history_fetched_ = str(result_of_history_fetched_).replace("'", "").replace("(", "").replace(")", "").replace(",", "")  #('1,Second message',)
                result_of_history_fetched_ = str(result_of_history_fetched_) + message + "-"
            #updating the messages of the battle_table
            command = f"UPDATE battle_table SET messages = (?) WHERE battle_id = (?)"
            adding_message = conn.execute(command,  ( str(result_of_history_fetched_),  battle_id[0]))
        #saving the messsage to teh db, appending it in a list so that i can retrieve the single items 
        #opponent messages and my messages are on the same list in the battle_table
        #the id of the opponent and mine areused to place them either on the right side or the left
        #should be stored in a tuple as [(1,message),(2,reply),(1, message),(2,reply)]
         #setting the user_id equal to the opponent_id
         #updating the battle table so that i have all teh conversation in one plac
        #column passed in directly in teh function?
        #printing out teh values passd 
        #print("values passed on to the command  ",column,value,  type(value), type(id_of_battle), id_of_battle, type(opponent_id), opponent_id )
        #changing teh column in teh opponent battle
            conn.commit()
        text.delete("1.0","end")
        message_history(battle_id, "")   
            
            
            
        pass
    else:print("no message to displayu")
    






def delete_widgets(root):
    #need to check if there are any widgets
    if len(root.winfo_children())>0:
        [i.destroy() for i in root.winfo_children()]
    else:
        pass


def delete_widgets_access_previous(funct, *args):
    #calling the other screen , passing in some arguments 
    funct(args)


#refreshing_function 
def refresh(*args):

    
    while True:
    #need to account for ended games with a flag thatcan be all hits 
        
        
        
        
    #with args[0]=id_of_battle, args[1][0]=user_id[0]
    #fetching_positions = fetching_the_battle(args[0], args[1][0])
    #result = processing_fetched_results(fetching_positions, 0)
   # need to get the opponent id here 
        id_opponent = getting_opponent_id_from_battle_id(args[0][0], args[1])
    #print("opponent id in the loading battle --> ", id_opponent)
        fetching_positions_opponent = fetching_the_battle(args[0], id_opponent)
    #getting results for opponent , flag 1 for opponent
        result_opponent = processing_fetched_results(fetching_positions_opponent, 1)
    #after having checked the DB where i have written the new values i isolate the difference 
    # frame = args[2],
    # what differences i have here?
    #1) hits
    #2) misses 
    #the calculation is made with the colored buttons (they are colored with the 3 and 1 coloring colors )
    #
    # configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in  all_misses_opponent_]#[i for i in all_misses_opponent_]]
    # configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]
    #
    #WHEN I RETRIEVED IS ALREADY COLORED, SO I CAN JUST COLOR THE DIFFERENCE 
    #
    #
    #
    #
    
        diff_hit = [i for i in [str(i["text"]) for i in args[2].grid_slaves() if i["bg"]=="red"] if i not in result_opponent['all_hits_opponent']]
        diff_miss = [i for i in [str(i["text"]) for i in args[2].grid_slaves() if i["bg"]=="gray27"] if i not in result_opponent['all_misses_opponent']]
        #print("diff_miss, diff_hits    ", diff_miss, diff_hit, "all_hits_opponent",  result_opponent['all_hits_opponent'], "all_misses_opponent", result_opponent['all_misses_opponent'])
        #the two lists seem to be the same, i can now subtract the two and just get the difference not to color anything to avoid buffer effect
        #all_values_colored = diff_hit + diff_miss + result_opponent['all_hits_opponent'] +  result_opponent['all_misses_opponent']
        #all buttons that could be available
        #all disabled flag
        all_disabled = [str(i["text"]) for i in  args[2].grid_slaves() if i["state"]==DISABLED]
        #print("len all disabled", len(all_disabled))
        #all_able_buttons_after_addition = [str(i["text"]) for i in args[2].grid_slaves() if i not in [all_values_colored]]
        #not colored in  frame.grid_slaves, result[] are the updated values 
        #all_able_buttons_before_addition = [str(i["text"]) for i in args[2].grid_slaves(
        #it does nothing if the user id is the same as that of the player now playingz
        time.sleep(3)
        if len(result_opponent["all_hits_opponent"])==10:
            pass
        else:
            #print("result_opponent ------>     ", result_opponent)
        #here result or result opponent are the same, as we write in both when pressing
            if args[1][0] == int(result_opponent["player_now_playing"]):
                #in this case then also the difference is to be colored 
                if diff_miss!=[] and diff_hit!=[]:
                    #frame field as args[2], current user id is --> args[1][0]
                    #print("in refreshing, player different from the one that has played in db",  args[1][0] ,type(args[1][0]),
                    #      result_opponent["player_now_playing"], type(result_opponent["player_now_playing"]))
                    coloring(args[2], result_opponent['all_ships_opponent'],  diff_hit, diff_miss, 3,"")#result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent']
                else:pass
            else:
                #if needs to be loaded again
                if len(all_disabled)==100:
                    coloring(args[2], result_opponent['all_ships_opponent'],result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'],  0,"")# result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent']
                    if diff_miss!=[] and diff_hit!=[]:
                        coloring(args[2], result_opponent['all_ships_opponent'],diff_hit ,diff_miss,  0,"")# result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent']
                    else:
                        pass
                    #if i am waiting here i need to reenable everything not colored 
                else:
                    if diff_miss!=[] and diff_hit!=[]:
                        coloring(args[2], result_opponent['all_ships_opponent'],diff_hit ,diff_miss,  0,"")
                    else:pass
                    
                
            #print("in refreshing, player equal from the one that has played in db", args[1][0] ,result_opponent["player_now_playing"])
        #print("refreshed ", result_opponent["player_now_playing"], args[1][0])
    

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




def get_battle_name_from_id(id_):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT name FROM battle_table WHERE  battle_id = (?)"
        result_of_name_fetch = conn.execute(command, (id_))
        fetching_battle_name = result_of_name_fetch.fetchone()
        conn.commit()
        return fetching_battle_name
    
    
    
    pass



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
                        
#????????????????????????''             
#checking here if i have any picture loaded for a certain name 
#if none is found then we upload the default picture
def check_if_image(name):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT user_pic FROM users WHERE  name = (?)"
        img = conn.execute(command, (name,))
        #returns a tuple here
        photo_tuple = img.fetchone()
        print("photo tuple to check if the db has something", photo_tuple )
    if photo_tuple == None:
        img="download.png"
        empPhoto = convertToBinaryData(img)
        #here i update a different pic
        with sqlite3.connect(path_to_db) as conn:
            #needs changes in the query
                command = "UPDATE users SET user_pic = (?)  WHERE name = (?)"
                conn.execute(command, (empPhoto, name))
                conn.commit()  
        #need to add a default pic
    else:pass
       
            
#retrieving the image
def retrieve_image(name, current_window ):
    try:
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
        label_picture = Label( current_window, image = render, width=100, height=100)
                        #needs to be recalled here as well
        label_picture.image = render # keep a reference!
    except:
        image = PIL.Image.open(r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\download.png")
                        # convert the image : ata to file object
        render = ImageTk.PhotoImage(image)
                        #displaying it 
                        # Create a Label Widget to display the text or Image
        label_picture = Label( current_window, image = render, width=100, height=100)
                        #needs to be recalled here as well
        label_picture.image = render # keep a reference!
    #should i grid always in the same position so that i do not have any problems when using this in different screens 
    label_picture.grid(row=0, column=0)
    
 



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
        configure_all = [i.configure(bg="gray82", state=ACTIVE) for i in frame.grid_slaves()]
        
        #print("entering the coloring 0 flag that should color all the already pressed buttons, ", "all_hits_opponent", all_hits_opponent_, "all misses opponent", all_misses_opponent_)
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_misses_opponent_]#[i for i in all_misses_opponent_]]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]#[i for i in all_hits_opponent_]]
        #print("went through with coloring flag == 0", all_hits_opponent_, all_misses_opponent_, len(all_misses_opponent_))
    #coloring when loading, ended
    elif flag == 1:
        print("entering flag 1 battle anded ", all_misses_opponent_, all_hits_opponent_)
        #all the buttons are colored , hits red, misses in gray
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] not in all_hits_opponent_]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]
    #at pressing when battle ongoing and hit
    elif flag==2:
        #check the format here 
        #WHAT IS HAPPENING HERE ACTUALLY? IS THERE SOMETHING I NEED TO CHANGE HERE?  
        result = all_misses_opponent_ + all_hits_opponent_
        all_buttons_text = [i["text"] for i in frame.grid_slaves()]
        print("entering flag 2 in coloring, it is the palyers' turn, to color ", all_misses_opponent_, all_hits_opponent_, result, all_buttons_text)
        #all_to_color_lightly = [[i["text"] for i in frame.grid_slaves()].remove(i) for i in result]
        #configure_field_others = [i.configure(bg="grey81", state=DISABLED) for i in frame.grid_slaves() if i["text"] not in  all_to_color_lightly]
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_misses_opponent_]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]
        configure_field_others = [i.configure(bg="grey81", state=DISABLED) for i in frame.grid_slaves() if i["bg"] not in ["red", "gray27"]]
        
        
        
        
        
    elif flag==3:
        #here i have the case in which it is not the palyers' turn 
        print("entered flag 3 it is the other player' turn", all_hits_opponent_, all_misses_opponent_)
        #configure_all = [i.configure(bg="azure2") for i in frame.grid_slaves()]
        configure_field_pressed = [i.configure(bg="gray27", state=DISABLED) for i in frame.grid_slaves() if i["text"] in  all_misses_opponent_]#[i for i in all_misses_opponent_]]
        configure_ships_hits = [i.configure(bg="red", state=DISABLED) for i in frame.grid_slaves() if i["text"] in all_hits_opponent_]
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
        hit_or_misses=hit_or_misses
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
        
        #writing to misses here, ALL HITS STILL STATIC
        result_miss = write_hit_miss_update('misses','player_now_playing', j_comma , id_of_battle, id_opponent,  result_opponent["all_misses_player"], id_player)
        #, nowwwwupdate sunk
        #what is what here??
        coloring(frame, all_ships_opponent,  result_opponent["all_hits_player"], result_miss, 3, j)
        

       
#here i need to design the different commands. checking if the pressed button is in the ships ones           

   
    







                    

