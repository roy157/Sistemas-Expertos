def ver(tablero, fila, col, num):
	if num in tablero[fila]:
		return False

	for i in range(4):
		if tablero[i][col] == num:
			return False

	inicio_fila = (fila // 2) * 2 
	inicio_col = (col // 2)* 2
	for i in range(inicio_fila, inicio_fila +2):
		for j in range(inicio_col, inicio_col +2):
			if tablero[i][j] == num:
				return False
	return True
	


def backtracking(tablero):
	for i in range(4):
		for j in range(4):
			if tablero[i][j] == 0:
				for num in range(1,5):
					if ver(tablero,i,j,num):
						tablero[i][j] = num
						if backtracking(tablero):
							return True
						tablero[i][j] = 0 #aqui hacemos back
				return False
	return True			




def imprimir(tablero):
    for fila in tablero:
        print(fila)


tablero = [
	[2,0,0,3],
	[0,0,0,1],
	[1,0,0,0],
	[3,0,0,2]
]


print("SOLCUION DEL MINI-SUDOKU:")
print("ENTRADA:")
for fila in tablero:
	print(fila)

print("SALIDA:")

if backtracking(tablero):
	imprimir(tablero)
else:
	print("no hay solucion")
