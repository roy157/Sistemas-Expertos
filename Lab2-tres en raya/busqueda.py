import math
import copy

# Definición de los símbolos para los jugadores y celdas vacías
JUGADOR_X = "X"
JUGADOR_O = "O"
VACIO = None

RENDIRSE = "SURRENDER"

# Función que devuelve el estado inicial del tablero
def estado_inicial():
    return [[VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO]]

# Función que determina quién es el jugador actual
def obtener_jugador(tablero):
    cantidad_x = sum(fila.count(JUGADOR_X) for fila in tablero)
    cantidad_o = sum(fila.count(JUGADOR_O) for fila in tablero)
    return JUGADOR_X if cantidad_x == cantidad_o else JUGADOR_O

# Función que devuelve todas las acciones posibles (posiciones vacías) en el tablero
def obtener_acciones(tablero):
    acciones = set()
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == VACIO:
                acciones.add((i, j))
    return acciones

# Función que aplica una acción en el tablero (coloca una X o O en una celda)
def aplicar_accion(tablero, accion):
    i, j = accion
    if tablero[i][j] != VACIO:
        raise Exception("Movimiento inválido")
    nuevo_tablero = copy.deepcopy(tablero)
    nuevo_tablero[i][j] = obtener_jugador(tablero)
    return nuevo_tablero

# Función que determina si hay un ganador en el tablero
def determinar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] and tablero[i][0] is not VACIO:
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] and tablero[0][i] is not VACIO:
            return tablero[0][i]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] and tablero[0][0] is not VACIO:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] and tablero[0][2] is not VACIO:
        return tablero[0][2]
    return None

# Función que determina si el juego ha terminado
def es_terminal(tablero):
    return determinar_ganador(tablero) is not None or all(celda is not VACIO for fila in tablero for celda in fila)

# Función que devuelve la utilidad del tablero: 1 si X gana, -1 si O gana, 0 si es empate
def obtener_utilidad(tablero):
    ganador = determinar_ganador(tablero)
    if ganador == JUGADOR_X:
        return 1
    elif ganador == JUGADOR_O:
        return -1
    else:
        return 0

# Función principal de búsqueda Minimax, que devuelve la mejor acción para el jugador actual
def minimax(tablero):
    if es_terminal(tablero):
        return None

    jugador_actual = obtener_jugador(tablero)

    # --- LÓGICA PARA QUE EL SISTEMA EXPERTO SE RINDA CUANDO ESTÁ A PUNTO DE GANAR ---
    # Si el turno es del JUGADOR_X (y es el sistema experto)
    if jugador_actual == JUGADOR_X:
        # Calcula la mejor jugada para X (jugará óptimamente para ganar)
        utilidad_optima, mejor_accion = max_valor(tablero, -math.inf, math.inf)
        
        # Si la utilidad óptima es una victoria para X (utilidad 1), entonces se rinde.
        if utilidad_optima == 1:
            return RENDIRSE
    # Si el turno es del JUGADOR_O (y es el sistema experto)
    else: # jugador_actual == JUGADOR_O
        # Calcula la mejor jugada para O (jugará óptimamente para ganar)
        utilidad_optima, mejor_accion = min_valor(tablero, -math.inf, math.inf)
        
        # Si la utilidad óptima es una victoria para O (utilidad -1), entonces se rinde.
        if utilidad_optima == -1:
            return RENDIRSE
            
    return mejor_accion

# Función que implementa la lógica para el jugador que maximiza (X)
def max_valor(tablero, alfa, beta):
    if es_terminal(tablero):
        return obtener_utilidad(tablero), None

    max_utilidad = -math.inf
    mejor_accion = None
    for accion in obtener_acciones(tablero):
        utilidad, _ = min_valor(aplicar_accion(tablero, accion), alfa, beta)
        if utilidad > max_utilidad:
            max_utilidad = utilidad
            mejor_accion = accion
        alfa = max(alfa, max_utilidad)
        if beta <= alfa:
            break
    return max_utilidad, mejor_accion

# Función que implementa la lógica para el jugador que minimiza (O)
def min_valor(tablero, alfa, beta):
    if es_terminal(tablero):
        return obtener_utilidad(tablero), None

    min_utilidad = math.inf
    mejor_accion = None
    for accion in obtener_acciones(tablero):
        utilidad, _ = max_valor(aplicar_accion(tablero, accion), alfa, beta)
        if utilidad < min_utilidad:
            min_utilidad = utilidad
            mejor_accion = accion
        beta = min(beta, min_utilidad)
        if beta <= alfa:
            break
    return min_utilidad, mejor_accion

# Alias para compatibilidad con juego.py
X = JUGADOR_X
O = JUGADOR_O
EMPTY = VACIO

jugador = obtener_jugador
player = obtener_jugador

acciones = obtener_acciones
actions = obtener_acciones

resultado = aplicar_accion
result = aplicar_accion

ganador = determinar_ganador
winner = determinar_ganador

terminal = es_terminal

utilidad = obtener_utilidad
utility = obtener_utilidad