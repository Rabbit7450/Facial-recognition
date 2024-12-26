Algoritmo HundirElBarco
	Definir SIZE Como Entero
	Definir ships Como Entero
	SIZE <- 5
	ships <- 3
	Definir fila, columna Como Entero
	Definir playerBoard Como Cadena
	Dimensionar playerBoard(5,5)
	Definir opponentBoard Como Cadena
	Dimensionar opponentBoard(5,5)
	// Inicializar tableros con '~'
	Para i<-1 Hasta SIZE-1 Hacer
		Para j<-1 Hasta SIZE-1 Hacer
			playerBoard[i,j]<-'~'
			opponentBoard[i,j]<-'~'
		FinPara
	FinPara
	Escribir 'Selecciona el modo de juego:'
	Escribir '1. 1 vs 1'
	Escribir '2. Un jugador'
	Leer mode
	// Colocación de barcos del jugador
	Escribir 'Coloca tus barcos en el tablero.'
	ships <- ships
	Mientras ships>0 Hacer
		Escribir 'Ingresa las coordenadas del barco (fila columna): '
		Leer fila, columna
		Si fila>=1 Y fila<SIZE Y columna>=1 Y columna<SIZE Y playerBoard[fila,columna]='~' Entonces
			playerBoard[fila,columna]<-'B'
			ships <- ships-1 // Colocar un barco
		SiNo
			Escribir 'Posición inválida o ya ocupada. Intenta de nuevo.'
		FinSi
	FinMientras
	Si mode=1 Entonces
		// Colocación de barcos del oponente (jugador 2)
		Escribir 'Ahora, el oponente colocará sus barcos.'
		ships <- ships
		Mientras ships>0 Hacer
			Escribir 'Ingresa las coordenadas del barco del oponente (fila columna): '
			Leer fila, columna
			Si fila>=1 Y fila<SIZE Y columna>=1 Y columna<SIZE Y opponentBoard[fila,columna]='~' Entonces
				opponentBoard[fila,columna]<-'B'
				ships <- ships-1 // Colocar un barco
			SiNo
				Escribir 'Posición inválida o ya ocupada. Intenta de nuevo.'
			FinSi
		FinMientras
	SiNo
		// Colocación de barcos del oponente (computadora)
		Escribir 'La computadora colocará sus barcos.'
		ships <- ships
		Mientras ships>0 Hacer
			fila <- Aleatorio(1,SIZE-1)
			columna <- Aleatorio(1,SIZE-1)
			Si opponentBoard[fila,columna]='~' Entonces
				opponentBoard[fila,columna]<-'B'
				ships <- ships-1 // Colocar un barco
			FinSi
		FinMientras
	FinSi
	Escribir '¡Bienvenido a Hundir el barco!'
	Mientras Verdadero Hacer
		Definir x, n Como Entero
		Escribir 'Adivina las coordenadas del oponente (fila columna): '
		Leer x, n
		Si opponentBoard[x,n]='B' Entonces
			opponentBoard[x,n]<-'X'
			Escribir '¡Impacto!' // Impacto
		SiNo
			Si opponentBoard[x,n]='~' Entonces
				opponentBoard[x,n]<-'O'
				Escribir '¡Agua!' // Agua
			SiNo
				Escribir 'Ya has adivinado esas coordenadas. Intenta de nuevo.'
				// Regresar al inicio del bucle sin hacer nada
			FinSi
		FinSi
		// Comprobar si todos los barcos del oponente están hundidos
		Definir allSunk Como Lógico
		allSunk <- Verdadero
		Para i<-1 Hasta SIZE-1 Hacer
			Para j<-1 Hasta SIZE-1 Hacer
				Si opponentBoard[i,j]='B' Entonces
					allSunk <- Falso
				FinSi
			FinPara
		FinPara
		Si allSunk Entonces
			Escribir '¡Has hundido todos los barcos del oponente!'
			// Terminar el juego
			Escribir 'Fin del juego.'
			i <- SIZE
		FinSi // Esto termina el bucle principal
		// Mostrar el tablero del oponente
		Escribir 'Tablero del oponente:'
		Escribir '  0 1 2 3 4'
		Para i<-1 Hasta SIZE-1 Hacer
			Escribir i, ' '
			Para j<-1 Hasta SIZE-1 Hacer
				Si opponentBoard[i,j]='B' Entonces
					Escribir '~', ' '
				SiNo // Mostrar un espacio vacío si hay un barco
					Escribir opponentBoard[i,j], ' '
				FinSi // Mostrar impacto o agua
			FinPara
			Escribir ''
		FinPara
	FinMientras
FinAlgoritmo
