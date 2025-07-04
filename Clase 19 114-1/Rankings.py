import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("textura_respuesta.jpg",100,40,10,10)
fondo_pantalla = pygame.transform.scale(pygame.image.load("ranking_fondo.jpg"),PANTALLA)
def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
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
    datos[0].sort(key=lambda jugador: jugador["Puntuacion"], reverse=True)

    y = 80
    puesto = 1
    for i in datos[0]:
      nombre = str(i["Nombre"])
      puntaje = str(i["Puntuacion"])
      mostrar_texto(pantalla, f"{puesto}. Nombre : {nombre} - Puntuacion: {puntaje}", (30, y), FUENTE_RANKING, COLOR_BLANCO)
      y += 40
      puesto += 1
      if puesto == 11:
       break
    
   
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,f"TOP 10",(200,10),pygame.font.Font("simpson.otf",50), COLOR_AMARILLO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_RESPUESTA,COLOR_BLANCO)
    pygame.display.flip()
    
    return retorno
    