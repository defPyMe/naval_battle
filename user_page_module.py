from tkinter import *
import sqlite3
import io
from tkinter import filedialog
#from retrieve_user_image import retrieve_image
from tkinter import messagebox

from sql_queries_ import  retrieve_image, check_if_image, path_to_db, check_users, SaveBattle, retrieve_battle, insert_image, getting_user_id_from_name
from checking_function import calculate_cases

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



def update(window):
    print("refresh!!!!!!")
    #window.after(5000, lambda: update(window))






    
    


#need to be moved from here as it is not the 
def create_field(frame):
    for i in range(10):
        for j in range(10):
            button = Button(frame, text=str(i)+str(j), command="")#lambda j=str(i)+str(j): check_hit(j)
            button.grid(row=i, column=j)



def new_battle(name, flag, battle_name, opponent_name):
    base_window = Toplevel()
    frame_field = Frame(base_window)
    player_frame = Frame(base_window)
    base_window.title("New Battle of player : " + name )
    #frame_ships = Frame(base_window)
    #creating the buttons 
    create_field(frame_field)
    frame_field.grid(row=0, column=0, padx=10, pady=10)
    player_frame.grid(row=0, column=1)
    #frame_ships.grid(row=1, column=1)
    label_opponent = Label(player_frame, text="Opponent", width=10)
    label_opponent.grid(row=1, column=0)
    #insert_battle_name, selected_option
    if flag==0:
            print("flag==0")
            label_name_battle = Label(player_frame, text="add a name for the battle", width=10)
            #need to get the users here, is it  alist
            options = [""]+[check_users(name)]
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
            save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(name, frame_field, insert_battle_name, selected_option))
            save_button.grid(row=6, column=1, pady=(30,))

            #creating the buttons 
    else:
            print("flag==1")
            selected_option = StringVar(value=opponent_name)
            # set the default option
            #getting the option menu but with then default value onluy , if one it should be ok as we can only select one
            option_menu = OptionMenu(player_frame, selected_option, value=opponent_name)
            option_menu.grid(row=1, column=1)
            
            #label of name
            label_name_battle = Label(player_frame, text="battle name", width=10)
            label_name_battle.grid(row=0, column=0)
            #actual value for battle name
            
            
            insert_battle_name = Text(player_frame, height=1, width=10)
            insert_battle_name.grid(row=0, column=1) 
            #actual value, label is ok by default
            default_text = battle_name 
            insert_battle_name.insert(END, default_text)

# Disable the Text widget
            insert_battle_name.configure(state='disabled')
            

            #CAN T GET TH EVALUE AS IT IS NOT A TEXT FIELD ANYMORE!!
            save_button = Button(player_frame, text="Save", bg="green", command=lambda: SaveBattle(name, frame_field, insert_battle_name, selected_option))
            save_button.grid(row=6, column=1, pady=(30,))
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
 
    pass

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
        print("entering resetting")
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
    frame_buttons = Frame(base_window)
    frame_buttons.grid(row=0, column=0)
    retrieve_battle(name, frame_buttons, user_id)
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
    button_new_battle = Button(frame_buttons, text="new battle",width=15, height=2,bg="red", command =lambda: new_battle(name, 0, "", ""))
    button_old_battles = Button(frame_buttons, text="show old battles",width=15, height=2,bg="red", command=lambda: retrieving_battles(name, user_id))
    button_show_champions = Button(frame_buttons, text="show champions",width=15, height=2,bg="red", command="")
    button_change_profile = Button(frame_buttons, text="change profile",width=15, height=2,bg="red", command=lambda: build_modify_profile(name))
    
    label_player_name.grid(row=0, column=0)
    button_new_battle.grid(row=0, column=0,padx=(150,10), pady=20)
    button_old_battles.grid(row=1, column=0,padx=(150,10), pady=10 )
    button_show_champions.grid(row=2, column=0,padx=(150,10), pady=10)
    button_change_profile.grid(row=3, column=0,padx=(150,10), pady=10)
    update(base_window)
    