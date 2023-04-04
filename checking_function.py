#here i need also the pressed x and y as i need to get where itis positioned in case it is one
#needs to return the values of the x and y
def checking_first_button(trial_x, trial_y, x, y,all_x, all_y,  diff):
    #getting the two lenghts of the lists
    #ex (0, 3)
    len_x_y = [len(trial_x), len(trial_y)]
    #here it needs to default to 2 if it is bigger than one 
    len_x_y_cleaned = [i if i<2 else 2 for i in len_x_y]
    #creating the reference dictionary
    #need to include both parts in the dictionary with min x and min y
    
    # SHOULD I ADD THE Y HERE?????
    
    cases =  {1: (max(trial_x)), 0: ((0, 100), (0, 100)), 2:((min(trial_x), max(trial_x)))}
    result = [cases[i] for i in len_x_y_cleaned]
    #needs the calculaition now if len (i(0))==1 --> needs if left or right
    #they are ints
    for i in result:
        if len(i)==1:
            pressed_button = int(str(y)+str(x))
            #if it is lower than the pressed button
            if i[0] < pressed_button:
                #uniting the two here
                correct_collision_interval = [i for i in all_x if i > i[0] ] + [i for i in all_y if i > i[0] ]
            elif i[0] < pressed_button:
                #calling it the same so that i have to return one thing onluy 
                correct_collision_interval_x = [i for i in all_x if i < i[0] ] + [i for i in all_y if i < i[0] ]
        else:
            correct_collision_interval_x = [i for i in all_x if i > min_max_trying_x[0] and i < min_max_trying_x[1]]
            correct_collision_interval_y = [i for i in all_y if i > min_max_trying_y[0] and i < min_max_trying_y[1]]
    
    
    
    
    correct_collision_interval_x = [i for i in all_x if i > min_max_trying_x[0] and i < min_max_trying_x[1]]
    correct_collision_interval_y = [i for i in all_y if i > min_max_trying_y[0] and i < min_max_trying_y[1]]
    
    
    
    
    
    pass
    








