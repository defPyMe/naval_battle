import ast

f = ["['', '44', '54', '55']"]
f_list = ast.literal_eval(f[0])
print(f_list)
