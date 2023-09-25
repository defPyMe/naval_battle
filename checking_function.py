




#x as the string with the button name 
def create_columns(x):
    #creating the two lists 
    horizontal = []
    vertical = []
    #all horizontal lines 
    for i in range(10):
        l = []
        for j in range(10):
            l.append(int(str(i)+str(j)))
        horizontal.append(l)


  
    #all vertical lines 
    for j in range(10):
        l = []
        for i in [0,1,2,3,4,5,6,7,8,9]:
            l.append(int(str(i)+str(j)))
        vertical.append(l)
        
        
        
    #getting the two lists based on x and y 
    all_y_vert = [i for i in vertical if x in i]
    all_x_hor = [i for i in horizontal if x in i]

    #returning the two lists with the possible values

    
    print("all_y_vert, all_x_vert", all_y_vert,  all_x_hor )
    return all_y_vert, all_x_hor


# i will use here the same functionf for checking teh up and d
def create_tuple(all_colored,input_no_skip, pressed):
    #all colored
    #all__ = [74,23,25,33,45]# here i have two collisions that are the 333 and teh 35
    #all possible x
    all_colored_ = [int(i) for i in all_colored]
    #all_ = [32,33,34,35,36] #case of x
    g = [[],[]]
    #getting all the collisions 
    f = [i for i in input_no_skip if i in all_colored_]
    #this is teh smallest one so zero is a good guess
    print("f ----------------->",f, all_colored_, input_no_skip, pressed)
    g[0]= [ 0 if len(f) == 0 else 0 if len(f)==1 and pressed[0] < f[0] else max(max([i for i in input_no_skip if i in all_colored_]), pressed[0])] #what happens here if something is found or nothing isfound smaller number 0 or number 
    # if[] then 0, if one number add also the pressed needs to see if bigger or smaller than pressed, if two keep smaller  
    g[1]= [ 100 if len(f) == 0 else 100 if len(f)==1 and pressed[0] > f[0]  else max(max([i for i in input_no_skip if i in all_colored_]), pressed[0])]
    #not working here as well as we are missing some values 
    
    
    
    
    
    
    
    return g

#teh colored_buttons_singular = all teh current ships colored
#all colored = all teh buttons colored for all teh ships
#total ships = all teh ships to place for teh specific ship
def getting_possible_collision(all_colored, no_skip_x,no_skip_y, pressed):
    #changing to int as they will be analyzed as integers
    
    #getting all_x and y ordered if there are any collisions
    #print("(all_colored, no_skip_x,no_skip_y, pressed", all_colored, no_skip_x,no_skip_y, pressed)
    collisions_x = sorted([i for i in no_skip_x if i in all_colored])
    collisions_y = sorted([i for i in no_skip_y if i in all_colored])
    #here i can have no collision, up down in both, only up/only down , no collision
    #the lists should do nothing if empty, approach either from top or bottom 
    #[33,36], [], [33]
    #pressed	34
    #all_colored	74,23,33,25,35,45
    #all_x_no_skip	32,-33-,34,35,-36-
    #all_y_no_skip	14,24,34,44,54
    #returns a possible collision or not in case some ships were found or not
    x_collision = create_tuple(all_colored, no_skip_x, pressed)#creating for x
    y_collision =  create_tuple(all_colored, no_skip_y, pressed)
    #result above [[33], [100]], [[0],[100]]
    print(no_skip_y, y_collision, no_skip_x, x_collision , type(no_skip_y), type(y_collision), type(no_skip_x), type(x_collision))
    #remove the values using teh limits 
    #[29, 39, 49] [[0], [100]] [38, 39] [[0], [100]] <class 'list'> <class 'list'> <class 'list'> <class 'list'>
    result_possible = [i for i in no_skip_y if i > y_collision[0][0] and i < y_collision[1][0]] + [i for i in no_skip_x if i > x_collision[0][0] and i < x_collision[1][0]]
    #result_possible_ = [str(i) for i in result_possible]
    #print("result_possible, result_possible_", result_possible, result_possible)
    return result_possible
    
    

def calculate_cases(x, y,colored_buttons_singular, all_colored, total_ships):
    #here x,y are integers
    #print("x,y in the ==1 function", x,y)
    #print("all the things plugged in the function")
    #print(x, y,colored_buttons_singular, all_colored, total_ships)
        #generating the list of numbers
    all_values_allowed = [i for i in range(0, 11)]
    #ex = 4- positioned 
    diff = total_ships - (len(colored_buttons_singular) + 1)
    pressed = [int(str(y)+str(x))]
    if diff > 0:
    #the first list is the y while the second is the x
        x_y_column_row = create_columns(pressed[0])
        #creating the possible values using the diff
        all_x = [int(str(y)+(str(int(x+i)))) for i in range (-diff, diff+1)] #could be out of teh border
        all_y = [ int(str(int(y+i))+(str(x))) for i in range (-diff, diff+1)] #could be out here as well
        # all_x, all_y corrected, removing values that are not in the row
        #sorting the two rows
        #print("all_x, all_y, x_y_column_row", x_y_column_row)
        all_x_no_skip = sorted([i for i in all_x if i in x_y_column_row[1][0]])
        all_y_no_skip = sorted([i for i in all_y if i in x_y_column_row[0][0]])
        #print(" all_x, all_y, all_x_no_skip,  all_y_no_skip", all_x, all_y, all_x_no_skip,  all_y_no_skip)
        #removing also the ships collision
        #it shouldnt go over the ship if crossed  
        
        #getting if there is a collision , should return a tuple, for y and x
        results_pre = getting_possible_collision(all_colored,   all_x_no_skip , all_y_no_skip, pressed)
        #i need to color the buttons now
        results = [['{:02d}'.format(i) for i in  results_pre], diff, colored_buttons_singular]
        #print("results i am getting now", results)    
#adding a flag to see if it is coloring a retrieve dbattle ot a new one , also if it is ongoing



        #def coloring(frame, all_ships_opponent, all_hits_opponent, all_misses_opponent, flag, j):

        # 
    else:
        results = [[],diff,[]]
    return results
    
    
    