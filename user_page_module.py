from tkinter import *
import sqlite3
import io
from tkinter import filedialog
#from retrieve_user_image import retrieve_image
from tkinter import messagebox
from sql_queries_ import  *
from checking_function import calculate_cases
#added for the function refresh
from sql_queries_ import refresh
import threading




def exit_root(root):
    root.destroy()
#this opens the image and displays it
def open(name, base_window):
    file = filedialog.askopenfilename(title='search images' , filetypes=(('png','*.png'),('jpeg', '*.jpg')))
    if file!= None:
        insert_image(file, name)
        retrieve_image(name, base_window)
    else:
        messagebox.showwarning("log_info", "wrong credentials")

#this will be make editable both the button of the picture and the text field 
def make_editable(text, button):
        text["state"] = NORMAL
        button["state"] = NORMAL

def update_name(new_name, name, toplevel):
    updated_name = (new_name.get("1.0", "end")).strip()
    #needs to update the name and show us a message 
    with sqlite3.connect(path_to_db) as conn:
            #needs changes in the query
            command = "UPDATE users SET name = (?)  WHERE name = (?)"
            conn.execute(command, (updated_name, name))
            conn.commit()
    toplevel.title(updated_name)
    messagebox.showinfo("update info", "Username successfully updated")







#need to be moved from here as it is not the 
#flag to differentiate between the creation field
#adding arguments to color in case battle has ended, jut one as we can differentialte the lists later
def create_field(frame, flag, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player):
    #print("all hits misses in create filed", all_hits, all_misses)
    #need to account also for ended games 
    if flag == 0:
        for i in range(10):
            for j in range(10):
                button = Button(frame, text=str(i)+str(j), command="")#lambda j=str(i)+str(j): check_hit(j)
                button.grid(row=i, column=j)
    elif flag == 1:
        #ongoing game
        for i in range(10):
            for j in range(10):
                button = Button(frame, text=str(i)+str(j), command=lambda j=str(i)+str(j): boom_trial(j,frame,  all_ships_opponent, id_opponent, id_of_battle, id_player))#lambda j=str(i)+str(j): check_hit(j)
                button.grid(row=i, column=j)
    elif flag == 2:
        for i in range(10):
            for j in range(10):
                button = Button(frame, text=str(i)+str(j))#lambda j=str(i)+str(j): check_hit(j)
                button.grid(row=i, column=j)
                #flag ==1 battle ended , j="" shouldn cause any damage
                coloring(frame, all_ships_opponent, all_hits, all_misses, 2, "")
        #need to color the buttons based on the hits and misses (misses dark gery and hits dark red)
        # coloring also the non presssed
        #not coloring as the battle has not started for this player
    else:
         for i in range(10):
            for j in range(10):
                button = Button(frame, text=str(i)+str(j))#lambda j=str(i)+str(j): check_hit(j)
                button.grid(row=i, column=j)
        
                #flag ==1 battle ended , j="" shouldn cause any damage

        


