from tkinter import *
import sqlite3
import io
from tkinter import filedialog
#from retrieve_user_image import retrieve_image
from sql_queries import insert_image, retrieve_image, check_if_image, path_to_db, check_users
from tkinter import messagebox


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

def new_battle(name):
    base_window = Toplevel()
    frame_field = Frame(base_window)
    player_frame = Frame(base_window)
    #frame_ships = Frame(base_window)
    #creating the buttons 
    create_field(frame_field)
    frame_field.grid(row=0, column=0, padx=10, pady=10)
    player_frame.grid(row=0, column=1)
    #frame_ships.grid(row=1, column=1)
    label_opponent = Label(player_frame, text="Opponent", width=10)
    label_name_battle = Label(player_frame, text="add a name for the battle", width=10)
    insert_battle_name = Text(player_frame, height=1, width=10)
    #need to get the users here, is it  alist
    options = [""]+[check_users(name)]
    # create a variable to store the selected option
    selected_option = StringVar()
    # set the default option
    selected_option.set(options[0])
# create the option menu widget
    option_menu = OptionMenu(player_frame, selected_option, *options)
    label_name_battle.grid(row=0, column=0)
    insert_battle_name.grid(row=0, column=1) 
    label_opponent.grid(row=1, column=0)
    option_menu.grid(row=1, column=1)
    #creating the buttons 
    #the fieldswhere we have the buttons is the frame field
    ship_1 = Button(player_frame, text="ship 1", width=10, bg="orange")
    # ret
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
    save_button = Button(player_frame, text="Save", bg="green", command="")
    save_button.grid(row=6, column=1, pady=(30,))

def create_field(frame):
    for i in range(10):
        for j in range(10):
            button = Button(frame, text=str(i)+str(j), command="")
            button.grid(row=i, column=j)

