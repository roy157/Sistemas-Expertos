# Este script Python resuelve un Sudoku utilizando el algoritmo de backtracking.
# El tablero del Sudoku se define directamente dentro de este archivo.

# --- Configuración_Inicial_del_Juego ---
# Los_digitos_validos_para_rellenar_una_celda (como texto).
DIGITOS_VALIDOS = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

# La_dimensión_del_tablero_de_Sudoku (siempre es 9).
DIMENSION = 9 

# El_tablero_inicial_del_rompecabezas.
# '0' o '_' representan celdas vacías (se convertirán a 'None').
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

# --- Funciones_Clave_del_Algoritmo ---

def encontrar_siguiente_vacio(tablero_actual):
    """
    Busca la próxima celda vacía (None) en el tablero.
    Retorna (indice_fila, indice_columna) o None si el_tablero_esta_lleno.
    """
    for indice_fila in range(DIMENSION):
        for indice_columna in range(DIMENSION):
            if tablero_actual[indice_fila][indice_columna] is None:
                return indice_fila, indice_columna
    return None # Todo_lleno

def es_movimiento_posible(tablero_actual, numero_a_poner, posicion_celda):
    """
    Verifica si 'numero_a_poner' es valido en 'posicion_celda'
    segun_las_reglas_del_Sudoku (fila, columna, y bloque_3x3).
    """
    f_celda, c_celda = posicion_celda # f_celda = fila_actual_de_la_celda, c_celda = columna_actual_de_la_celda

    # Comprobar_FILA
    for c_idx in range(DIMENSION): # c_idx = indice_de_columna
        if tablero_actual[f_celda][c_idx] == numero_a_poner and c_idx != c_celda:
            return False 

    # Comprobar_COLUMNA
    for f_idx in range(DIMENSION): # f_idx = indice_de_fila
        if tablero_actual[f_idx][c_celda] == numero_a_poner and f_idx != f_celda:
            return False 

    # Comprobar_BLOQUE_3x3
    inicio_f_bloque = (f_celda // 3) * 3 # inicio_f_bloque = inicio_de_fila_del_bloque
    inicio_c_bloque = (c_celda // 3) * 3 # inicio_c_bloque = inicio_de_columna_del_bloque

    for i_b_fila in range(inicio_f_bloque, inicio_f_bloque + 3): # i_b_fila = indice_fila_dentro_del_bloque
        for i_b_col in range(inicio_c_bloque, inicio_c_bloque + 3): # i_b_col = indice_columna_dentro_del_bloque
            if tablero_actual[i_b_fila][i_b_col] == numero_a_poner and (i_b_fila, i_b_col) != posicion_celda:
                return False 

    return True # Es_posible

def resolver_backtracking(tablero_actual):
    """
    Aplica el algoritmo recursivo de backtracking para encontrar_la_solucion_del_Sudoku.
    Modifica 'tablero_actual' directamente.
    Retorna True si hay_solucion, False si no_hay_solucion.
    """
    
    posicion_vacia = encontrar_siguiente_vacio(tablero_actual)

    if posicion_vacia is None:
        return True # Sudoku_resuelto
    
    f_vacia, c_vacia = posicion_vacia # f_vacia = fila_vacia, c_vacia = columna_vacia

    for num_candidato in DIGITOS_VALIDOS:
        if es_movimiento_posible(tablero_actual, num_candidato, (f_vacia, c_vacia)):
            tablero_actual[f_vacia][c_vacia] = num_candidato # Colocar_numero

            if resolver_backtracking(tablero_actual):
                return True # Solucion_encontrada
            
            tablero_actual[f_vacia][c_vacia] = None # Deshacer_movimiento (backtrack)

    return False # No_hay_solucion_desde_aqui

# --- Función_para_Mostrar_el_Tablero ---
def imprimir_tablero_en_consola(tablero_a_mostrar):
    """
    Imprime el tablero de Sudoku con formato visual (líneas divisorias).
    """
    for f_idx in range(DIMENSION): # f_idx = indice_de_fila
        if f_idx % 3 == 0 and f_idx != 0:
            print("- - - - - - - - - - -") 
        for c_idx in range(DIMENSION): # c_idx = indice_de_columna
            if c_idx % 3 == 0 and c_idx != 0:
                print("| ", end="")
            print(tablero_a_mostrar[f_idx][c_idx] if tablero_a_mostrar[f_idx][c_idx] is not None else " ", end=" ")
        print() 

# --- Bloque_de_Ejecucion_Principal ---
if __name__ == "__main__":
    # Preparamos_el_tablero_para_el_algoritmo (cambiar '0' o '_' a 'None').
    tablero_para_trabajar = []
    for fila_str in tablero_inicial:
        fila_convertida = []
        for celda_char in fila_str:
            fila_convertida.append(celda_char if celda_char in DIGITOS_VALIDOS else None)
        tablero_para_trabajar.append(fila_convertida)

    print("Tablero_inicial_del_Sudoku:")
    imprimir_tablero_en_consola(tablero_para_trabajar)
    
    print("\nIniciando_resolucion...")

    if resolver_backtracking(tablero_para_trabajar):
        print("\n¡Sudoku_Resuelto_con_exito!")
        imprimir_tablero_en_consola(tablero_para_trabajar)
    else:
        print("\nNo_se_encontro_solucion_para_este_Sudoku.")