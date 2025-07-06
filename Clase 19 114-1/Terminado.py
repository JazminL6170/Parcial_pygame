import pygame
from Constantes import *
from Funciones import *

pygame.init()

fuente = FUENTE_TEXTO
cuadro = crear_elemento_juego("textura_cuadro_final.jpg",250,50,20,190)
fondo_pantalla = pygame.transform.scale(pygame.image.load("foto_final.jpg"),PANTALLA)
def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict, lista_jugadores: list) -> str:
    retorno = "terminado"
    pygame.mixer.music.set_volume(0)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            #Estaria bueno forzarle al usuario que no pueda salir del juego hasta que guarde la puntuacion -> A gusto de ustedes
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:

            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)


            if letra_presionada == "backspace" and len(datos_juego["nombre"]) > 0:
                datos_juego["nombre"] = datos_juego["nombre"][0:-1]#Elimino el ultimo
                print(datos_juego["nombre"])
                limpiar_superficie(cuadro,"textura_cuadro_final.jpg",250,50)
            
            if letra_presionada == "space":
                datos_juego["nombre"] += " "
            
            if len(letra_presionada) == 1:  
                if bloc_mayus != 0:
                    datos_juego["nombre"] += letra_presionada.upper()
                else:
                    datos_juego["nombre"] += letra_presionada
            if letra_presionada == "return":
                limpiar_superficie(cuadro,"textura_cuadro_final.jpg",250,50)
                lista_jugadores = leer_json("Ranking_jugadas.json")
                nuevo_jugador = {"Nombre": datos_juego["nombre"], "Puntuacion": datos_juego["puntuacion"]}
                lista_jugadores.append(nuevo_jugador)
                generar_json("Ranking_jugadas.json", lista_jugadores)
                reiniciar_estadisticas(datos_juego)
                retorno = "menu"
            


    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro["superficie"],cuadro["rectangulo"])
    mostrar_texto(cuadro["superficie"],datos_juego["nombre"],(10,0),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla,"Fin del Juego",(200,20),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla,"Ingrese su nombre",(20,150),FUENTE_GENERAL,COLOR_BLANCO)
    mostrar_texto(pantalla,f"Usted obtuvo: {datos_juego["puntuacion"]} puntos",(20,95),FUENTE_RANKING,COLOR_NEGRO)


    return retorno