def calculate_cases(x, y,colored_buttons_singular, all_colored, total_ships):
    #need to add here the cases where the colored are more than one or one 
    #needs to take into account the x and y to see how to position
    #where to put this?????
    #will be at least one.
    print("x,y in the ==1 function", x,y)
        #generating the list of numbers
    all_values_allowed = [i for i in range(0, 11)]
    #all buttons need to be only the single colored buttons
    if len(colored_buttons_singular) == 1 and len(colored_buttons_singular) < total_ships:
        print("case of len colored buttons ==1 ")
        #one already positioned
        diff = total_ships - 1
        #creating a list of all the buttons that are possible on the x
        all_x = [(str(int(x+i))+str(y)) for i in range (-diff, diff+1) if x+i in all_values_allowed]
        #do the same for y, getting here a list so we just pass it below --> should be something like ['46', '57', '48', '37', '47']
        all_y = [(str(x) + str(int(y+i))) for i in range (-diff, diff+1) if y+i in all_values_allowed]
        print("all_x, all_y in the len==1 option", all_x, all_y)
        #needs to check here if there is teh possibility to go all teh way, checking the buttons that are already present 
        trying_x = [i for i in all_x if i in all_colored]
        #checking if the buttons are in the colored ones 
        trying_y = [i for i in all_y if i in all_colored]
        print("trying x and trying y to see which one i higher in the first function", trying_x, trying_y)
        if len(trying_x) == 0 and len(trying_y) !=0:#case of x
            print("entering trying_x == 0 and trying_y !=0")
            #returning the all_x list, should be something we can pass
            cases_list_str = all_x
        elif len(trying_x) != 0 and len(trying_y) ==0:#case of y
            print("trying_x != 0 and trying_y ==0")
            cases_list_str = all_y
        elif len(trying_x) != 0 and len(trying_y) !=0: #impossible to position
            print("trying_x != 0 and trying_y !=0")
            cases_list_str = []
        elif len(trying_x) == 0 and len(trying_y) == 0:#coast is clear
             
            print("entering cosat is clear")
            all_values = all_x + all_y 
            cases_list_str = list(set(all_values ))
        print("all cases tr in the > 1 function", cases_list_str)
    elif len(colored_buttons_singular) > 1 and len(colored_buttons_singular) < total_ships: #case in which we have more than one button of the same color 
        #changing the diff as we have more buttons here
        diff = total_ships - len(colored_buttons_singular)
        print("entering the second option where len > 1, printing diff, ",diff )
        all_current_ships_values = [i["text"] for i in colored_buttons_singular]
        if all_current_ships_values[0][:1] == all_current_ships_values[1][:1]: #case of x so that the ship is horizontal
            #here i should have to try only for teh case of x to see if we can get the values 
            all_x_right = [(str(int(x+i))+str(y)) for i in range ( diff+1) if x+i in all_values_allowed]
            #i cannot have the -diff in range, need tp act on the sum
            all_x_left = [(str(int(x-i))+str(y)) for i in range (diff) if x+i in all_values_allowed]
            print("printing all_x_eft, all_x_right in the len() > 1",all_x_left, all_x_right )
            #need to get a left or right difference here to avoid overlap
            trying_x_left = [i for i in all_x_left if i in all_colored]
            trying_x_right = [i for i in all_x_right if i in all_colored]
            print("printing trying_x_left, trying_x_right in the len() > 1",trying_x_left, trying_x_right )
            if len(trying_x_left) == 0 and len(trying_x_right) !=0:#case of x
            #returning the all_x list, should be something we can pass
                cases_list_str = all_x_left
            elif len(trying_x_left) != 0 and len(trying_x_right) ==0:#case of y
                cases_list_str = all_x_right
            elif len(trying_x_left) != 0 and len(trying_x_right) !=0: #impossible to position
                cases_list_str = []
            elif len(trying_x_left) == 0 and len(trying_x_right) ==0:#coast is clear 
                cases_list_str =  all_x_left + all_x_right
        else:#case of y
            all_y_down = [(x+str(int(y)+i)) for i in range ( diff+1) if y+i in all_values_allowed]
            #i cannot have the -diff in range, need tp act on the sum
            all_y_up = [(x+str(int(y)-i)) for i in range (diff) if y-i in all_values_allowed]
            trying_y_down = [i for i in all_y_down if i in all_colored]
            #getting the difference 
            trying_y_up = [i for i in all_y_up if i in all_colored]
            if len(trying_y_down) == 0 and len(trying_y_up) !=0:#case of x
            #returning the all_x list, should be something we can pass
                cases_list_str = all_y_down
            elif  len(trying_y_down) != 0 and len(trying_y_up) ==0:#case of y
                cases_list_str = all_y_up
            elif len(trying_y_down) != 0 and len(trying_y_up) !=0: #impossible to position
                cases_list_str = []
            elif  len(trying_y_down) == 0 and len(trying_y_up) ==0:#coast is clear 
                cases_list_str=  all_y_up + all_y_down 
    elif len(colored_buttons_singular) == total_ships:
        cases_list_str = []
                 

    
    
    
    
    
    
    
    
    
    
    
    
    #if len(colored_buttons)==1:
        #all_cases = {(x, y-1): (bool(y-1>0)),  (x+1, y): (bool(x+1<10)), (x, y+1):(bool(y+1<10)), (x-1, y):(bool(x-1>0))}
        #cases = {key: value for key, value in all_cases.items() if value == True}
        #cases_list = [i for i in cases.keys()]
        #cases_list_str = [(str(x)+str(y)) for x, y in cases_list]
    #else:
        #gettinmg if we are talking about an x or a y
        #checking only the forst element and then procee
        #missing a part here where we check if we are x or y
        #texts = []
        #first_element = [int(i["text"][0]) for i in colored_buttons]#all_x
        #second_element = [int(i["text"][1]) for i in colored_buttons]#all_y
        #zipped_function = [(i["text"][0])for i in colored_buttons]
        #print("first_element", "second_element", first_element, second_element, zipped_function)
        
        #if zipped_function[0][:1]==zipped_function[1][:1]:#case of y changing
            
            
        #    min_all_y = min(second_element)
        #    cases_list_str = [(str(first_element[0])+str(i)) for i in range(min_all_y,total)]
        #else:
            #doing the x part
            #min_all_x = min(first_element)
            #cases_list_str = [(str(i)+str(second_element[0])) for i in range(min_all_x,total)]
    return cases_list_str

#need to  add a new function to check the multiple button cases 



