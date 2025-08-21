# EJERCICIO 1 CASAS DE HOGWARTS

from logic import * 
# Lista de personas y casas 
personas = ["gilderoy", "minerva", "pomona", "horace"] 
casas = ["gryffindor", "hufflepuff", "ravenclaw", "slytherin"] 
 
# Crear símbolos lógicos para cada combinación persona-casa 
simbolos = [] 
for persona in personas: 
   for casa in casas: 
       simbolos.append(Symbol(f"{persona}_{casa}")) 
 
# Base de conocimiento vacía 
conocimiento = And() 
 
# Regla 1: Cada persona pertenece a una sola casa (al menos una) 
for persona in personas: 
   conocimiento.add(Or( 
       Symbol(f"{persona}_gryffindor"), 
       Symbol(f"{persona}_hufflepuff"), 
       Symbol(f"{persona}_ravenclaw"), 
       Symbol(f"{persona}_slytherin") 
   )) 
 
# Regla 2: Cada persona solo puede estar en una casa (no en dos o más) 
for persona in personas: 
   for casa1 in casas: 
       for casa2 in casas: 
           if casa1 != casa2: 
               conocimiento.add( 
                   Implication(Symbol(f"{persona}_{casa1}"), 
Not(Symbol(f"{persona}_{casa2}"))) 
               ) 
 
# Regla 3: Solo una persona puede pertenecer a cada casa 
for casa in casas: 
   for p1 in personas: 
       for p2 in personas: 
           if p1 != p2: 
               conocimiento.add( 
                   Implication(Symbol(f"{p1}_{casa}"), 
Not(Symbol(f"{p2}_{casa}"))) 
               ) 
 
# Regla 4: Minerva pertenece a Hufflepuff 
conocimiento.add(Symbol("minerva_hufflepuff")) 
 
# Regla 5: Gilderoy está en Hufflepuff o Ravenclaw 
conocimiento.add(Or(Symbol("gilderoy_hufflepuff"), 
Symbol("gilderoy_ravenclaw"))) 
 
# Regla 6: Pomona no está en Gryffindor 
conocimiento.add(Not(Symbol("pomona_gryffindor"))) 
 
# Mostrar solo los símbolos que se pueden deducir como verdaderos 
for simbolo in simbolos: 
   if model_check(conocimiento, simbolo): 
       print(simbolo) 




# EJERCICIO 2 DE LAS PELOTAS

from logic import * 
# Colores y posiciones posibles 
colors = ["red", "blue", "green", "yellow"] 
positions = [0, 1, 2, 3] 
# Lista para guardar todos los símbolos tipo red0, blue1, etc. 
symbols = [] 
for i in positions: 
for color in colors: 
symbols.append(Symbol(f"{color}{i}")) 
# Creamos la base de conocimiento 
knowledge = And() 
# Cada color tiene que estar en una sola posición 
for color in colors: 
knowledge.add(Or( 
Symbol(f"{color}0"), Symbol(f"{color}1"), 
Symbol(f"{color}2"), Symbol(f"{color}3") 
)) 
# Un mismo color no puede estar en dos posiciones distintas 
for color in colors: 
for i in positions: 
       for j in positions: 
           if i != j: 
               knowledge.add(Implication( 
                   Symbol(f"{color}{i}"), Not(Symbol(f"{color}{j}")) 
               )) 
 
# En cada posición solo puede haber un color 
for i in positions: 
   for c1 in colors: 
       for c2 in colors: 
           if c1 != c2: 
               knowledge.add(Implication( 
                   Symbol(f"{c1}{i}"), Not(Symbol(f"{c2}{i}")) 
               )) 
 
# Pista 1: red0, blue1, green2, yellow3 → solo 2 están bien 
# Se prueban todas las combinaciones posibles donde hay 2 verdaderos y 2 
falsos 
knowledge.add(Or( 
   And(Symbol("red0"), Symbol("blue1"), Not(Symbol("green2")), 
Not(Symbol("yellow3"))), 
   And(Symbol("red0"), Not(Symbol("blue1")), Symbol("green2"), 
Not(Symbol("yellow3"))), 
   And(Symbol("red0"), Not(Symbol("blue1")), Not(Symbol("green2")), 
Symbol("yellow3")), 
   And(Not(Symbol("red0")), Symbol("blue1"), Symbol("green2"), 
Not(Symbol("yellow3"))), 
   And(Not(Symbol("red0")), Symbol("blue1"), Not(Symbol("green2")), 
Symbol("yellow3")), 
   And(Not(Symbol("red0")), Not(Symbol("blue1")), Symbol("green2"), 
Symbol("yellow3")) 
)) 
 
# Pista 2: blue0, red1, green2, yellow3 → ninguno está bien 
# Se descartan esas combinaciones directamente 
knowledge.add(And( 
   Not(Symbol("blue0")), 
   Not(Symbol("red1")), 
   Not(Symbol("green2")), 
   Not(Symbol("yellow3")) 
)) 
 
# Mostrar los símbolos que se pueden confirmar como verdaderos 
print("Símbolos verdaderos:") 
for symbol in symbols: 
   if model_check(knowledge, symbol): 
       print(f"{symbol}") 