def new_battle(name, flag, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player, root, funct):
    print("deleting widgets new battle")
    #lambda arg=master: self.onclosing(arg)
    #caling the clean screen 
    
    
    
    
    
    
    root.protocol('WM_DELETE_WINDOW',lambda funct = delete_widgets, name=name, root=root, :  build_user_page(funct(root),  name, root))
    base_window = root
    frame_field = Frame(base_window)
    player_frame = Frame(base_window)
    base_window.title("New Battle of player : " + name )
    #frame_ships = Frame(base_window)
    #creating the buttons 
    frame_field.grid(row=0, column=0, padx=10, pady=10)
    #insert_battle_name, selected_option
    if flag==0:
        #empty arguments as new battle
            create_field(frame_field, 0, [], [],  all_ships_opponent, id_opponent, id_of_battle, id_player)
 
            player_frame.grid(row=0, column=1)
            #frame_ships.grid(row=1, column=1)new_battle
            label_opponent = Label(player_frame, text="Opponent", width=10)
            label_opponent.grid(row=1, column=0)
            #print("flag==0")
            label_name_battle = Label(player_frame, text="add a name for the battle", width=10)
            #need to get the users here, is it  alist
            #print("check users name ------------>",check_users(name))
            options = [""]+check_users(name)
            # create a variable to store the selected option
            selected_option = StringVar()
            # set the default option
            selected_option.set(options[0])
        # create the option menu widget
            option_menu = OptionMenu(player_frame, selected_option, *options)
            option_menu.grid(row=1, column=1)
            label_name_battle.grid(row=0, column=0)
            insert_battle_name = Text(player_frame, height=1, width=10)
            insert_battle_name.grid(row=0, column=1) 
                #the fieldswhere we have the buttons is the frame field
            ship_1 = Button(player_frame, text="ship 1", width=10, bg="orange")
            # rsettimng different values before lambda so we can have different for each button 
            ship_1.configure(command=lambda color="orange",frame = frame_field,  button=ship_1, : ship_click(color, frame, button, 1))
            ship_2 = Button(player_frame, text="ship 2", width=10, bg="blue")
            ship_2.configure(command=lambda color="blue",frame = frame_field,  button=ship_2, : ship_click(color, frame, button, 2))
            ship_3 = Button(player_frame, text="ship 3", width=10, bg="purple")
            ship_3.configure(command=lambda color="purple",frame = frame_field,  button=ship_3, : ship_click(color, frame, button, 3))
            
            ship_4 = Button(player_frame, text="ship 4", width=10, bg="pink")
            ship_4.configure(command=lambda color="pink",frame = frame_field,  button=ship_4, : ship_click(color, frame, button, 4))
            ship_1.grid(row=2, column=0, columnspan=2)
            ship_2.grid(row=3, column=0, columnspan=2)
            ship_3.grid(row=4, column=0, columnspan=2)
            ship_4.grid(row=5, column=0, columnspan=2)
    #in the save button i can pass the name as argument so that i get teh db save
    
    #save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(name, frame_field, insert_battle_name, selected_option))
    #save_button.grid(row=6, column=1, pady=(30,))
 


            #adding a flag here to skip creation in battle table , otherwise unique constarint error
            save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(base_window, name, frame_field, insert_battle_name, selected_option, 0))
            save_button.grid(row=6, column=1, pady=(30,))

            #creating the buttons 
    elif flag == 1:
            # empty arguments as the battle has not ended
            #print("all misses, all hits in new battle", all_hits, all_misses)
            create_field(frame_field, 1, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player)
            #print("flag==1")
            #with args[0]=id_of_battle, args[1][0]=user_id[0]
            #adding some threading part, not sure of what it does
            t = threading.Thread(target=lambda: refresh(id_of_battle, id_player, frame_field))
            t.daemon = True
            t.start()
            
            

    elif flag == 2:
        #ended game
            create_field(frame_field, 2, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player)
            #trying to return the widget so as to access it in loading
            #case in which i need to position the ships 
    else:
        #flag 3 for the buttons 
        #opponent opponent and battle name to be selected here 
        
        
        #id of battle -------------> (25, 'jjjjjj', ('Simona',))
        
        #phony variables here as they are not created or used in teh save battle operations 
 
        
        
        
        
        
        create_field(frame_field, 3, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player)
        player_frame.grid(row=0, column=1)
        #frame_ships.grid(row=1, column=1)
        label_opponent = Label(player_frame, text="Opponent", width=10)
        label_opponent.grid(row=1, column=0)
        label_opponent_name =  Label(player_frame,text=id_of_battle[2][0], width=10)
        label_opponent_name.grid(row=1, column=1)
        
        
        #print("flag==0")
        label_name_battle = Label(player_frame, text="name of battle", width=10)
        label_actual_name_battle =  Label(player_frame, text=id_of_battle[1], width=10)
        #need to get the users here, is it  alist
        #print("check users name ------------>",check_users(name))
        #options = [""]+check_users(name)
        # create a variable to store the selected option
        #selected_option = StringVar()
        # set the default option
        #selected_option.set(options[0])
    # create the option menu widget
        #option_menu = OptionMenu(player_frame, selected_option, *options)
        #option_menu.grid(row=1, column=1)
        
        
        
        label_name_battle.grid(row=0, column=0)
        label_actual_name_battle.grid(row=0, column=1)
        
        
        #overwriting the values 
        insert_battle_name = id_of_battle[1]
        selected_option = id_of_battle[2][0]
        
        
        
        
        #insert_battle_name = Label(text="" )
        #insert_battle_name.grid(row=0, column=1) 
            #the fieldswhere we have the buttons is the frame field
        ship_1 = Button(player_frame, text="ship 1", width=10, bg="orange")
        # rsettimng different values before lambda so we can have different for each button 
        ship_1.configure(command=lambda color="orange",frame = frame_field,  button=ship_1, : ship_click(color, frame, button, 1))
        ship_2 = Button(player_frame, text="ship 2", width=10, bg="blue")
        ship_2.configure(command=lambda color="blue",frame = frame_field,  button=ship_2, : ship_click(color, frame, button, 2))
        ship_3 = Button(player_frame, text="ship 3", width=10, bg="purple")
        ship_3.configure(command=lambda color="purple",frame = frame_field,  button=ship_3, : ship_click(color, frame, button, 3))
        
        ship_4 = Button(player_frame, text="ship 4", width=10, bg="pink")
        ship_4.configure(command=lambda color="pink",frame = frame_field,  button=ship_4, : ship_click(color, frame, button, 4))
        ship_1.grid(row=2, column=0, columnspan=2)
        ship_2.grid(row=3, column=0, columnspan=2)
        ship_3.grid(row=4, column=0, columnspan=2)
        ship_4.grid(row=5, column=0, columnspan=2)
