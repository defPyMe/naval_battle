"""dismissione cubo no viste micro strategy
ricreare info prima che bi provveda
budget ortega sulla pre, tutto quello lavorato (50 pezzi = 50 tag)
ad ortega serve èercentuale fallato, tutto quello con problema che non può essere venduto, fornitore esterno riceve da fallato, 

se percentuale aumenta 100 pre + costo faulty / pezzi

a lui serve parametro fallato per capire se sono bravi o no. fatto per anno di calendario solo yoox e poi azienda(produttore) e negozio (merce invenduta)
negozio più fallati come pezzi

fatto per anni e poi per stagioni di vendita"""
#all the placed sjhips 
all__ = [74,23,25,33,45]# here i have two collisions that are the 333 and teh 35
#all possible x
all_ = [32,33,34,35,36] #case of x
pressed = 34
g = [[],[]]
#getting all the collisions 
f = [i for i in all_ if i in all__]
#this is teh smallest one so zero is a good guess
print(f)
g[0]= [ 0 if len(f) == 0 else 0 if len(f)==1 and pressed < f[0] else min([i for i in all_ if i in all__])] #what happens here if something is found or nothing isfound smaller number 0 or number 
# if[] then 0, if one number add also the pressed needs to see if bigger or smaller than pressed, if two keep smaller  
g[1]= [ 100 if len(f) == 0 else 100 if len(f)==1 and pressed > f[0]  else max([i for i in all_ if i in all__])]







print(g)


