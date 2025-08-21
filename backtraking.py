import random

random.seed(10) # Reemplazar con los 2 últimos dígitos de tu código

"""
Búsqueda backtracking simple sin heurísticas o inferencia.
"""

VALORES = ["Lunes", "Martes", "Miércoles"]
VARIABLES = ["Gest. Tecn. Inf.", "Intel. Art.", "Elect. II", "Sist.Exper.", "Mét. Cuant. Inv.", "Taller Tesis I", "Pract. Pre-Prof."]
RESTRICCIONES = [
    ("Gest. Tecn. Inf.", "Intel. Art."),
    ("Gest. Tecn. Inf.", "Elect. II"),
    ("Intel. Art.", "Elect. II"),
    ("Intel. Art.", "Sist.Exper."),
    ("Intel. Art.", "Mét. Cuant. Inv."),
    ("Elect. II", "Mét. Cuant. Inv."),
    ("Elect. II", "Taller Tesis I"),
    ("Sist.Exper.", "Mét. Cuant. Inv."),
    ("Mét. Cuant. Inv.", "Taller Tesis I"),
    ("Mét. Cuant. Inv.", "Pract. Pre-Prof."),
    ("Taller Tesis I", "Pract. Pre-Prof.")
]

# Las llamadas a random.shuffle() se han eliminado para una ejecución predecible
# random.shuffle(VALORES)
# random.shuffle(VARIABLES)
# random.shuffle(RESTRICCIONES)

def backtrack(asignacion):
    """Ejecuta la búsqueda backtracking para encontrar una asignación."""
    # Revisa si la asignación está completa
    if len(asignacion) == len(VARIABLES):
        return asignacion

    # Prueba una nueva variable
    var = seleccionar_variable_no_asignada(asignacion)
    for valor in VALORES:
        nueva_asignacion = asignacion.copy()
        nueva_asignacion[var] = valor
        if es_consistente(nueva_asignacion):
            resultado = backtrack(nueva_asignacion)
            if resultado is not None:
                return resultado
    return None

def seleccionar_variable_no_asignada(asignacion):
    """Elige una variable que no ha sido usada, en orden."""
    for variable in VARIABLES:
        if variable not in asignacion:
            return variable
    return None

def es_consistente(asignacion):
    """Revisa si una asignación es consistente."""
    for (x, y) in RESTRICCIONES:
        # Solo considera arcos si ambas variables han sido asignadas
        if x in asignacion and y in asignacion:
            # Si ambos tienen el mismo valor, entonces no es consistente
            if asignacion[x] == asignacion[y]:
                return False

    # Si nada es inconsistente, entonces el horario es consistente
    return True

solution = backtrack(dict())
print(solution)