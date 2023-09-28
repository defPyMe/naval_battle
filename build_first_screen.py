from tkinter import *
from tkinter import messagebox
from build_user_page import build_user_page
from sql_queries_ import checking_credentials, delete_widgets

#adding a chat on the right side of the screen in the battle playing 
#adding a checking mechanism for the sinking of the ship







def logging_in(name_input, root):
    #need to add a connection to the list of users here 
    #should look here into the users table
    print("name input in logging in --> ",name_input)
    if checking_credentials(name_input):
        messagebox.showinfo("log_info", "log in successful")
        #here called with the delete widget function
        build_user_page(delete_widgets(root),name_input, root )
    else:
        messagebox.showwarning("log_info", "wrong credentials")




def build_first_screen():  
    root=Tk()
    root.geometry("200x200")
    root.resizable(False, False)
    label = Label(text = "", width=3, height=3)
    label1 = Label(text = "insert username")
    label_space = Label(text = "", width=1, height=1)
    label_space1 = Label(text = "", width=1, height=1)
    text_box = Entry(root)
    #giving the function som earguments without executing it directly with lambd
    button_log = Button(text = "log in", command = lambda: logging_in(text_box.get().strip(), root))
    #lambda needs lambda event here to work
    text_box.bind('<Return>',  lambda event: logging_in(text_box.get().strip(), root))
    label.pack()
    label1.pack()
    label_space.pack()
    text_box.pack()
    label_space1.pack()
    button_log.pack()
    #root.configure(background='blue')
    #addding an icon here? is it working
    photo = PhotoImage(file = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\pngwing.com.png")
    root.iconphoto(False, photo)
    root.mainloop()
    
    
build_first_screen()


#need to change the user picture frames as they are not showing the correct info 
#adding some images to teh build user page 