#in the save button i can pass the name as argument so that i get teh db save

#save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(name, frame_field, insert_battle_name, selected_option))
#save_button.grid(row=6, column=1, pady=(30,))


        #print("what is passed to saved button ----> ",insert_battle_name, selected_option)
        #what is passed to saved button ---->  jjjjjj Simona
        #adding a flag here to skip creation in battle table , otherwise unique constarint error
        #leaving 
        save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(base_window, name, frame_field, insert_battle_name, selected_option, 1))
        save_button.grid(row=6, column=1, pady=(30,))
        
    root.protocol('WM_DELETE_WINDOW',lambda funct = delete_widgets, name=name, root=root, :  build_user_page(funct(root),  name, root))
    return frame_field
            

 
    

#button in grid 
def button_click(button_grid, color, total_ships, frame):#need to start adding here 
    #only accessed if the ships are not positioned 
    text = tuple(button_grid["text"])
    #print("text when pressing the button", text)
    x = int(text[1])
    y =  int(text[0])
    colors = ["orange", "blue", "purple", "pink"]
    #checks how many there are
    colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
    #print("secopnd time here should be the prevbioud button", colored_buttons)
    all_colored = [i["text"] for i in frame.grid_slaves() if i["bg"] in colors]
    #print("all colored buttons , if firts ok with nothing", all_colored)
    #print("colored_buttons", colored_buttons)
    #should keep the things as they are here to better index
    #getting the possible actions 
    #the below returns a list and a tuple 
    possible_actions =  calculate_cases(x, y,colored_buttons, all_colored, total_ships) 
    #lets see it printed 
    #print("possible actions + color", possible_actions, color)
    #diff  != 0 and list =[] cannot position
    diff = possible_actions[1]
    if diff !=0 and len(possible_actions[0]) == 0:
        messagebox.showerror("impossible to position", "cant find a suitable place please choose another spot")
        #case in which i can position
    elif diff !=0 and len(possible_actions[0]) != 0:
        text_str = str(y)+str(x)
        #print("text on the button", text_str)
        if text_str in possible_actions[0]:
            #print("ok button allowed")
            button_grid["bg"]=color 
            [i.config(state = DISABLED, bg="grey") for i in frame.grid_slaves() if i["text"] not in possible_actions[0] and i["text"] not in all_colored]
        else: print("not entering", possible_actions[0], type(possible_actions[0][0]))
    elif diff ==0 and len(possible_actions[0]) == 0:
        #case when we have finished the options
         button_grid["bg"]=color 
         #slightly cahnging the above
         #recalculating the all_colored
         colored_buttons_2 =   possible_actions[2]+ [button_grid["text"]]
    
         all_colored_total = all_colored + colored_buttons_2
         #print("all colored should be alll teh èpresssed", all_colored_total)
         [i.config(state = ACTIVE, bg="#f0f0f0", command="") for i in frame.grid_slaves() if i["text"] not in all_colored_total ]
        
        
    return None
    
        
    

