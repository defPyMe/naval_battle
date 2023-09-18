

def funct(*args):
    print(args)

def delete_widgets_access_previous(root, funct, *args):
    print(args)
    #calling the other screen , passing in some arguments 
    print(funct(args))
    
delete_widgets_access_previous("root", "funct", "name", "root")