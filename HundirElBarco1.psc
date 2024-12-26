Proceso HundirElBarco
    Definir SIZE Como Entero
    Definir SHIPS Como Entero
    Definir ships Como Entero
    Definir fila, columna Como Entero
    Definir allSunk Como Booleano
	
    SIZE <- 5
    SHIPS <- 3
	
    // Definir las matrices
    Definir playerBoard[0..4, 0..4] Como Caracter
    Definir opponentBoard[0..4, 0..4] Como Caracter
	
    // Inicializar tableros con '~'
    Para i Desde 0 Hasta 4 Hacer
        Para j Desde 0 Hasta 4 Hacer
            playerBoard[i, j] <- '~'
            opponentBoard[i, j] <- '~'
        Fin Para
    Fin Para
	
    Escribir "Selecciona el modo de juego:"
    Escribir "1. 1 vs 1"
    Escribir "2. Un jugador"
    Leer mode
	
    // Colocación de barcos del jugador
    Escribir "Coloca tus barcos en el tablero."
    ships <- SHIPS
    Mientras ships > 0 Hacer
        Escribir "Ingresa las coordenadas del barco (fila columna): "
        Leer fila, columna
		
        Si fila >= 0 Y fila < SIZE Y columna >= 0 Y columna < SIZE Y playerBoard[fila, columna] = '~' Entonces
            playerBoard[fila, columna] <- 'B' // Colocar un barco
            ships <- ships - 1
        Sino
            Escribir "Posición inválida o ya ocupada. Intenta de nuevo."
        Fin Si
    Fin Mientras
	
    Si mode = 1 Entonces
        // Colocación de barcos del oponente (jugador 2)
        Escribir "Ahora, el oponente colocará sus barcos."
        ships <- SHIPS
        Mientras ships > 0 Hacer
            Escribir "Ingresa las coordenadas del barco del oponente (fila columna): "
            Leer fila, columna
			
            Si fila >= 0 Y fila < SIZE Y columna >= 0 Y columna < SIZE Y opponentBoard[fila, columna] = '~' Entonces
                opponentBoard[fila, columna] <- 'B' // Colocar un barco
                ships <- ships - 1
            Sino
                Escribir "Posición inválida o ya ocupada. Intenta de nuevo."
            Fin Si
        Fin Mientras
    Sino
        // Colocación de barcos del oponente (computadora)
        Escribir "La computadora colocará sus barcos."
        ships <- SHIPS
        Mientras ships > 0 Hacer
            fila <- Aleatorio(0, SIZE-1)
            columna <- Aleatorio(0, SIZE-1)
			
            Si opponentBoard[fila, columna] = '~' Entonces
                opponentBoard[fila, columna] <- 'B' // Colocar un barco
                ships <- ships - 1
            Fin Si
        Fin Mientras
    Fin Si
	
    Escribir "¡Bienvenido a Hundir el barco!"
	
    Mientras Verdadero Hacer
        Escribir "Adivina las coordenadas del oponente (fila columna): "
        Leer fila, columna
		
        Si opponentBoard[fila, columna] = 'B' Entonces
            opponentBoard[fila, columna] <- 'X' // Impacto
            Escribir "¡Impacto!"
        Sino Si opponentBoard[fila, columna] = '~' Entonces
				opponentBoard[fila, columna] <- 'O' // Agua
				Escribir "¡Agua!"
			Sino
				Escribir "Ya has adivinado esas coordenadas. Intenta de nuevo."
				Continuar
			Fin Si
			
			// Comprobar si todos los barcos del oponente están hundidos
			allSunk <- Verdadero
			Para i Desde 0 Hasta 4 Hacer
				Para j Desde 0 Hasta 4 Hacer
					Si opponentBoard[i, j] = 'B' Entonces
						allSunk <- Falso
						Romper
					Fin Si
				Fin Para
				Si No allSunk Entonces
					Romper
				Fin Si
			Fin Para
			
			Si allSunk Entonces
				Escribir "¡Has hundido todos los barcos del oponente!"
				Romper
			Fin Si
			
			// Mostrar el tablero del oponente
			Escribir "Tablero del oponente:"
			Escribir "  0 1 2 3 4"
			Para i Desde 0 Hasta 4 Hacer
				Escribir i, " ";
				Para j Desde 0 Hasta 4 Hacer
					Si opponentBoard[i, j] = 'B' Entonces
						Escribir '~', " "; // Mostrar un espacio vacío si hay un barco
					Sino
						Escribir opponentBoard[i, j], " "; // Mostrar impacto o agua
					Fin Si
				Fin Para
				Escribir ""
			Fin Para
		Fin Mientras
Fin Proceso
