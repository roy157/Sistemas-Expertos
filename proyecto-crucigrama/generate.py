import sys # Se importa 'sys' para poder leer argumentos pasados al script por la terminal.
from collections import deque # Se importa 'deque', una lista optimizada para añadir y quitar elementos de los extremos (cola).

from crossword import * # Se importan las clases y funciones del archivo 'crossword.py'.

class CrosswordCreator():

    def __init__(self, crossword):
        """Constructor de la clase. Se ejecuta al crear un objeto CrosswordCreator."""
        # Almacena el objeto 'crossword', que contiene la estructura, variables y palabras del problema.
        self.crossword = crossword
        
        # self.domains son los dominios que debe tener cada variable. Pueden ser números o letras.
        # Para este ejemplo, cada variable (un espacio del crucigrama) se mapea a un conjunto de palabras.
        # Si se quisiera trabajar con una matriz o tablero, esta estructura se modificaría: las claves podrían ser
        # tuplas (fila, columna) y el valor de cada una sería un conjunto de números, como {1, 2,..., 9}.
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """Crea una matriz 2D de caracteres a partir de una asignación."""
        # Crea una matriz vacía del tamaño del crucigrama. Si en tu caso el problema no es visual
        # o la estructura es una simple matriz 9x9, esta función podría no ser necesaria o se
        # adaptaría para simplemente preparar una matriz de números para imprimir.
        letters = [[None for _ in range(self.crossword.width)] for _ in range(self.crossword.height)]
        # Rellena la matriz con las letras de cada palabra asignada.
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """Imprime una representación del crucigrama en la terminal."""
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """Guarda la asignación del crucigrama como un archivo de imagen."""
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)
       
       
        img = Image.new("RGBA", (self.crossword.width * cell_size, self.crossword.height * cell_size), "black")
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [(j * cell_size + cell_border, i * cell_size + cell_border), ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text((rect[0][0] + ((interior_size - w) / 2), (rect[0][1] + ((interior_size - h) / 2) - 10)), letters[i][j], fill="black", font=font)
        img.save(filename)

    def solve(self):
        """Orquesta la resolución: simplifica el problema y luego busca la solución."""
        self.enforce_node_consistency() # 1. Aplica restricciones unarias (pre-procesamiento).
        self.ac3()                      # 2. Aplica inferencia para reducir dominios.
        return self.backtrack(dict())   # 3. Inicia la búsqueda inteligente.

    def enforce_node_consistency(self):
        """Asegura que cada valor del dominio de una variable cumpla su restricción unaria (la de sí misma)."""
        # Itera sobre cada variable del problema.
        for var in self.domains:
            # Reemplaza su dominio con un nuevo conjunto que solo contiene los valores que cumplen la regla.
            # En un problema de tablero con números ya puestos, la lógica se modificaría para que si
            # una celda (variable) tiene un valor inicial, su dominio se reduzca únicamente a ese valor.
            self.domains[var] = {word for word in self.domains[var] if len(word) == var.length}

    def revise(self, x, y):
        """Hace que la variable X sea consistente en arco con la variable Y."""
        revised = False # Bandera para saber si el dominio de X fue modificado.
        # Obtiene la restricción entre X e Y. En este problema es un solapamiento.
        # En un problema de tablero, la "restricción" sería que son vecinas y deben ser diferentes.
        overlap = self.crossword.overlaps.get((x, y))
        if not overlap: return False
        
        i, j = overlap # Índices de las letras que deben coincidir.
        
        words_to_remove = set() # Conjunto para guardar valores inconsistentes.
        for word_x in self.domains[x]:
            # Busca si existe al menos una palabra de soporte en el dominio de Y.
            # Para un tablero, la condición se modificaría a algo como `any(word_x != word_y for word_y in self.domains[y])`
            has_support = any(word_x[i] == word_y[j] for word_y in self.domains[y])
            # Si no hay soporte, el valor es imposible y se debe eliminar.
            if not has_support:
                words_to_remove.add(word_x)

        if words_to_remove: # Si se encontraron valores para eliminar...
            self.domains[x] -= words_to_remove # ...se eliminan del dominio de X.
            revised = True # ...y se marca que hubo una revisión.
        return revised # Devuelve si se hizo o no una revisión.

    def ac3(self, arcs=None):
        """
        Algoritmo AC-3. Es el motor de inferencia que propaga restricciones.
        Su uso es clave para la eficiencia: al asignar un número a una celda, se llamaría a AC-3
        con los arcos entre esa celda y sus vecinas para podar las opciones del resto del tablero.
        """
        queue = deque(arcs if arcs is not None else self.crossword.overlaps.keys())
        while queue:
            x, y = queue.popleft()
            if self.revise(x, y): # Si el dominio de X se reduce...
                if not self.domains[x]: return False # ...y queda vacío, no hay solución.
                # ...todos los vecinos de X deben ser re-evaluados con respecto a X.
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True # Si la cola se vacía, la consistencia se logró.

    def assignment_complete(self, assignment):
        """Devuelve True si la asignación está completa (todas las variables tienen valor)."""
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Verifica si una asignación parcial es consistente con todas las reglas.
        Para un problema de tablero, la lógica de esta función cambiaría. En lugar de verificar
        solapamientos de letras, se modificaría para comprobar que un número no se repite
        en su fila, columna o bloque correspondiente.
        """
        # 1. Chequeo de unicidad: todas las palabras asignadas deben ser diferentes.
        if len(set(assignment.values())) != len(assignment.values()): return False
        
        # 2. Chequeo de cada variable asignada.
        for var, word in assignment.items():
            # Restricción unaria: longitud correcta.
            if var.length != len(word): return False
            # Restricción binaria: sin conflictos con vecinos.
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if word[i] != assignment[neighbor][j]: return False
        return True # Si pasa todas las pruebas, es consistente.

    def order_domain_values(self, var, assignment):
        """Heurística LCV (Least-Constraining Value). Ordena los valores a probar."""
        # Devuelve una lista de valores ordenada por cuál restringe menos las opciones de las variables vecinas.
        return sorted(self.domains[var], key=lambda value: sum(1 for neighbor in self.crossword.neighbors(var) if neighbor not in assignment and value in self.domains[neighbor]))

    def select_unassigned_variable(self, assignment):
        """
        Elige la mejor variable a asignar a continuación, usando heurísticas.
        Esta función es crítica para la eficiencia en problemas complejos como los de tablero.
        """
        unassigned_vars = [v for v in self.crossword.variables if v not in assignment]
        # Elige la variable con: 1. Menos valores restantes (MRV), y 2. Mayor grado (más vecinos) como desempate.
        # Para un problema de tablero, la heurística MRV es la más potente y recomendada.
        return min(unassigned_vars, key=lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))))

    def backtrack(self, assignment):
        """Búsqueda recursiva por backtracking, optimizada con heurísticas."""
        if self.assignment_complete(assignment): return assignment # Caso base: éxito.
        var = self.select_unassigned_variable(assignment) # Elige la variable más prometedora.
        for value in self.order_domain_values(var, assignment): # Itera sobre los valores más prometedores.
            assignment[var] = value # Intenta una asignación.
            if self.consistent(assignment): # Comprueba si es válida.
                result = self.backtrack(assignment) # Si lo es, continúa la búsqueda.
                if result: return result # Si la búsqueda hija tuvo éxito, retorna la solución.
            del assignment[var] # Si no, deshaz la asignación para probar otro valor.
        return None # Si ningún valor funcionó, esta rama falla.

def main():
    """Función principal que maneja la ejecución del script desde la terminal."""
    if len(sys.argv) not in [3, 4]: # Comprueba que el número de argumentos sea correcto.
        sys.exit("Usage: python generate.py structure words [output]")

    # Parsea los argumentos de la línea de comandos.
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Crea el objeto Crossword con los archivos de entrada.
    crossword = Crossword(structure, words)
    # Crea el objeto CrosswordCreator que resolverá el problema.
    creator = CrosswordCreator(crossword)
    # Llama al método solve para obtener la asignación final.
    assignment = creator.solve()

    # Muestra el resultado final.
    if assignment is None:
        print("No solution.") # Si no se encontró solución.
    else:
        creator.print(assignment) # Si se encontró, se imprime.
        if output: # Y si se especificó, se guarda como imagen.
            creator.save(assignment, output)

# Punto de entrada estándar de un script de Python.
if __name__ == "__main__":
    main()