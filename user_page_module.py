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
    ship_1.configure(command=lambda color="orange",frame = frame_field,  button=ship_1, : ship_click(color, frame, button))
    ship_2 = Button(player_frame, text="ship 2", width=10, bg="blue")
    ship_2.configure(command=lambda color="blue",frame = frame_field,  button=ship_2, : ship_click(color, frame, button))
    ship_3 = Button(player_frame, text="ship 3", width=10, bg="purple")
    ship_3.configure(command=lambda color="purple",frame = frame_field,  button=ship_3, : ship_click(color, frame, button))
    
    ship_4 = Button(player_frame, text="ship 4", width=10, bg="pink")
    ship_4.configure(command=lambda color="pink",frame = frame_field,  button=ship_4, : ship_click(color, frame, button))
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

def calculate_cases(x, y):
    all_cases = {(x, y-1): (bool(y-1>0)),  (x+1, y): (bool(x+1<10)), (x, y+1):(bool(y+1<10)), (x-1, y):(bool(x-1>0))}
    cases = {key: value for key, value in all_cases.items() if value == True}
    cases_list = [i for i in cases.keys()]
    cases_list_str = [(str(x), str(y)) for x, y in cases_list]
    return cases_list_str

#button in grid 
def button_click(button_grid, color, total_ships, frame):#need to start adding here 
    text = tuple(button_grid["text"])
    x = int(text[0])
    y =  int(text[1])
    possible_actions =  calculate_cases(x, y)
    colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
    #should keep the things as they are here to better index
    all_buttons = [i["text"] for i in frame.grid_slaves()]
    #cases in which we have no colored buttons 
    if len(colored_buttons)==0:
        button_grid["bg"]=color
        #possible_options = [value for key, value in cases.items() if key]
        #print("possinle_options",possible_actions)
        
        
        
        
    elif len(colored_buttons)==1:
        #[(3, 7), (4, 8), (3, 9), (2, 8)]
        #colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
        #all_buttons = [tuple((i["text"])) for i in frame.grid_slaves()]
        #print("all_buttons_text", all_buttons)
        #now i need to disable the buttons
        #[i.config(state = DISABLED, bg="grey") for i in frame.grid_slaves() if ((int(x), int(y)) for x, y in tuple(i["text"])) not in possible_actions.keys ]
        pass
        
    

#button of the ships
def ship_click(color, frame, button):
    #removes the color from the button 
    colored_buttons = [i for i in frame.grid_slaves() if i["bg"]==color]
    if len(colored_buttons) == 0:
        total_ships = button["text"]
    #needs here to add the button config attribute and add the other argumnets as well
        [i.config(command=lambda button_grid=i, color=color, total_ships=total_ships, frame=frame : button_click(button_grid, color, total_ships, frame)) for i in frame.grid_slaves()]
        button["bg"]=color
    else:
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
    print("name", name)
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
    