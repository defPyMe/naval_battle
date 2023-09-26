"""f = "(1, adding first message),(2, adding second),(1, adding message),(2, adding reply),(1, adding message),(2, adding reply)"


ff = f.replace("[", "").replace("]", "").replace(")", "").replace("(", "").split(",")
gg = [(ff[i].strip(), ff[j+1].strip()) for i in range(0,len(ff)-1) for j in range(1, len(ff)-1)]
#for i in ff:


# 0,1 - 2,3 - 4,5 ....
#processing the list
kk = [((ff[i]).strip(), (ff[i+1]).strip()) for i in range(0,len(ff)-1,2)]


print(kk)"""



print(tuple(2))