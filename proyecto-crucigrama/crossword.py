class Variable():
    # Esta clase es como una plantilla para definir qué es una "variable" en nuestro problema.
    # En este caso, una variable es un espacio donde va una palabra (ej: 4-Horizontal).

    # Define constantes de clase para la dirección, para evitar usar strings directamente y prevenir errores.
    ACROSS = "across" # Constante para palabras horizontales.
    DOWN = "down"     # Constante para palabras verticales.

    def __init__(self, i, j, direction, length):
        """Constructor de la clase. Se llama al crear una nueva Variable."""
        # 'i' es la fila inicial de la variable (la coordenada Y).
        self.i = i
        # 'j' es la columna inicial de la variable (la coordenada X).
        self.j = j
        # 'direction' es la orientación de la palabra (ACROSS o DOWN).
        self.direction = direction
        # 'length' es el número de celdas que ocupa la palabra.
        self.length = length
        # 'self.cells' es una lista que almacenará las coordenadas (fila, col) de cada celda que ocupa esta variable.
        self.cells = []
        
        # Este bucle calcula las coordenadas de todas las celdas de la variable.
        for k in range(self.length):
            # Añade una tupla de coordenadas (fila, columna) a la lista 'cells'.
            self.cells.append(
                # El cálculo de la fila: si la dirección es DOWN, la fila aumenta con cada letra 'k'. Si no, se mantiene igual.
                (self.i + (k if self.direction == Variable.DOWN else 0),
                 # El cálculo de la columna: si la dirección es ACROSS, la columna aumenta. Si no, se mantiene igual.
                 self.j + (k if self.direction == Variable.ACROSS else 0))
            )
        # Si tu problema fuera un tablero numérico, una "variable" podría ser mucho más simple. No necesitaría
        # dirección, longitud o lista de celdas. La variable podría ser simplemente la tupla de su coordenada,
        # por ejemplo: variable_sudoku = (fila, columna).

    def __hash__(self):
        """Define cómo "hashear" un objeto Variable. Es esencial para poder usarlo en un conjunto (set) o como clave en un diccionario."""
        # Devuelve un número único basado en los atributos inmutables de la variable.
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        """Define cuándo dos objetos Variable se consideran "iguales"."""
        # Dos variables son iguales si todos sus atributos principales (posición, dirección, longitud) son idénticos.
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.direction == other.direction) and
            (self.length == other.length)
        )
    # En un problema donde la variable es una simple tupla como (fila, columna), no necesitarías escribir
    # los métodos __hash__ y __eq__, ya que las tuplas ya saben cómo hacerlo por defecto.

    def __str__(self):
        """Define la representación en string del objeto, para cuando se imprime (print)."""
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        """Define la representación "oficial" del objeto, útil para depuración."""
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():
    # Esta clase modela todo el problema del crucigrama en su conjunto.
    # Contiene la estructura, el vocabulario, las variables y las restricciones (solapamientos).

    def __init__(self, structure_file, words_file):
        """Constructor de la clase. Carga y procesa los archivos de entrada para definir el problema."""

        # --- Determina la estructura del crucigrama a partir de un archivo ---
        # 'with open(...)' asegura que el archivo se cierre correctamente.
        with open(structure_file) as f:
            # Lee todas las líneas del archivo en una lista de strings.
            contents = f.read().splitlines()
            # La altura es el número de líneas.
            self.height = len(contents)
            # El ancho es la longitud de la línea más larga.
            self.width = max(len(line) for line in contents)

            # 'self.structure' será una matriz 2D (lista de listas) de booleanos.
            # True significa que es una celda para una letra, False es un bloque negro.
            self.structure = []
            # Itera sobre cada fila 'i'.
            for i in range(self.height):
                row = [] # Crea una nueva fila.
                # Itera sobre cada columna 'j'.
                for j in range(self.width):
                    # Si la columna 'j' está fuera de los límites de la línea actual...
                    if j >= len(contents[i]):
                        row.append(False) # ...es un espacio vacío (no parte de la estructura).
                    # Si el caracter en la posición (i, j) es un guion bajo...
                    elif contents[i][j] == "_":
                        row.append(True) # ...es una celda que debe ser rellenada.
                    # Si es cualquier otro caracter...
                    else:
                        row.append(False) # ...es un bloque negro.
                # Añade la fila completa a la estructura.
                self.structure.append(row)
        # Para un tablero numérico, este bloque sería similar, pero en lugar de True/False,
        # guardarías el número inicial (1-9) si la celda está rellena, o un 0 si está vacía.

        # --- Guarda la lista de palabras (el dominio inicial) ---
        with open(words_file) as f:
            # Lee las palabras, las convierte a mayúsculas y las guarda en un conjunto (set) para búsquedas rápidas.
            self.words = set(f.read().upper().splitlines())

        # --- Determina el conjunto de variables a partir de la estructura ---
        # 'self.variables' es un conjunto que almacenará todos los objetos Variable del crucigrama.
        self.variables = set()
        # Itera sobre cada celda de la rejilla para encontrar dónde empiezan las palabras.
        for i in range(self.height):
            for j in range(self.width):

                # Busca palabras verticales.
                # Una palabra vertical empieza si la celda es 'True' Y (está en la primera fila O la celda de arriba es 'False').
                starts_word = (
                    self.structure[i][j]
                    and (i == 0 or not self.structure[i - 1][j])
                )
                if starts_word:
                    # Si empieza una palabra, calcula su longitud mirando hacia abajo.
                    length = 1
                    for k in range(i + 1, self.height):
                        if self.structure[k][j]:
                            length += 1
                        else:
                            break # Se detiene cuando encuentra un bloque negro.
                    # Si la longitud es mayor que 1, es una variable válida.
                    if length > 1:
                        # Crea un objeto Variable y lo añade al conjunto de variables.
                        self.variables.add(Variable(
                            i=i, j=j, direction=Variable.DOWN, length=length
                        ))

                # Busca palabras horizontales (lógica idéntica pero en el eje X).
                starts_word = (
                    self.structure[i][j]
                    and (j == 0 or not self.structure[i][j - 1])
                )
                if starts_word:
                    length = 1
                    for k in range(j + 1, self.width):
                        if self.structure[i][k]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j, direction=Variable.ACROSS, length=length
                        ))
        # Para un problema de tablero, este bloque sería mucho más simple. Simplemente se recorrería
        # la matriz y se añadiría una variable por cada celda vacía.
        # Ejemplo: if tablero[i][j] == 0: self.variables.add((i, j))

        # --- Calcula los solapamientos (restricciones) entre cada par de palabras ---
        # self.overlaps es un diccionario donde se guardarán todas las restricciones binarias.
        self.overlaps = dict()
        # Itera sobre cada posible par de variables (v1, v2).
        for v1 in self.variables:
            for v2 in self.variables:
                # Una variable no se solapa consigo misma.
                if v1 == v2:
                    continue
                
                # Usa la intersección de conjuntos para ver si v1 y v2 comparten alguna celda.
                intersection = set(v1.cells).intersection(v2.cells)
                
                # Si la intersección está vacía, no hay solapamiento.
                if not intersection:
                    self.overlaps[v1, v2] = None
                # Si hay intersección (debe ser una única celda)...
                else:
                    # ...obtiene la celda de intersección.
                    intersection = intersection.pop()
                    # ...y guarda la restricción. El valor es una tupla (i, j) que significa:
                    # "la i-ésima letra de v1 debe ser igual a la j-ésima letra de v2".
                    self.overlaps[v1, v2] = (
                        v1.cells.index(intersection),
                        v2.cells.index(intersection)
                    )
        # Para un problema de tablero, este bloque se reemplazaría por una lógica que define a los "vecinos".
        # No habría "solapamiento", la restricción sería simplemente "diferente de". Se crearía un diccionario
        # donde la clave es una celda y el valor es un conjunto de todas las celdas en su misma fila, columna y bloque.

    def neighbors(self, var):
        """Dado una variable, devuelve el conjunto de todas las variables que se solapan con ella."""
        # Esta es una función de ayuda para obtener fácilmente los vecinos de una variable.
        # Devuelve un conjunto de variables 'v' que son diferentes a 'var' y tienen
        # una entrada de solapamiento (una restricción) en el diccionario 'self.overlaps'.
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var]
        )
        # Para un problema de tablero, esta función sería esencial. Dado una celda (fila, col),
        # devolvería el conjunto de todas las otras celdas en la misma fila, columna y bloque 3x3.