#button of the ships
def ship_click(color, frame, button, total):
    #creates a list with all the colors 
    colors = ["orange", "blue", "purple", "pink"]
    #knows if there are any other buttons 
    colored_buttons = [i for i in frame.grid_slaves() if i["bg"] in colors]
    #color of the single button
    colored_buttons_specific = [i for i in frame.grid_slaves() if i["bg"]==color]
    #gets the total number of units
    total_ships = total
    #there are no other buttons 
    #print("all the buttons that are the same color clicked from the ships", colored_buttons_specific , color)
    if len(colored_buttons_specific) == 0:
    #needs here to add the button config attribute and add the other argumnets as well
    #configuring all of the buttons
        [i.config(state = ACTIVE, bg="#f0f0f0", command=lambda button_grid=i, color=color, total_ships=total_ships, frame=frame : button_click(button_grid, color, total_ships, frame)) for i in frame.grid_slaves() if i not in colored_buttons]
    else:
        #print("entering resetting")
        #i can truy to remove the color dinamically 
        #this should reset all the other buttons if not of the color 
        colors.remove(color)
        colored_buttons_removed_clicked = [i for i in frame.grid_slaves() if i["bg"] in colors]
        [i.config(state = ACTIVE, command="", bg="#f0f0f0") for i in frame.grid_slaves() if i not in colored_buttons_removed_clicked] 
        #changes the color of the buttons selected by our ship to reset

      









def build_modify_profile(name, root):
    base_window =root
    base_window.title("Profile detail : "+ name)
    label_username = Label(base_window, text="Name of the user")
    label_picture = Label(base_window,text="picture of the user")
    username = Text(base_window,height=1,width=10)
    username.insert("1.0", name)
    pic_to_change = Button(base_window,text="Select picture to change", command=lambda: open(name, base_window))
    #these two should stay as not editable until we press button
    pic_to_change["state"] = DISABLED 
    username.state = DISABLED
    button_edit = Button(base_window, text="edit", command=lambda: make_editable(username, pic_to_change))
    button_save_changes = Button(base_window, text="Save", command=lambda: update_name(username, name, base_window))
    #adding a default if none is present 
    check_if_image(name)
    #now i have to display the image here as well
    label_picture.grid(row=0, column=0)
    retrieve_image(name, base_window)
    pic_to_change.grid(row=2, column=0)
    #all the widgets in the second column 
    label_username.grid(row=0, column=1)
    username.grid(row=1, column=1)
    button_edit.grid(row=2, column=1)
    button_save_changes.grid(row=3, column=1)


    
def buld_champion_interface(root):
    base_window = root
    label_champions = Label(text="Player Classification")
    #GETTING ALL THE PLAYERS 
    



