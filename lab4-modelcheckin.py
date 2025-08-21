# -*- coding: utf-8 -*- 
from logic import * 
 
# Ejercicio 1: KB: (P ∧ ¬Q) → R … ¿KB |= R? 
def ejercicio_1(): 
   P = Symbol("P") 
   Q = Symbol("Q") 
   R = Symbol("R") 
 
   kb = Implication(And(P, Not(Q)), R) 
   print("Ejercicio 1 - KB:", kb.formula()) 
   print("¿KB implica R?", model_check(kb, R)) 
 
 
# Ejercicio 2: KB: (A ∨ C) ∧ (B ∨ ¬C) … ¿KB |= (A ∨ B)? 
def ejercicio_2(): 
   A = Symbol("A") 
   B = Symbol("B") 
   C = Symbol("C") 
 
   kb = And(Or(A, C), Or(B, Not(C))) 
   print("Ejercicio 2 - KB:", kb.formula()) 
   print("¿KB implica (A ∨ B)?", model_check(kb, Or(A, B))) 
 
 
# Ejercicio 3: KB: (¬P → Q) ∧ (Q ∨ R) ∧ ¬(Q ∧ R) ∧ R … ¿KB |= ¬Q? 
def ejercicio_3(): 
   P = Symbol("P") 
   Q = Symbol("Q") 
   R = Symbol("R") 
 
   kb = And( 
       Implication(Not(P), Q), 
       Or(Q, R), 
       Not(And(Q, R)), 
       R 
   ) 
   print("Ejercicio 3 - KB:", kb.formula()) 
   print("¿KB implica ¬Q?", model_check(kb, Not(Q))) 
 
 
# Llamada a las funciones de los ejercicios 
if __name__ == "__main__": 
   ejercicio_1() 
print()  # Espacio entre resultados 
ejercicio_2() 
print()  # Espacio entre resultados 
ejercicio_3() 