def calculate_cases(x, y,colored_buttons_singular, all_colored, total_ships):
    #here x,y are integers
    #print("x,y in the ==1 function", x,y)
    #print("all the things plugged in the function")
    #print(x, y,colored_buttons_singular, all_colored, total_ships)
        #generating the list of numbers
    all_values_allowed = [i for i in range(0, 11)]
    diff = total_ships - (len(colored_buttons_singular) + 1)
    pressed = [str(y)+str(x)]
    #print("diff----->", diff)
    #here i have cases of 2,3,4 ships as the first get inteccepted right away 
    if diff > 0:
        #now i need to model what happens when we have a len==1 of the colored buttons
        #need to consider that there can be obstacles or not 
        if len(colored_buttons_singular) == 0:
            #now i expand in all directions(x,y) with the diff
            #i type cast here again to get a list of integers
            #the below includes the pressed button
            all_x = [int(str(y)+(str(int(x+i)))) for i in range (-diff, diff+1) if x+i in all_values_allowed] 
            all_y = [ int(str(int(y+i))+(str(x))) for i in range (-diff, diff+1) if y+i in all_values_allowed]
            #here in case i press 23 i will get respectively all_x = ['03', '13', '23', '33', '43'] all_y = ['21', '22', '23', '24', '25']
            #now i need to check if any of the options is in the already colored buttons
            #here i make the all_colored list in integers
            all_colored_int = [int(i) for i in all_colored]
            #the below should work as we have all integers in both
            trying_x = [i for i in all_x if i in all_colored_int]
            trying_y = [i for i in all_y if i in all_colored_int]
            #pressed buttons
            print("all_x, all_y", all_x, all_y)
            print("trying_x, trying_y", trying_x, trying_y)
            #now i need to get the minimum and maximum to see where we touch first, if we touch at all, they can be tuples
            #need to consider all the following cases 
            # 1) trying_x != zer trying y == 0, 2) trying_x == 0 trying y != 0, 3) trying_x == 0 trying y == 0, 4) trying_x != zer trying y != 0
            #need to consider here the possible collisions with other ships 
            #as of now not moving in all directions , i have t try to 
            #if it is 54 anything different than that might work, but need to check if the lenght is 
            if len(trying_x)==0 and len(trying_y)!=0:
                min_max_trying_x = (min(trying_x), max(trying_x))
                min_max_trying_y = (0, 100)
            elif len(trying_y)!=0 and len(trying_x)==0:
                min_max_trying_y = (min(trying_y), max(trying_y))
                min_max_trying_x = (0, 100)
            elif len(trying_y)==0 and len(trying_x)==0:
                min_max_trying_x = (-1, 100)
                min_max_trying_y = (-1, 100)
            elif len(trying_y)!=0 and len(trying_x)!=0:
                min_max_trying_y = (min(trying_y), max(trying_y))
                min_max_trying_x = (min(trying_x), max(trying_x))
            #getting the different elements in all_x, all_y in teh interval
            print("min_max_trying_y", min_max_trying_y, min_max_trying_x)
            correct_collision_interval_x = [i for i in all_x if i > min_max_trying_x[0] and i < min_max_trying_x[1]]
            correct_collision_interval_y = [i for i in all_y if i > min_max_trying_y[0] and i < min_max_trying_y[1]]
            #converting all the values to strings as that is what the below expects
            correct_collision_interval_x_str = ['{:02d}'.format(i) for i in  correct_collision_interval_x]
            correct_collision_interval_y_str = ['{:02d}'.format(i) for i in  correct_collision_interval_y]
            print("correct_collision_interval_y_str, correct_collision_interval_x_str", correct_collision_interval_y_str,correct_collision_interval_x_str)
            
            #if the lenght is equal or above == ok that list, if it is below --> not equal
            if len( correct_collision_interval_x_str) >= diff and len( correct_collision_interval_y_str) < diff:
                #case of obstacle on the x and y but only x feasible
                cases_list_str = correct_collision_interval_x_str
            elif len( correct_collision_interval_x_str) < diff and len( correct_collision_interval_y_str) >= diff :
                #case of obstacle on the x and y but only y feasible
                cases_list_str = correct_collision_interval_y_str 
                #here we can have the two are feasible
            elif len( correct_collision_interval_x_str) >= diff and len( correct_collision_interval_y_str) >= diff:
                #case of unpositionable ship, returns an empty list as we cannot position 
                cases_list_str = correct_collision_interval_y_str + correct_collision_interval_x_str 
            #in case both are strictly less then we know we cannot position and we return an empty string
            elif len( correct_collision_interval_x_str) < diff and len( correct_collision_interval_y_str) < diff:
                #here i can go all the way in both directions 
                cases_list_str = []
            #the first time we access it should be equal to 0 while the second to something bigger than 0
        elif len(colored_buttons_singular) > 0:
            #need to get here if we are in a case of x or y
            #the obstacles should have been taken care by the above. here we need to consider the min and max and if there are any obstacles in both parts 
            #if there are obstacles we need to choose either one or teh other
            #here i get all the values i have that share the same (chosen in button) color
            #passing here the clicked button as well
            all_current_ships_values = [i["text"] for i in colored_buttons_singular] + [str(y)+str(x)]
            #print("all current ships values + evaluation that should be  ", all_current_ships_values,str(all_current_ships_values[0])[:1], str(all_current_ships_values[1])[:1])
            #getting the set so we do not have duplicates 
            #len_set = set(all_current_ships_values)
        #getting the smallest value and the highest 
        #if the below passes we are moving horizontally so case of x
        #need some checking here to see if the pressed buttin iso of 
        #the below could be x or y --> [(01), (11)] or (0,1), (0,2)
            all_x = [int((i[1:])) for i in all_current_ships_values]
            #getting all the x and y 
            all_y = [int((i[0:1])) for i in all_current_ships_values]
            #needs the min anad max of both
            min_max_x = (min(all_x), max(all_x))
            min_max_y = (min(all_y), max(all_y))
            #getting the len of one of the two 
            len_of_one = len(all_x)
            if (min_max_x[0]+(len_of_one-1)) == (min_max_x[1]) or (min_max_y[0]+(len_of_one-1)) == min_max_y[1]:
                #after i have sorted it 
                if(str(all_current_ships_values[0]))[:1] == str(all_current_ships_values[1])[:1]:
                    #all the y are the sa
                    #print("case of all y equals")
                    all_x = [int((i[1:])) for i in all_current_ships_values]
                    #getting the minimum and m,ax
                    min_x = min(all_x)
                    max_x = max(all_x)
                    #now i need to expand in both directions if there is space
                    #i expand one more because there might be some 
                    all_x_right = [(str(y)+ str(int(max_x+i))) for i in range (0, diff +1) if max_x+i in all_values_allowed]
                    all_x_left = [str(y) + (str(int(min_x+i))) for i in range (-diff, 0) if min_x+i in all_values_allowed]
                    #print("all_x_left, all_x_right", all_x_left, all_x_right)
                    #OBSTACLE AND LIMITS?
                    #needs to check if tehre are any units in the all colored buttons 
                    #obstacles case
                    #trying_x_right = [i for i in all_x_right if i in all_colored]  
                    #trying_x_left = [i for i in all_x_left if i in all_colored]
                    #i know it is a case of x, i can unite the two lists and remove values that are in all colored
                    all_x_right_and_left = all_x_right + all_x_left
                    #exclusing collisions
                    all_x_no_collisions = [i for i in all_x_right_and_left if i not in all_colored] + pressed
                    #returning the value here
                    cases_list_str = all_x_no_collisions
                else:
                    #check here             
                    all_y = [int((i[0:1])) for i in all_current_ships_values]
                    #print("entering vertical all the y are + the x we have in the button --> ", all_y, x )
                    #getting the minimum and m,ax
                    min_y = min(all_y)
                    max_y = max(all_y)
                    #print("min and maz y", min_y, max_y)
                    #now i need to expand in both directions if there is space
                    #i expand one more because there might be some 
                    all_y_down = [(str(int(max_y+i))+str(x)) for i in range (0, diff+1) if min_y+i in all_values_allowed]
                    all_y_up = [(str(int(min_y+i))+str(x)) for i in range (-diff, 0) if max_y+i in all_values_allowed]
                    #OBSTACLE AND LIMITS?
                    #print("all ups and downs", all_y_up, all_y_down)
                    #needs to check if tehre are any units in the all colored buttons 
                    #obstacles case
                    #trying_x_right = [i for i in all_x_right if i in all_colored]  
                    #trying_x_left = [i for i in all_x_left if i in all_colored]
                    #i know it is a case of x, i can unite the two lists and remove values that are in all colored
                    all_y_up_and_down = all_y_up + all_y_down + [str(y)+str(x)]
                    #exclusing collisions
                    all_y_no_collisions = [i for i in  all_y_up_and_down if i not in all_colored] 
                    print("allowed values in case f x staying the same")
                    #returning the value here
                    cases_list_str = all_y_no_collisions
            else:
                cases_list_str = []
        #now i need to consider the case in which i have a diff == 0 that means we have positioned all
        #cannot press the same button twice, case of x and of y
    else:
        cases_list_str = []
    #returns the list and the diff
    return cases_list_str, diff, colored_buttons_singular
            #i check only the x so t
            # 
            # 
            # 
            # hat if it is not verified it is a y 
            
            