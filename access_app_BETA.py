import ast

f =  ["['', '65', '65', '75', '75', '85', '85', '86', '86', '76', '76', '77', '77', '72', '72']"]
f_list = ast.literal_eval(f[0])
print(f_list)
