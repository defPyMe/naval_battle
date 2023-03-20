def calculate_cases(x, y):
    all_cases = {(x, y-1): (bool(y-1>0)),  (x+1, y): (bool(x+1<10)), (x, y+1):(bool(y+1<10)), (x-1, y):(bool(x-1>0))}
    cases = {key: value for key, value in all_cases.items() if value == True}
    cases_list = [i for i in cases.keys()]
    return cases_list

# example usage
cases = calculate_cases(5, 4)
print(cases)  