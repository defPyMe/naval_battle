trial_x = [43,44,45,46,47]
trial_y = [25, 35, 45, 55, 65]





len_x_y = [0, 3]
#here it needs to default to 2 if it is bigger than one 
len_x_y_cleaned = [i if i<2 else 2 for i in len_x_y]
# [f(x) if condition else g(x) for x in sequence]
cases = {1: (max(trial_x)), 0: ((0, 100), (0, 100)), 2:((min(trial_x), max(trial_x)))}
result = [cases[i] for i in len_x_y_cleaned]
print(result)