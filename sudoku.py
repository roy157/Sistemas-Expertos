# No necesita 'sys' si el tablero se define aquí.

# --- Configuración Básica del Sudoku ---
VALORES = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
T = 9 # Tamaño

# Tablero de ejemplo directamente en el código (0 o '_' como None)
# Puedes cambiar este tablero para probar otros Sudokus
tablero_inicial = [
    ['0','0','3','0','2','0','6','0','0'],
    ['9','0','0','3','0','5','0','0','1'],
    ['0','0','1','8','0','6','4','0','0'],
    ['0','0','8','1','0','2','9','0','0'],
    ['7','0','0','0','0','0','0','0','8'],
    ['0','0','6','7','0','8','2','0','0'],
    ['0','0','2','6','0','9','5','0','0'],
    ['8','0','0','2','0','3','0','0','9'],
    ['0','0','5','0','1','0','3','0','0']
]

# --- Funciones Esenciales ---

def siguiente_vacio(b):
    for r in range(T):
        for c in range(T):
            if b[r][c] is None: return r, c
    return None

def es_valido(b, num, pos):
    r, c = pos
    for x in range(T): # Fila y Columna
        if b[r][x] == num and x != c: return False
        if b[x][c] == num and x != r: return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3): # Bloque 3x3
        for j in range(bc, bc + 3):
            if b[i][j] == num and (i, j) != pos: return False
    return True

def resolver(b):
    vacio = siguiente_vacio(b)
    if not vacio: return True
    r, c = vacio
    for num in VALORES:
        if es_valido(b, num, (r, c)):
            b[r][c] = num
            if resolver(b): return True
            b[r][c] = None
    return False

# --- Preparación y Ejecución ---

# Convertir el tablero_inicial a la representación con None
tablero = []
for fila_str in tablero_inicial:
    fila_convertida = []
    for char in fila_str:
        fila_convertida.append(char if char in VALORES else None)
    tablero.append(fila_convertida)

print("Tablero inicial:")
for r in range(T): # Imprimir inicial
    if r % 3 == 0 and r != 0: print("- - - - - - - - - - -")
    for c in range(T):
        if c % 3 == 0 and c != 0: print("| ", end="")
        print(tablero[r][c] if tablero[r][c] is not None else " ", end=" ")
    print()

print("\nResolviendo...")
if resolver(tablero):
    print("\n¡Resuelto!")
    for r in range(T): # Imprimir final
        if r % 3 == 0 and r != 0: print("- - - - - - - - - - -")
        for c in range(T):
            if c % 3 == 0 and c != 0: print("| ", end="")
            print(tablero[r][c], end=" ")
        print()
else:
    print("\nSin solución.")