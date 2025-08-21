import math
import copy

# Definición de los símbolos para los jugadores y celdas vacías
JUGADOR_X = "X"
JUGADOR_O = "O"
VACIO = None

# Función que devuelve el estado inicial del tablero
def estado_inicial():
    # El tablero es una lista de listas con valores vacíos (None)
    return [[VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO]]

# Función que determina quién es el jugador actual
def obtener_jugador(tablero):
    # Contamos la cantidad de X y O en el tablero
    cantidad_x = sum(fila.count(JUGADOR_X) for fila in tablero)
    cantidad_o = sum(fila.count(JUGADOR_O) for fila in tablero)
    # El jugador que tiene el turno es el que tiene menos piezas en el tablero
    return JUGADOR_X if cantidad_x == cantidad_o else JUGADOR_O

# Función que devuelve todas las acciones posibles (posiciones vacías) en el tablero
def obtener_acciones(tablero):
    acciones = set()  # Usamos un set para evitar duplicados
    for i in range(3):  # Recorremos el tablero de 3x3
        for j in range(3):
            if tablero[i][j] == VACIO:
                acciones.add((i, j))  # Añadimos la posición vacía como una acción posible
    return acciones

# Función que aplica una acción en el tablero (coloca una X o O en una celda)
def aplicar_accion(tablero, accion):
    i, j = accion
    # Verificamos si la celda ya está ocupada
    if tablero[i][j] != VACIO:
        raise Exception("Movimiento inválido")
    # Creamos una copia del tablero para no modificar el original
    nuevo_tablero = copy.deepcopy(tablero)
    nuevo_tablero[i][j] = obtener_jugador(tablero)  # Colocamos la pieza del jugador actual
    return nuevo_tablero

# Función que determina si hay un ganador en el tablero
def determinar_ganador(tablero):
    # Revisamos filas y columnas para detectar una línea ganadora
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] and tablero[i][0] is not VACIO:
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] and tablero[0][i] is not VACIO:
            return tablero[0][i]
    # Revisamos las diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] and tablero[0][0] is not VACIO:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] and tablero[0][2] is not VACIO:
        return tablero[0][2]
    return None  # No hay ganador

# Función que determina si el juego ha terminado
def es_terminal(tablero):
    # El juego ha terminado si hay un ganador o si el tablero está lleno
    return determinar_ganador(tablero) is not None or all(celda is not VACIO for fila in tablero for celda in fila)

# Función que devuelve la utilidad del tablero: 1 si X gana, -1 si O gana, 0 si es empate
def obtener_utilidad(tablero):
    ganador = determinar_ganador(tablero)
    if ganador == JUGADOR_X:
        return 1  # X gana
    elif ganador == JUGADOR_O:
        return -1  # O gana
    else:
        return 0  # Empate

# Función principal de búsqueda Minimax, que devuelve la mejor acción para el jugador actual
def minimax(tablero):
    if es_terminal(tablero):
        return None  # Si el juego ha terminado, no hay acción que tomar

    jugador_actual = obtener_jugador(tablero)

    if jugador_actual == JUGADOR_X:
        # Si el turno es de X, llamamos a max_valor
        _, mejor_accion = max_valor(tablero, -math.inf, math.inf)
    else:
        # Si el turno es de O, llamamos a min_valor
        _, mejor_accion = min_valor(tablero, -math.inf, math.inf)
    return mejor_accion

# Función que implementa la lógica para el jugador que maximiza (X)
def max_valor(tablero, alfa, beta):
    if es_terminal(tablero):
        return obtener_utilidad(tablero), None  # Si el juego ha terminado, devolvemos la utilidad

    max_utilidad = -math.inf
    mejor_accion = None
    for accion in obtener_acciones(tablero):
        # Aplicamos la acción y evaluamos el valor con min_valor
        utilidad, _ = min_valor(aplicar_accion(tablero, accion), alfa, beta)
        if utilidad > max_utilidad:
            max_utilidad = utilidad
            mejor_accion = accion
        # Actualizamos alfa con el valor máximo encontrado
        alfa = max(alfa, max_utilidad)
        if beta <= alfa:
            break  # Poda: si el valor mínimo de O es menor o igual que alfa, no exploramos más
    return max_utilidad, mejor_accion

# Función que implementa la lógica para el jugador que minimiza (O)
def min_valor(tablero, alfa, beta):
    if es_terminal(tablero):
        return obtener_utilidad(tablero), None  # Si el juego ha terminado, devolvemos la utilidad

    min_utilidad = math.inf
    mejor_accion = None
    for accion in obtener_acciones(tablero):
        # Aplicamos la acción y evaluamos el valor con max_valor
        utilidad, _ = max_valor(aplicar_accion(tablero, accion), alfa, beta)
        if utilidad < min_utilidad:
            min_utilidad = utilidad
            mejor_accion = accion
        # Actualizamos beta con el valor mínimo encontrado
        beta = min(beta, min_utilidad)
        if beta <= alfa:
            break  # Poda: si el valor máximo de X es mayor o igual que beta, no exploramos más
    return min_utilidad, mejor_accion

# Alias para compatibilidad con juego.py
X = JUGADOR_X
O = JUGADOR_O
EMPTY = VACIO

# Alias de funciones para compatibilidad con el archivo juego.py
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
