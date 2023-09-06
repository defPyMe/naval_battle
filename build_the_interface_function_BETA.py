import ast

input_str =  "['', '03', '13', '23', '31', '32', '04', '34', '33', '14', '24', '44', '43', '42']" # Replace this with your input string

hit_or_misses = ast.literal_eval(input_str)
print(hit_or_misses)
"""

input_list = ast.literal_eval(input_str)
    #result_list = [int(x) if x.isdigit() else x.strip("'") for x in input_list]
print(input_list)"""

