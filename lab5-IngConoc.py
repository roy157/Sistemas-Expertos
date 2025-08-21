from logic import *   
 
#ASESINOS 
MUSTARD = Symbol("MUSTARD") 
SCARLET = Symbol("SCARLET") 
PLUM = Symbol("PLUM") 
#LUGAR 
BALLROOM = Symbol("BALLROOM") 
KITCHEN = Symbol("KITCHEN") 
LIBRARY = Symbol("LIBRARY") 
#ARMA 
KNIFE = Symbol("KNIFE") 
REVOLVER = Symbol("REVOLVER") 
WRENCH = Symbol("WRENCH") 
 
simbolos = [MUSTARD,SCARLET,PLUM,BALLROOM 
,KITCHEN,LIBRARY,KNIFE,REVOLVER,WRENCH] 
 
#Sabemos que hay un asesino que estuvo en una ubicacion con un arma 
CONOCIMIENTO = And( 
     Or(MUSTARD,SCARLET,PLUM), 
     Or(BALLROOM,KITCHEN,LIBRARY), 
     Or(KNIFE,REVOLVER,WRENCH) 
) 
#Se nos entregan las cartas iniciales: scarlet ballroom knife 
CONOCIMIENTO.add(And(Not(SCARLET),Not(BALLROOM),Not(KNIFE))) 
#Por lo menos uno de los sguientes es falso mustrard library wrench 
CONOCIMIENTO.add(And(Or( 
    Not(MUSTARD), 
    Not(LIBRARY), 
    Not(WRENCH)) 
    )) 
#Sabemos que no es plum 
CONOCIMIENTO.add(And(Not(PLUM))) 
#Sabemos que no fue en el kitchen 
CONOCIMIENTO.add(And(Not(KITCHEN))) 
 
for simbolo in simbolos: 
    if model_check(CONOCIMIENTO, simbolo): 
        print(f"{simbolo}: VERDADERO") 
    elif model_check(CONOCIMIENTO, Not(simbolo)): 
        print(f"{simbolo}: FALSO") 
    else: 
        print(f"{simbolo}: QUIZÁ") 