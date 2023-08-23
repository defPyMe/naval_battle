#how to get the difference with the all_x and all_y











#all_x, all_y [7, 8, 9, 10] [9, 19, 29]



def checking_lines(all_x, all_y):
    #creating the two lists 
    horizontal = []
    vertical = []
    #all horizontal lines 
    for i in range(10):
        l = []
        for j in range(10):
            l.append(str(i)+str(j))
        horizontal.append(l)


    #SHOULDN T BE NEEDED HERE 
    #all vertical lines 
    #for j in range(10):
    #    l = []
    #    for i in [0,2,3,4,5,6,7,8,9]:
    #    
    #        l.append(str(i)+str(j))
    #    vertical.append(l)
    
        
    return horizontal   
    #return vertical, horizontal







l = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'], ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19'], ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29'], 
     ['30', '31', '32', '33', '34', '35', '36', '37', '38', '39'], ['40', '41', '42', '43', '44', '45', '46', '47', '48', '49'], ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59'], 
     ['60', '61', '62', '63', '64', '65', '66', '67', '68', '69'], ['70', '71', '72', '73', '74', '75', '76', '77', '78', '79'], ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89'], 
     ['90', '91', '92', '93', '94', '95', '96', '97', '98', '99']]  

all_x = [18,19,20]

#funtion to get the most common elements, taken from geeks for geeks
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num


#creating a function that takes the input and then we spit out the corrected possibilites 
#lò is teh list we useti 
#is this only for the x rows? 
def  avoiding_skipping_rows(input_x, l):
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

    
    
    
    
    return [ i[1] for i in indices if i[0] == result_most_common ]


avoiding_skipping_rows(all_x, l)