#button in grid 
def button_click(button_grid, color, total_ships, frame):#need to start adding here 
    #only accessed if the ships are not positioned 
    text = tuple(button_grid["text"])
    x = int(text[0])
    y =  int(text[1])
    colors = ["orange", "blue", "purple", "pink"]
    #checks how many there are
    colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
    all_colored = [i["text"] for i in frame.grid_slaves() if i["bg"] in colors]
    #should keep the things as they are here to better index

    if len(colored_buttons) < total_ships:
    #cases in which we have no colored buttons 
        if len(colored_buttons)==0:
        #print("possinle_options",possible_actions)
            button_grid["bg"]=color
        #NEEDS TO BE THE ALL COLORS
            colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
        #NEEDS COMPREHENSIVE CHECKING HERE
        
        
        
        
            possible_actions =  calculate_cases(x, y,colored_buttons, all_colored, total_ships) 
        #adding the pressed button to make it colored 
            possible_actions.append(str(button_grid["text"]))
            print("possible actions", possible_actions)
            [i.config(state = DISABLED, bg="grey") for i in frame.grid_slaves() if i["text"] not in possible_actions]
        
        
        elif len(colored_buttons)>=1:
            button_grid["bg"]=color
        #needs to be recalculated here 
            colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
            possible_actions = calculate_cases(x, y,colored_buttons,all_colored,  total_ships)
        #if the max has been reached we recolor all but the blue ones and reset the command 
            print("possible actions second button", possible_actions)
            if len(colored_buttons)==total_ships:
                [i.config(state = ACTIVE, bg="#f0f0f0", command="") for i in frame.grid_slaves() if i["bg"]!=color]
            else:
                pass
    else:
        #case in which we are at the level of ships
        #this should reset all the other buttons if not of the color 

        #knows if there are any other buttons 
        colored_buttons = [i for i in frame.grid_slaves() if i["bg"] in colors]      
        [i.config(command="", bg="#f0f0f0") for i in frame.grid_slaves() if i not in colored_buttons ] 
        
        
        
        
        #[(3, 7), (4, 8), (3, 9), (2, 8)]
        #colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
        #all_buttons = [tuple((i["text"])) for i in frame.grid_slaves()]
        #print("all_buttons_text", all_buttons)
        #now i need to disable the buttons
        #[i.config(state = DISABLED, bg="grey") for i in frame.grid_slaves() if ((int(x), int(y)) for x, y in tuple(i["text"])) not in possible_actions.keys ]
        
        
    

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
    if len(colored_buttons_specific) == 0:
    #needs here to add the button config attribute and add the other argumnets as well
    #configuring all of the buttons
        [i.config(command=lambda button_grid=i, color=color, total_ships=total_ships, frame=frame : button_click(button_grid, color, total_ships, frame)) for i in frame.grid_slaves()]
    else:
        #this should reset all the other buttons if not of the color 
        [i.config(command="", bg="#f0f0f0") for i in frame.grid_slaves() if i not in colored_buttons ] 
        #changes the color of the buttons selected by our ship to reset
        [i.config(command="", bg="#f0f0f0") for i in frame.grid_slaves() if i["bg"]==color] 

      









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
    
    

def build_user_page(name):
   
    base_window = Toplevel()
    base_window.geometry("500x300")
    base_window.title("Military Base : " + name )
    frame_pic = Frame(base_window)
    frame_buttons = Frame(base_window)
    frame_pic.grid(row=0, column=0)
    frame_buttons.grid(row=0, column=1)
    label_player_name = Label(frame_pic, text=name, width=7, padx=(70, ))
    #retrieve_image(name)
    button_new_battle = Button(frame_buttons, text="new battle",width=15, height=2,bg="red", command =lambda: new_battle(name))
    button_old_battles = Button(frame_buttons, text="show old battles",width=15, height=2,bg="red", command="")
    button_show_champions = Button(frame_buttons, text="show champions",width=15, height=2,bg="red", command="")
    button_change_profile = Button(frame_buttons, text="change profile",width=15, height=2,bg="red", command=lambda: build_modify_profile(name))
    
    label_player_name.grid(row=0, column=0)
    button_new_battle.grid(row=0, column=0,padx=(150,10), pady=20)
    button_old_battles.grid(row=1, column=0,padx=(150,10), pady=10 )
    button_show_champions.grid(row=2, column=0,padx=(150,10), pady=10)
    button_change_profile.grid(row=3, column=0,padx=(150,10), pady=10)
    