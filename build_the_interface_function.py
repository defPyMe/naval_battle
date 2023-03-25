#all_values_allowed = [i for i in range(0, 11)]
#x = 2
#case of x
#all_current_ships_values = ["22", "23", "24"]

#if (str(all_current_ships_values[0]))[:1] == str(all_current_ships_values[1])[:1]:
#    print("comparison operation",(str(all_current_ships_values[0]))[:1],str(all_current_ships_values[1])[:1] )
#    
#    all_y = [int((i[1:])) for i in all_current_ships_values]
                #getting the minimum and m,ax
#    print("all_y",all_y)
#    min_x = min(all_y)
#    max_x = max(all_y)
#    diff = 1
#    print("min_x, max_x", min_x, max_x)
                #now i need to expand in both directions if there is space
#    all_y_up = [(str(x)+str(int(max_x+i))) for i in range (diff, diff +2) if max_x+i in all_values_allowed]
#    all_y_down = [(str(x)+str(int(min_x+i))) for i in range (-diff -1 , 0) if min_x+i in all_values_allowed]

#    print("all_x_right, all_x_left", all_y_up, all_y_down)
#else : print("not entering")
all_values_allowed = [i for i in range(0, 11)]
x = 2
all_y = [7, 8]
min_y = min(all_y)
max_y = max(all_y)
print("min and maz y", min_y, max_y)
diff = 2
#now i need to expand in both directions if there is space
#i expand one more because there might be some 
all_y_up = [(str(int(min_y+i))+str(x)) for i in range (0, diff+1) if min_y+i in all_values_allowed]
all_y_down = [(str(int(max_y+i))+str(x)) for i in range (-diff-1, 0) if max_y+i in all_values_allowed]

print("down, up", all_y_down, all_y_up)