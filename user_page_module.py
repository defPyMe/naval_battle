from tkinter import *
import sqlite3
import io
from tkinter import filedialog
#from retrieve_user_image import retrieve_image
from tkinter import messagebox
from sql_queries_ import  (retrieve_image, check_if_image, path_to_db, check_users, SaveBattle,
                            retrieve_battle, insert_image, getting_user_id_from_name,
                                boom_trial, coloring, getting_name_from_id, get_battle_name_from_id)
from checking_function import calculate_cases
#added for the function refresh
from sql_queries_ import refresh
import threading


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


#initialize both the arguments with a function and then display only the correct one
def create_attributes():
    label_opponent = Label(args[0], text="Opponent", width=10)
    
    
    
    pass



#player_frame, name, frame_field,  label_name_battle ="" 
def create_interface_field(*args):#args[0] = player_frame, args[1]=name, args[2]=label_name_battle, 
        args[0].grid(row=0, column=1)
            #frame_ships.grid(row=1, column=1)
        label_opponent = Label(args[0], text="Opponent", width=10)
        label_opponent.grid(row=1, column=0)
        #print("flag==0")
        label_name_battle = Label(args[0], text="add a name for the battle", width=10)
        #need to get the users here is it  alist
        #print("check users name ------------>",check_users(name))
        options = [""]+check_users(args[1])
        # create a variable to store the selected option
        selected_option = StringVar()
        # set the default option
        selected_option.set(options[0])
    # create the option menu widget
        option_menu = OptionMenu(args[0], selected_option, *options)
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
        save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(name, frame_field, insert_battle_name, selected_option, 0))
        save_button.grid(row=6, column=1, pady=(30,))
    
    
        pass


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

        


def new_battle(name, flag, all_hits, all_misses,  all_ships_opponent, id_opponent, id_of_battle, id_player):
    base_window = Toplevel()
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
            #frame_ships.grid(row=1, column=1)
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

      









def build_modify_profile(name):
    base_window = Toplevel()
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


    
def buld_champion_interface():
    base_window = Toplevel()
    label_champions = Label(text="Player Classification")
    #GETTING ALL THE PLAYERS 
    
    
    
def retrieving_battles(name, user_id):
    base_window = Toplevel()
    base_window.geometry("500x300")
    base_window.title("Battles of player : " + name )
    #need to create the buttons with the commands to create teh buttons 
    #need to add a scrolalble frame here
    """
    
            container = Frame(new_window, width = 10, height = 10)
        
        canvas = Canvas(container)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
             lambda e: canvas.configure(
              scrollregion=canvas.bbox("all")
             )
            )

        
        # adding all to the interface 
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
       
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    
    
    
    """
    #initializing frame
    frame_buttons = Frame(base_window)
    #adding some propertiees 
    frame_buttons.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
    #canvas created and added to frame
    canvas=Canvas(frame_buttons,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
    bar=Scrollbar(frame_buttons,orient=VERTICAL)
    bar.pack(side=RIGHT,fill=Y)
    bar.config(command=canvas.yview)
    canvas.config(width=50,height=300)
    canvas.config(yscrollcommand=bar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
   
    frame_buttons_1 = Frame(base_window)
   
    canvas.create_window(0, 0, anchor='nw', window=frame_buttons_1)
   
   
    
    
    
    """
    h = Scrollbar(base_window, orient = 'horizontal')
    # attach Scrollbar to root window at
    # the bootom
    h.pack(side = BOTTOM, fill = X)
    # create a vertical scrollbar-no need
        # to write orient as it is by
        # default vertical
    v = Scrollbar(base_window)
    v.pack(side = RIGHT, fill = Y)
    #widget where the buttons will be stored
    # here xscrollcomannd is used to attach Frame
        # widget to the horizontal scrollbar
        # here yscrollcomannd is used to attach Frame
        # widget to the vertical scrollbar
    frame_buttons = Frame(base_window, xscrollcommand = h.set,
                 yscrollcommand = v.set)
    # attach Frame widget to root window at top
    frame_buttons.pack(side=TOP, fill=X)
    h.config(command=frame_buttons.xview)
  
        # here command represents the method to
        # be executed yview is executed on
        # object 't' Here t may represent any
        # widget
    v.config(command=frame_buttons.yview)"""
    
    
    retrieve_battle(name, frame_buttons_1, user_id)
    pass


def build_user_page(name):
    user_id = getting_user_id_from_name(name)
    base_window = Toplevel()
    base_window.geometry("500x300")
    base_window.title("Military Base : " + name )
    frame_pic = Frame(base_window)
    frame_buttons = Frame(base_window)
    frame_pic.grid(row=0, column=0)
    frame_buttons.grid(row=0, column=1)
    label_player_name = Label(frame_pic, text=name, width=7, padx=(70, ))
    #retrieve_image(name)
    button_new_battle = Button(frame_buttons, text="new battle",width=15, height=2,bg="red", command =lambda: new_battle(name, 0, "", "", "", "", "",""))
    button_old_battles = Button(frame_buttons, text="show battles",width=15, height=2,bg="red", command=lambda: retrieving_battles(name, user_id))
    button_show_champions = Button(frame_buttons, text="show champions",width=15, height=2,bg="red", command="")
    button_change_profile = Button(frame_buttons, text="change profile",width=15, height=2,bg="red", command=lambda: build_modify_profile(name))
    
    label_player_name.grid(row=0, column=0)
    button_new_battle.grid(row=0, column=0,padx=(150,10), pady=20)
    button_old_battles.grid(row=1, column=0,padx=(150,10), pady=10 )
    button_show_champions.grid(row=2, column=0,padx=(150,10), pady=10)
    button_change_profile.grid(row=3, column=0,padx=(150,10), pady=10)
    
    