def most_frequent(List):
    counter = 0
    num = List[0]
    # returns the most frequent
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i
 
    return num





def checking_lines():
    #creating the two lists 
    horizontal = []
    vertical = []
    #all horizontal lines 
    for i in range(10):
        l = []
        for j in range(10):
            l.append(str(i)+str(j))
        horizontal.append(l)


  
    #all vertical lines 
    for j in range(10):
       l = []
       for i in [0,2,3,4,5,6,7,8,9]:
    
        l.append(str(i)+str(j))
        vertical.append(l)
    
        
    return vertical, horizontal


#creating a function that takes the input and then we spit out the corrected possibilites 
#lò is teh list we useti 
#is this only for the x rows? 
def  avoiding_skipping_rows(input_x):
    #creating the checklist here 
    l =  checking_lines()
    #correcting the difference 
    correct_collision_interval_x_str = ['{:02d}'.format(i) for i in  input_x]
    #correct_collision_interval_y_str = ['{:02d}'.format(i) for i in  correct_collision_interval_y]
    indices = []
    for i, sublist in enumerate(l):
        element_found =  [(i,j) for j in correct_collision_interval_x_str if j in sublist]
        if element_found !=[]:
            indices = indices + element_found
        else:
            pass
    #need to get the main component of the list 
    result_most_common = (most_frequent(indices))[0]
    #going back to integer    
    return [ i[1] for i in indices if i[0] == result_most_common ]


#here i need also the pressed x and y as i need to get where itis positioned in case it is one
#needs to return the values of the x and y
def checking_first_button(trial_x, trial_y, x, y,all_x, all_y):
    #getting the two lenghts of the lists
    #ex (0, 3)
    len_x_y = [len(trial_x), len(trial_y)]
    #here it needs to default to 2 if it is bigger than one 
    len_x_y_cleaned = [i if i<2 else 2 for i in len_x_y]
    #creating the reference dictionary
    #need to include both parts in the dictionary with min x and min y
    #I have to put here the differenvce in y and x
    
    # SHOULD I add one with the variable and iterate
    print("all_x, all_y", all_x, all_y)
    print("trial_x, trial_y, len_x_y_cleaned", trial_x, trial_y, len_x_y_cleaned)
    
    [i.append(0) for i in [trial_x, trial_y] if i== []]
    
    cases_x =  {1: [max(trial_x)], 0: [0, 100], 2:[min(trial_x), max(trial_x)]}
    cases_y = {1: [max(trial_y)], 0: [0, 100], 2:[min(trial_y), max(trial_y)]}

    
    #is this returning two separate things?
    results = [[],[]]
    #trying to crteate the wo entities with a two element list 
    results[0].append(cases_x[len_x_y_cleaned[0]])
    results[1].append(cases_y[len_x_y_cleaned[1]]) 
    print("results", results)

    #needs the calculaition now if len (i(0))==1 --> needs if left or right
    #they are ints
    for i in range(len(results)):
        pressed_button = int(str(y)+str(x))
        #identifying if it is a max or min
        #the second needs to take the first thing in the list
        if len(results[0][0])==1 and len(results[1][0])!=1:
            #here x is equal to 1
            #going down the line and getting the single list item
            if pressed_button > results[0][0][0]:
                print("case1", pressed_button,results[0][0][0], all_x, all_y)
                #the part that i smore tha one in leght shouldn t really change 
                #approaching from above 
                correct_collision_interval_x =  [i for i in all_x if i > results[0][0][0]] 
                #needds to go a step further down
                correct_collision_interval_y = [i for i in all_y if i > results[1][0][0] and i < results[1][0][1]]

            else:
                print("case2" , pressed_button,  results[0][0][0], all_x, all_y)
                correct_collision_interval_x =  [i for i in all_x if i < results[0][0][0]] 
                correct_collision_interval_y = [i for i in all_y if i > results[1][0][0] and i < results[1][0][1]]
            #should be ok here
 
        elif len(results[0][0])!=1 and len(results[1][0])==1:
            if pressed_button > results[1][0][0]:
                #getting the second one 
                print("case3", pressed_button,results[1][0][0],all_x, all_y  )
                
                #ARE THE TWO CORRECT? ARE WE GETTING THE RIGHT INDEXING? 
                
                
                
                correct_collision_interval_x =   [i for i in all_x if i > results[0][0][0] and i < results[0][0][1]] 
                correct_collision_interval_y = [i for i in all_y if i > results[1][0][0]] 

            else:
                print("case4", pressed_button,results[1][0][0], all_x, all_y)
                correct_collision_interval_x =   [i for i in all_x if i > results[0][0][0] and i < results[0][0][1]] 
                correct_collision_interval_y = [i for i in all_y if i < results[1][0][0]] 

        #now the case where we have all the values above the chosen threshold            
        elif len(results[0][0])!=1 and len(results[1][0])!=1:
            if results[0][0]==[0,100] and results[1][0]!=[0,100]:
                #it means i have the situation to check into the second 
                if pressed_button > results[1][0][0]:
                    
                    #then we are approaching from below
                        print("case5", pressed_button,results[1][0][0], all_x, all_y)
                        correct_collision_interval_x = [i for i in all_x if i > results[0][0][0] and i < results[0][0][1]]
                        correct_collision_interval_y = [i for i in all_y if i > results[1][0][0]]#pressed button
                elif pressed_button < results[1][0][0]:     
                       #approaching from above
                        print("case6", pressed_button, results[1][0][0], all_x, all_y)
                        correct_collision_interval_x = [i for i in all_x if i > results[0][0][0] and i < results[0][0][1]]
                        correct_collision_interval_y = [i for i in all_y if i < results[1][0][0]]#pressed button
                        #case in which the first is different 
            elif results[0][0]!=[0,100] and results[1][0]==[0,100]:
                #only minimum here 
                if pressed_button > results[0][0][0]:
                    print("case7", pressed_button,  results[0][0][0],all_x, all_y)
                    #approaching from below
                    correct_collision_interval_x = [i for i in all_x if i > results[0][0][0]]#pressed button before
                    correct_collision_interval_y = [i for i in all_y if i > results[0][0][0] and i < results[0][0][1]]
                elif pressed_button < results[0][0][0]:
                    print("case8", pressed_button, results[0][0][0],all_x, all_y)
                    correct_collision_interval_x = [i for i in all_x if i < pressed_button]
                    correct_collision_interval_y = [i for i in all_y if i > results[0][0][0] and i < results[0][0][1]]
            elif results[0][0]==[0,100] and results[1][0]==[0,100]:
                correct_collision_interval_x =  [i for i in all_x if i > results[0][0][0] and i < results[0][0][1]]
                correct_collision_interval_y = [i for i in all_y if i > results[1][0][0] and i < results[1][0][1]]
            
                    
        #neeeds an outer circle where the cases of x [0,100] and cases y [0, 100] is gotten        
 
    #outside of all the ifs i use a conversion
    print("what the correct collisons are", correct_collision_interval_y, correct_collision_interval_x)
    correct_collision_interval_x_str = ['{:02d}'.format(i) for i in  correct_collision_interval_x]
    correct_collision_interval_y_str = ['{:02d}'.format(i) for i in  correct_collision_interval_y]
    #this is a list with all the chosen values 
    return correct_collision_interval_x_str, correct_collision_interval_y_str

    


