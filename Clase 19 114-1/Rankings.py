import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("textura_respuesta.jpg",100,40,10,10)
fondo_pantalla = pygame.transform.scale(pygame.image.load("ranking_fondo.jpg"),PANTALLA)

def mostrar_top_jugadores(pantalla: pygame.Surface,  lista_jugadores: list,
    fuente: pygame.font.Font, color: tuple, pos_inicial: tuple = (30, 80),
    max_jugadores: int = 10) -> None:
    """
    Muestra en pantalla los mejores puntajes de los primeros 10 jugadores.

    Args:
        pantalla (pygame.Surface): Superficie sobre la que se dibujará el ranking.
        lista_jugadores (list): Lista de diccionarios con claves "Nombre" y "Puntuacion".
        fuente (pygame.font.Font): Fuente utilizada para mostrar el texto.
        color (tuple): Color del texto.
        pos_inicial (tuple): Posición inicial (x, y) para comenzar a mostrar los nombres.
        max_jugadores (int): Cantidad máxima de jugadores a mostrar.

    Returns:
        None
    """
    lista_jugadores.sort(key=lambda jugador: jugador["Puntuacion"], reverse=True)
    x, y = pos_inicial
    for i, jugador in enumerate(lista_jugadores[:max_jugadores]):
        nombre = str(jugador["Nombre"])
        puntaje = str(jugador["Puntuacion"])
        fecha = jugador.get("Fecha", "Sin fecha")
        mostrar_texto(pantalla, f"{i + 1}. Nombre : {nombre} - Puntuacion: {puntaje} - Fecha: {fecha}", (x, y), fuente, color)
        y += 35

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
    """
    Muestra la pantalla de rankings del juego.

    Dibuja el fondo, procesa eventos (como clic en botón "VOLVER" o cierre de ventana), 
    y muestra los mejores puntajes.

    Args:
        pantalla (pygame.Surface): Superficie principal del juego donde se dibujan los elementos visuales.
        cola_eventos (list[pygame.event.Event]): Lista de eventos capturados por pygame durante el bucle principal.
        lista_rankings (list): Lista que contiene una sublista de diccionarios 
        con los datos de los jugadores (Nombre y Puntuacion).

    Returns:
        str: Nombre de la próxima ventana a mostrar.
            
    """
    pantalla.blit(fondo_pantalla, (0,0))
    retorno = "rankings"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
        
   
    
    pantalla.blit(fondo_pantalla, (0,0))
    datos = lista_rankings
    mostrar_top_jugadores(pantalla, datos[0], FUENTE_RANKING, COLOR_BLANCO)
    
   
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,f"TOP 10",(200,10),pygame.font.Font("simpson.otf",50), COLOR_BLANCO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_BOTON,COLOR_BLANCO)
    pygame.display.flip()
    
    return retorno

