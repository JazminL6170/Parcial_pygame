import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_suma = crear_elemento_juego("mas.webp",40,40,320,200)
boton_resta = crear_elemento_juego("menos.webp",40,40,100,200)
boton_volver = crear_elemento_juego("textura_respuesta.jpg",100,40,10,10)
boton_mute= crear_elemento_juego("mute.png",40,40,400,200)
boton_sonido = crear_elemento_juego("sonido.png",68,68,440,187)
boton_modo_bart = crear_elemento_juego("modo_bart.png",73,110,150,300)
boton_modo_lisa = crear_elemento_juego("modo_lisa.png",130,110,290,300)

fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            #QUE VUELVA AL MENU CUANDO TOCO LA TECLA ESC
            pass
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        if datos_juego["musica_activada"] == True:
                          datos_juego["volumen_musica"] += 25
                          datos_juego["mute"] = False
                          CLICK_SONIDO.play()
                          pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)

                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 25
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                        CLICK_SONIDO.play()
                    else: 
                        ERROR_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
                elif boton_mute["rectangulo"].collidepoint(evento.pos):
                    datos_juego["volumen_musica"] = 0
                    datos_juego["musica_activada"] = False
                    pygame.mixer.music.set_volume(0)
                    datos_juego["mute"] = True
                elif boton_sonido["rectangulo"].collidepoint(evento.pos):
                    ACTIVAR_SONIDO.play()
                    if not datos_juego["musica_activada"]:
                      pygame.mixer.music.load("musica.mp3")
                      pygame.mixer.music.play(-1)
                      datos_juego["musica_activada"] = True

                    datos_juego["volumen_musica"] = 25
                    pygame.mixer.music.set_volume(25 / 100)
                    datos_juego["mute"] = False
                elif boton_modo_bart["rectangulo"].collidepoint(evento.pos):
                    datos_juego["modo"] = "bart"
                    CLICK_SONIDO.play()
                elif boton_modo_lisa["rectangulo"].collidepoint(evento.pos):
                    datos_juego["modo"] = "lisa"
                    CLICK_SONIDO.play()
                    
    
    pantalla.blit(fondo_pantalla,(0,0))

    boton_modo_bart["superficie"].set_alpha(255 if datos_juego["modo"] == "bart" else 120)
    boton_modo_lisa["superficie"].set_alpha(255 if datos_juego["modo"] == "lisa" else 120)

    
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    pantalla.blit(boton_mute["superficie"],boton_mute["rectangulo"])
    pantalla.blit(boton_sonido["superficie"],boton_sonido["rectangulo"])
    pantalla.blit(boton_modo_bart["superficie"],boton_modo_bart["rectangulo"])
    pantalla.blit(boton_modo_lisa["superficie"],boton_modo_lisa["rectangulo"])

    mostrar_texto(pantalla,"Configuracion de Juego",(100,80),FUENTE_TEXTO,COLOR_AMARILLO)
    mostrar_texto(pantalla,"Volumen",(90,150),FUENTE_TEXTO,COLOR_BLANCO)
    mostrar_texto(pantalla,f"{datos_juego["volumen_musica"]} %",(220,190),FUENTE_TEXTO,COLOR_BLANCO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(pantalla,"Dificultad:",(90,260),FUENTE_RESPUESTA,COLOR_BLANCO)


    return retorno
    

#def manejar_botones_ajustes()