def calculate_cases(x, y,colored_buttons_singular, all_colored, total_ships):
    #here x,y are integers
    #print("x,y in the ==1 function", x,y)
    #print("all the things plugged in the function")
    #print(x, y,colored_buttons_singular, all_colored, total_ships)
        #generating the list of numbers
    all_values_allowed = [i for i in range(0, 11)]
    #ex = 4- positioned 
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
            all_x_ = [int(str(y)+(str(int(x+i)))) for i in range (-diff, diff+1) if x+i in all_values_allowed] 
            all_y = [ int(str(int(y+i))+(str(x))) for i in range (-diff, diff+1) if y+i in all_values_allowed]
            
            
            
            #ADDING THE CHaECKING FUNCTION TO SEE IF ALL_X IS THE PROBLEM
            
            
            #PROBLE,M!!! NEEDDS SDTO RETURN INTEGERS 
            
            
            all_x = [int(i) for i in avoiding_skipping_rows(all_x_)]
         
            
            print("all_x, all_y, all_x is worked with the all skipping rows function", all_x, all_y)
            
            
            
            
            #here in case i press 23 i will get respectively all_x = ['03', '13', '23', '33', '43'] all_y = ['21', '22', '23', '24', '25']
            #now i need to check if any of the options is in the already colored buttons
            #here i make the all_colored list in integers
            all_colored_int = [int(i) for i in all_colored]
            #the below should work as we have all integers in both
            trying_x = [i for i in all_x if i in all_colored_int]
            trying_y = [i for i in all_y if i in all_colored_int]
            
            print("trying_x, trying_y that go into checking_first_button", trying_x, trying_y)
            
            
            #pressed buttons
            #should put the new function here as the elements are all calculated , here an obj is returned 
            tuple_result = checking_first_button(trying_x, trying_y, x, y,all_x, all_y)
            
            
            
 
            correct_collision_interval_x_str = tuple_result[0]
            correct_collision_interval_y_str = tuple_result [1]
            print( "correct tuple collision",  correct_collision_interval_x_str,    correct_collision_interval_y_str)
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
    
    
    
    
    
    print("cases_list_str, diff, colored_buttons_singular",cases_list_str, diff, colored_buttons_singular)
    
    return cases_list_str, diff, colored_buttons_singular

            
            