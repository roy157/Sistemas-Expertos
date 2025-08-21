from logic import *

# Declaración de símbolos (síntomas y enfermedades)
fiebre = Symbol("fiebre")
garganta = Symbol("dolor de garganta")
tos = Symbol("tos")
resfriado = Symbol("resfriado")
alergia = Symbol("alergia")
gripe = Symbol("gripe")

# Base de conocimiento (reglas médicas)
kb = And(
    Implication(And(garganta, tos, Not(fiebre)), resfriado),
    Implication(And(garganta, Not(tos), Not(fiebre)), alergia),
    Implication(And(fiebre, garganta, tos), gripe)
)

# Preguntar síntomas al usuario
entrada = input("Ingresa tus síntomas separados por comas (ej: fiebre, tos): ").lower()

# Crear una lista de síntomas verdaderos según entrada del usuario
hechos = []
if "fiebre" in entrada:
    hechos.append(fiebre)
if "dolor de garganta" in entrada or "garganta" in entrada:
    hechos.append(garganta)
if "tos" in entrada:
    hechos.append(tos)

# Mostrar diagnóstico basado en la base de conocimiento
print("\nDiagnóstico posible:")
if model_check(And(kb, *hechos), gripe):
    print("- Gripe")
if model_check(And(kb, *hechos), resfriado):
    print("- Resfriado")
if model_check(And(kb, *hechos), alergia):
    print("- Alergia")
if not (model_check(And(kb, *hechos), gripe) or model_check(And(kb, *hechos), resfriado) or model_check(And(kb, *hechos), alergia)):
    print("No se pudo determinar una enfermedad con los síntomas dados.")
