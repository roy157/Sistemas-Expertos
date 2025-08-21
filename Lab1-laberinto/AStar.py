import sys

class Nodo():
    def __init__(self, estado, padre, accion, heuristica=0, costo=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.heuristica = heuristica
        self.costo = costo 

class Laberinto():

    def __init__(self, nombreArchivo):

        # Leer el archivo y establecer la altura y la anchura del laberinto
        with open(nombreArchivo) as f:
            contenido = f.read()

        # Validar el inicio y el objetivo
        if contenido.count("A") != 1:
            raise Exception("el laberinto debe tener exactamente un punto de partida")
        if contenido.count("B") != 1:
            raise Exception("el laberinto debe tener exactamente un objetivo")

        # Determinar la altura y la anchura del laberinto
        contenido = contenido.splitlines()
        self.altura = len(contenido)
        self.anchura = max(len(linea) for linea in contenido)
        self.explorado = set() #nuevo
        
        self.paredes = []
        for i in range(self.altura):
            fil = []
            for j in range(self.anchura):
                try:
                    if contenido[i][j] == "A":
                        self.inicio = (i, j)
                        fil.append(False)
                    elif contenido[i][j] == "B":
                        self.meta = (i, j)
                        fil.append(False)
                    elif contenido[i][j] == " ":
                        fil.append(False)
                    else:
                        fil.append(True)
                except IndexError:
                    fil.append(False)
            self.paredes.append(fil)

        self.solucion = None
        self.orden_exploracion = {}  # Almacenar el orden de exploración de todos los nodos


    def print(self):
        solucion = self.solucion[1] if self.solucion is not None else None
        print()
        for i, fil in enumerate(self.paredes):
            for j, col in enumerate(fil):
                if col:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.meta:
                    print("B", end="")
                elif solucion is not None and (i, j) in solucion:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def vecinos(self, estado):
        fil, col = estado
        candidatos = [
            ("arriba", (fil - 1, col)),
            ("abajo", (fil + 1, col)),
            ("izquierda", (fil, col - 1)),
            ("derecha", (fil, col + 1))
        ]

        resultado = []
        for accion, (r, c) in candidatos:
            if 0 <= r < self.altura and 0 <= c < self.anchura and not self.paredes[r][c]:
                resultado.append((accion, (r, c)))
        return resultado

    def solve(self):
        """Encuentra una solución al laberinto usando Greedy Best-First Search."""
            
        # Heurística: distancia Manhattan a la meta
        def h(estado):
            return abs(estado[0] - self.meta[0]) + abs(estado[1] - self.meta[1])

        self.numExplorados = 0
        inicio = Nodo(estado=self.inicio, padre=None, accion=None, heuristica=h(self.inicio), costo=0)

        frontera = [inicio]  
        
        # Registrar el nodo inicial como paso 0 en la exploración
        self.orden_exploracion[self.inicio] = 0

        while frontera:
            # Ordenar la frontera por la heurística
            frontera.sort(key=lambda n: n.costo + n.heuristica)

            # El primer nodo es el que tiene la heurística más baja
            nodo = frontera.pop(0)  
            
            # Registrar el número de exploración para este nodo
            if nodo.estado not in self.orden_exploracion:
                self.orden_exploracion[nodo.estado] = self.numExplorados
            
            self.numExplorados += 1

            # Si nodo es la meta, entonces tenemos una solucion
            if nodo.estado == self.meta:
                acciones = []
                celdas = []
                while nodo.padre is not None:
                    acciones.append(nodo.accion)
                    celdas.append(nodo.estado)
                    nodo = nodo.padre
                acciones.reverse()
                celdas.reverse()
                self.solucion = (acciones, celdas) 
                return

            # Marcar nodo como explorado
            self.explorado.add(nodo.estado)

            # Revisamos los vecinos
            for accion, estado in self.vecinos(nodo.estado):
                if estado not in self.explorado and estado not in [n.estado for n in frontera]:
                    heuristica_hijo = h(estado)  # Calculamos la heurística para el hijo
                    hijo = Nodo(estado=estado, padre=nodo, accion=accion, heuristica=heuristica_hijo, costo=nodo.costo + 1)
                    frontera.append(hijo)

        raise Exception("No hay solución")

    def imagen_salida(self, nombreArchivo, mostrar_solucion=True, mostrar_explorado=True):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.anchura * cell_size, self.altura * cell_size),
            "black"
        )
        dibujo = ImageDraw.Draw(img)
        
        # Intenta cargar una fuente 
        try:
            fuente = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            fuente = ImageFont.load_default()

        solucion = self.solucion[1] if self.solucion is not None else None
        for i, fil in enumerate(self.paredes):
            for j, col in enumerate(fil):
                # Determinar el color de fondo de la celda
                if col:
                    fill = (40, 40, 40)  # Paredes
                elif (i, j) == self.inicio:
                    fill = (255, 0, 0)  # Inicio
                elif (i, j) == self.meta:
                    fill = (0, 171, 28)  # Meta
                elif solucion is not None and mostrar_solucion and (i, j) in solucion:
                    fill = (220, 235, 113)  # Camino solución
                elif mostrar_explorado and (i, j) in self.explorado:
                    fill = (212, 97, 85)  # Explorado pero no en solución
                else:
                    fill = (237, 240, 252)  # Celda vacía

                # Dibujar celda
                dibujo.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
                
                # Mostrar movimiento secuencial en todas las celdas exploradas
                if (i, j) in self.orden_exploracion:
                    num_texto = str(self.orden_exploracion[(i, j)])
                    # Calcular posición para centrar el texto
                    text_width = dibujo.textlength(num_texto, font=fuente)
                    text_position = (
                        j * cell_size + (cell_size - text_width) / 2,
                        i * cell_size + (cell_size - 16) / 2  
                    )
                    # Dibujar el número del orden de exploración
                    dibujo.text(text_position, num_texto, fill=(0, 0, 0), font=fuente)

        img.save(nombreArchivo)


if len(sys.argv) != 2:
    sys.exit("Usage: python laberinto.py laberinto.txt")

m = Laberinto(sys.argv[1])
print("Laberinto:")
m.print()
print("Resolviendo...")
m.solve()
print("Estados Explorados:", m.numExplorados)
print("Solution:")
m.print()
m.imagen_salida("laberinto.png", mostrar_explorado=True)
