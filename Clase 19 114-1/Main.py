import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configuracion import *
from Rankings import *
from Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS 114")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
sonido = True

pantalla = pygame.display.set_mode(PANTALLA)
corriendo = True
datos_juego = {
    "puntuacion": 0,
    "vidas": 5,
    "nombre": "",
    "volumen_musica": 0,
    "mute" : False,
    "musica_activada" : False,
    "indice": 0,
    "modo": "bart",
    "cantidad_aciertos": 0,
    "doble_chance_activado": False,
    "por_dos_activado": False,
    "comodines": {
        "bomba": True,
        "por_dos": True,
        "doble_chance": True,
        "pasar": True
    }
}

lista_jugadores = leer_json("Ranking_jugadas.json")
reloj = pygame.time.Clock()
ventana_actual = "menu"
bandera_juego = False
while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()

    if ventana_actual == "menu":
        reiniciar_estadisticas(datos_juego)
        ventana_actual = mostrar_menu(pantalla, cola_eventos)

    elif ventana_actual == "salir":
        corriendo = False

    elif ventana_actual == "rankings":
        lista_jugadores = [leer_json("Ranking_jugadas.json")]
        ventana_actual = mostrar_rankings(pantalla, cola_eventos, lista_jugadores)

    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "juego":
        lista_preguntas = cargar_dificultad(datos_juego["modo"])
        if bandera_juego == False:
            bandera_juego = True

        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego, lista_preguntas, sonido)

    elif ventana_actual == "terminado":
        if bandera_juego == True:
            bandera_juego = False
        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego, lista_jugadores)

    pygame.display.flip()

pygame.quit()