def SaveBattle(toplevel, name_creator, field, text, options, flag):
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
        #setting teh name and battle in case tyhe ships haven t been placed 
        
        try:
            selection_var = options.get().translate(translator)
            #the first is the name of the opponent while the second is the name of the battle
            name_opponent_and_battle = (selection_var + "  " +  text.get("1.0", "end")).split()

            #selection_var, name_opponent_and_battle   ---------> Silvia ['Silvia', 'ccccccccccccc']
        except:
            #inn  this case it is the name of battle and opponent 
            #['jjjjjj', 'Simona']
            name_opponent_and_battle = [options] + [text] 
            print("name opponent and battle in sql query ", name_opponent_and_battle)
            selection_var = text
        
        #here we pass the test if all the fields are filled and all the ships positioned 
        #need to check here for teh battle name 
        #needs to create the battle before we can save the data 
        #need to verify the condition here , once i have all the conditions i do not need also to create a new battle
        
        #checking ifd the ships are correclty placed
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
                                print("id fetchd ---->", id_fetched)
                                
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
    #needs to go back to the main window 
    #trying to call the closing window
    #object ev ent is not callable
    messagebox.showinfo("battle added", "battle added successfully")
    delete_widgets(toplevel)
    build_user_page("",  name_creator, toplevel)

    
