x = 2
y = 3
all_values_allowed = [i for i in range(0, 11)]
tot = 3 
diff = 3 - 1
all_colored = ["13"]
all_x = [(str(int(x+i))+str(y)) for i in range (-diff, diff+1) if x+i in all_values_allowed]
all_y = [(str(x) + str(int(y+i))) for i in range (-diff, diff+1) if y+i in all_values_allowed]


trying_x = [i for i in all_x if i in all_colored ]
trying_y = [i for i in all_y if i in all_colored]





print(all_x, all_y)
print(len(trying_x), len(trying_y))





