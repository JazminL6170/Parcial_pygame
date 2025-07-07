import pygame
from Constantes import *
from Funciones import *
from datetime import datetime

pygame.init()

fuente = FUENTE_TEXTO
cuadro = crear_elemento_juego("textura_cuadro_final.jpg",250,50,20,190)
fondo_pantalla = pygame.transform.scale(pygame.image.load("foto_final.jpg"),PANTALLA)

boton_volver = crear_elemento_juego("textura_respuesta.jpg", 120, 40, 85, 280)
boton_reiniciar = crear_elemento_juego("textura_respuesta.jpg", 120, 40, 85, 350)

def guardar_puntuacion(datos_juego: dict, ruta_archivo: str = "Ranking_jugadas.json") -> None:
    """
    Guarda el nombre y la puntuación del jugador actual en el archivo de rankings.

    Args:
        datos_juego (dict): Diccionario con el nombre y puntuación del jugador.
        ruta_archivo (str): Ruta del archivo JSON a actualizar.

    Returns:
        None
    """
    lista_jugadores = leer_json(ruta_archivo)
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo_jugador = {
        "Nombre": datos_juego["nombre"],
        "Puntuacion": datos_juego["puntuacion"],
        "Fecha": fecha_actual
    }
    lista_jugadores.append(nuevo_jugador)
    generar_json(ruta_archivo, lista_jugadores)
    
    return None

def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict, lista_jugadores: list) -> str:
    """
    Muestra la pantalla final del juego donde el jugador ingresa su nombre para guardar la puntuación.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibujan todos los elementos visuales.
        cola_eventos (list[pygame.event.Event]): Lista de eventos recibidos de pygame.
        datos_juego (dict): Diccionario que contiene los datos actuales del jugador,
        incluyendo 'nombre' y 'puntuacion'.
        lista_jugadores (list): Lista con los jugadores cargados previamente.

    Returns:
        str: Indicador de la siguiente pantalla a mostrar
    """
    retorno = "terminado"
    pygame.mixer.music.set_volume(0)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
            
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                reiniciar_estadisticas(datos_juego)
                retorno = "menu"
            elif boton_reiniciar["rectangulo"].collidepoint(evento.pos):
                limpiar_superficie(cuadro,"textura_cuadro_final.jpg",250,50)
                reiniciar_estadisticas(datos_juego)
                retorno = "juego"

        elif evento.type == pygame.KEYDOWN:

            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)


            if letra_presionada == "backspace" and len(datos_juego["nombre"]) > 0:
                datos_juego["nombre"] = datos_juego["nombre"][0:-1]
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
                guardar_puntuacion(datos_juego, "Ranking_jugadas.json")
                reiniciar_estadisticas(datos_juego)
                retorno = "menu"
            


    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro["superficie"],cuadro["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    pantalla.blit(boton_reiniciar["superficie"], boton_reiniciar["rectangulo"])
  
    mostrar_texto(cuadro["superficie"],datos_juego["nombre"],(10,0),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla,"Fin del Juego",(200,20),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla,"Ingrese su nombre",(20,150),FUENTE_GENERAL,COLOR_BLANCO)
    mostrar_texto(pantalla,f"Usted obtuvo: ",(20,95),FUENTE_GENERAL,COLOR_NEGRO)
    mostrar_texto(pantalla, F"{datos_juego["puntuacion"]} puntos", (200, 95),FUENTE_GENERAL, COLOR_ROJO)
    mostrar_texto(boton_volver["superficie"], "VOLVER", (20, 10), FUENTE_BOTON, COLOR_BLANCO)
    mostrar_texto(boton_reiniciar["superficie"], "REINICIAR", (10, 10), FUENTE_BOTON, COLOR_BLANCO)
    mostrar_texto(pantalla,"Presione enter para agregar su puntuacion al RANKING", (20,400),FUENTE_TEXTO, COLOR_VERDE)


    return retorno