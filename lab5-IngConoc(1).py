# V1
from logic import *


A = Symbol("tiene dolor de garganta")
B = Symbol("tiene fiebre")
C = Symbol("tiene tos")
D = Symbol("tiene resfriado")
E = Symbol("tiene alergia")
F = Symbol("TIENE GRIPE")

kb = And()

kb1 = Implication(A,Not(B))
kb2 = Implication(And(A,C,Not(B)),D)
kb3 = Implication(And(A,Not(C),Not(B)),E)
kb4 = Implication(And(B,A,C),F)

# Consulta: f ∨ D V E
query2 = Or(F,D,E)
query0 = F
query1 = D
query3 = E
print("KB |= R ?", model_check(kb1, query2))
print("KB |= R ?", model_check(kb2, query2))
print("KB |= R ?", model_check(kb3, query2))
print("KB |= R ?", model_check(kb4, query2))