def retrieving_battles(name, user_id, root, funct):
    print("name in retrieving battles", name)
    root.protocol('WM_DELETE_WINDOW',lambda funct = delete_widgets, name=name, root=root, :  build_user_page(funct(root),  name, root))
    base_window = root
    base_window.geometry("500x300")
    base_window.title("Battles of player : " + name )
    #need to create the buttons with the commands to create teh buttons 
    #need to add a scrolalble frame here

    #initializing frame
    frame_buttons = Frame(base_window)
    #adding some propertiees 
    frame_buttons.pack(expand=True, fill=BOTH) #.grddddid(row=0,column=0)
    #canvas created and added to frame
    canvas=Canvas(frame_buttons,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
    bar=Scrollbar(frame_buttons,orient=VERTICAL)
    bar.pack(side=RIGHT,fill=Y)
    bar.config(command=canvas.yview)
    canvas.config(width=50,height=300)
    canvas.config(yscrollcommand=bar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    frame_buttons_1 = Frame(base_window, padx = 10)
    canvas.create_window(0, 0, anchor='nw', window=frame_buttons_1)
    #retrieve_battle(name, frame, user_id, root, funct)
    print("user_id   -->", user_id)
    retrieve_battle(name, frame_buttons_1, user_id, root, funct)
    pass


def build_user_page(funct,  name, root):
    user_id = getting_user_id_from_name(name)
    base_window= root
    print("root", root, "name in build user page", name)
    base_window.geometry("500x300")
    base_window.title("Military Base : " + name )
    frame_pic = Frame(base_window)
    frame_buttons = Frame(base_window)
    frame_pic.grid(row=0, column=0)
    frame_buttons.grid(row=0, column=1)
    label_player_name = Label(frame_pic, text=name, width=7, padx=(70, ))
    #retrieve_image(name)
    #funct is the delete widgets at calling, needs to be different here
    button_new_battle = Button(frame_buttons, text="new battle",width=15, height=2,bg="red", command =lambda: new_battle(name, 0, "", "", "", "", "","", root, delete_widgets(root)))
    button_old_battles = Button(frame_buttons, text="show battles",width=15, height=2,bg="red", command=lambda: retrieving_battles(name, user_id, root, delete_widgets(root)))
    button_show_champions = Button(frame_buttons, text="show champions",width=15, height=2,bg="red", command="")
    button_change_profile = Button(frame_buttons, text="change profile",width=15, height=2,bg="red", command=lambda: build_modify_profile(name, root))
    
    label_player_name.grid(row=0, column=0)
    button_new_battle.grid(row=0, column=0,padx=(150,10), pady=20)
    button_old_battles.grid(row=1, column=0,padx=(150,10), pady=10 )
    button_show_champions.grid(row=2, column=0,padx=(150,10), pady=10)
    button_change_profile.grid(row=3, column=0,padx=(150,10), pady=10)
    #exiting last window
    root.protocol('WM_DELETE_WINDOW',lambda : exit_root(root))
    
def retrieve_battle(name, frame, user_id, root, funct):
    print("name in retrieve battles", name)
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
        button = Button(frame, text=battle_names[i],width=60, height=5, padx=20, pady=3,bg="orange", 
                        
                        command=lambda f=(fetching_the_result[i][0],battle_names[i],opponent_current_battle): loading_battle(f , user_id, 0, name, root, delete_widgets(root)))
        # attach Text widget to root window at top
        button.pack()#side=TOP, fill=X)#.grid(row=i, column=0)
    pass   


            
#needs id of th eplayer , user_id should be the one playing
def loading_battle(id_of_battle, user_id, flag, name, root, funct):
    print("name in loading battle", name)
    print("funct   -> ", funct)
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
    #print("why the algorithm is not working at the moment ----->", result_opponent, "result ----->",  result)
    #taken into account when the player has no ships placed , should load the full field (maybe save should close the field)
    #needs result as the result is ships of the current player 
    print("result ------------------>", len([i for i in result["all_ships_player"] if i!=""]))
    if len([i for i in result["all_ships_player"] if i!=""])<10:
        
        #if no partial positioning is possible thanks to the save button 
        #zero a s flag as it is a new battle
       new_battle(name, 3, [], [],  result_opponent["all_ships_opponent"], id_opponent, id_of_battle, user_id[0], root, delete_widgets(root))
        
        
        
    else:
        if len(checking_ast(result_opponent['all_hits_opponent']))==10 or len(checking_ast(result['all_hits_player']))==10:        
            #print("entering opponent won")
        #opponent won
        #id_of_battle[2][0] --> opponent _name
        #all hits palyer shold show what i have hit in te opponent field 
        #    print("ONE OF THE BATTLES HAS ENEDED FOR SURE")
        #COMMENTING OUT
        
        
        

        
            new_battle(id_of_battle[2][0], 2,result['all_hits_player'], result['all_misses_player'],result_opponent['all_ships_opponent'],  id_opponent, id_of_battle, user_id, root, delete_widgets(root))
            #base_window.title("Winner  of the battle is: " + id_of_battle[2][0])
        #elif len(result['all_common_player_no_null'])==10:
            #print("entering player won")
            #player won
            #user_page_module.new_battle(name[0], 2,result['all_hits_player'], result['all_misses_player'] ,
            #                            result_opponent['all_ships_opponent'],  id_opponent, id_of_battle, user_id)
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
                wid = new_battle(name, 1,result_opponent['all_hits_opponent'],result_opponent['all_misses_opponent'], result_opponent['all_ships_opponent'],
                                                id_opponent, id_of_battle, user_id, root, delete_widgets(root))
                #print("entering battle still ongoing",result['all_hits_player'], result_opponent['all_hits_opponent'], result['all_misses_player'], result_opponent['all_misses_opponent'], 
                #      result_opponent['all_ships_opponent'],id_opponent, id_of_battle)
                #print("waht we are pasing to coloring", result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'])
                #coloring as it is ongoing
                coloring(wid, result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'], 3,"")
    
            else:
                print("user playing different from the one in db")
                wid = new_battle(name, 1,result_opponent['all_hits_opponent'],result_opponent['all_misses_opponent'], result_opponent['all_ships_opponent'],
                                                id_opponent, id_of_battle, user_id, root, delete_widgets(root))
        #need probably to introduce a new instance in coloring to disable all the field , coloring darker grey the misses, dark grey the misses and light grey all the others
                coloring(wid, result_opponent['all_ships_opponent'], result_opponent['all_hits_opponent'], result_opponent['all_misses_opponent'], 0,"")
                pass
        



