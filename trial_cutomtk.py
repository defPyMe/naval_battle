import sys
import math
from contextlib import redirect_stdout



def compute_closest_to_zero(ts):
    print(ts)
    if 0<len(ts)<=10000:
        #creating dicitionary
        dict_variables ={abs(i): i for i in ts}
        print(dict_variables)
        min_key = min(dict_variables.keys())
        max_value = max(dict_variables.values())
        return max_value
    else:
        return 0
    
ts = [1, -2, -8, 4, 5]
compute_closest_to_zero(ts)