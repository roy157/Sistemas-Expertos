# -*- coding: utf-8 -*-

import pygame
import sys
import time

import busqueda

pygame.init()
size = ancho, alto = 600, 400

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)

pantalla = pygame.display.set_mode(size)

# Asegúrate de que la ruta a la fuente sea correcta en tu sistema
letraChica = pygame.font.Font("C:/Users/Duverly/Desktop/ex/lab2-hugo/OpenSans-Regular.ttf", 28)
letraGrande = pygame.font.Font("C:/Users/Duverly/Desktop/ex/lab2-hugo/OpenSans-Regular.ttf", 40)
letraMovimiento = pygame.font.Font("C:/Users/Duverly/Desktop/ex/lab2-hugo/OpenSans-Regular.ttf", 60)

usuario = None
tablero = busqueda.estado_inicial()
turnoSistemaExperto = False
se_rendido = False # Variable para rastrear la rendición del sistema experto

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pantalla.fill(negro)

    # Dejar que el usuario elija un ganador
    if usuario is None:

        # Dibujar el Título
        titulo = letraGrande.render("# Tres en Raya #", True, blanco)
        tituloRect = titulo.get_rect()
        tituloRect.center = ((ancho / 2), 50)
        pantalla.blit(titulo, tituloRect)

        # Dibujar botones
        playXButton = pygame.Rect((ancho / 8), (alto / 2), ancho / 4, 50)
        playX = letraChica.render("Jugar con X", True, negro)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(pantalla, blanco, playXButton)
        pantalla.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (ancho / 8), (alto / 2), ancho / 4, 50)
        playO = letraChica.render("Jugar con O", True, negro)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(pantalla, blanco, playOButton)
        pantalla.blit(playO, playORect)

        # Revisar si un boton fue presionado
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                usuario = busqueda.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                usuario = busqueda.O

    else:

        # Dibujar el tablero
        espacio_tamanho = 80
        espacio_origen = (ancho / 2 - (1.5 * espacio_tamanho),
                       alto / 2 - (1.5 * espacio_tamanho))
        espacios = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    espacio_origen[0] + j * espacio_tamanho,
                    espacio_origen[1] + i * espacio_tamanho,
                    espacio_tamanho, espacio_tamanho
                )
                pygame.draw.rect(pantalla, blanco, rect, 3)

                if tablero[i][j] != busqueda.EMPTY:
                    movimiento = letraMovimiento.render(tablero[i][j], True, blanco)
                    movimientoRect = movimiento.get_rect()
                    movimientoRect.center = rect.center
                    pantalla.blit(movimiento, movimientoRect)
                row.append(rect)
            espacios.append(row)

        ggwp = busqueda.terminal(tablero) # juego finalizado
        jugador = busqueda.jugador(tablero)

        # Mostrar titulo
        if se_rendido:
            # Mensaje mejorado para cuando el sistema experto se rinde
            titulo = f"Sistema Experto se rinde. ¡Ganaste!" 
        elif ggwp:
            ganador = busqueda.ganador(tablero)
            if ganador is None:
                titulo = f"Empate."
            else:
                titulo = f"{ganador} ganó."
        elif usuario == jugador:
            titulo = f"Jugar como {usuario}"
        else:
            titulo = f"Sistema Experto pensando..."
        titulo = letraGrande.render(titulo, True, blanco)
        tituloRect = titulo.get_rect()
        tituloRect.center = ((ancho / 2), 30)
        pantalla.blit(titulo, tituloRect)

        # Revisar para movimiento de Sistema Experto
        if usuario != jugador and not ggwp and not se_rendido:
            if turnoSistemaExperto:
                time.sleep(0.5)
                movimiento = busqueda.minimax(tablero)
                
                if movimiento == busqueda.RENDIRSE:
                    se_rendido = True
                elif movimiento is not None:
                    tablero = busqueda.resultado(tablero, movimiento)
                
                turnoSistemaExperto = False
            else:
                turnoSistemaExperto = True

        # Revisar para movimiento de usuario
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and usuario == jugador and not ggwp and not se_rendido:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (tablero[i][j] == busqueda.EMPTY and espacios[i][j].collidepoint(mouse)):
                        tablero = busqueda.resultado(tablero, (i, j))

        if ggwp or se_rendido:
            botonReiniciar = pygame.Rect(ancho / 3, alto - 65, ancho / 3, 50)
            reiniciar = letraChica.render("Play Again", True, negro)
            reiniciarRect = reiniciar.get_rect()
            reiniciarRect.center = botonReiniciar.center
            pygame.draw.rect(pantalla, blanco, botonReiniciar)
            pantalla.blit(reiniciar, reiniciarRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if botonReiniciar.collidepoint(mouse):
                    time.sleep(0.2)
                    usuario = None
                    tablero = busqueda.estado_inicial()
                    turnoSistemaExperto = False
                    se_rendido = False
    
    pygame.display.flip()