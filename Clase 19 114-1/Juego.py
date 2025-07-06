import pygame 
from Constantes import *
from Preguntas import *
from Funciones import *

pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo_juego.jpg"), PANTALLA)
textura_pregunta = pygame.transform.scale(pygame.image.load("textura_pregunta.jpg"), (350, 150))
textura_respuesta =  pygame.transform.scale(pygame.image.load("textura_respuestas.jpg"), (250, 60))
cuadro_pregunta = crear_elemento_juego("textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 120, 80)
lista_respuestas = crear_lista_respuestas("textura_respuestas.jpg", ANCHO_BOTON, ALTO_BOTON, 30, 245)
evento_tiempo = pygame.USEREVENT 
pygame.time.set_timer(evento_tiempo, 1000)

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict, lista_preguntas: list, sonido: bool) -> str:
    retorno = "juego"
    

    pregunta_actual = lista_preguntas[datos_juego["indice"]]

    if "tiempo_pregunta" not in datos_juego:
        datos_juego["tiempo_pregunta"] = 20

    if "cantidad_aciertos" not in datos_juego:
        datos_juego["cantidad_aciertos"] = 0

    if "respuestas_visibles" not in datos_juego:
        datos_juego["respuestas_visibles"] = [0, 1, 2, 3]

    if datos_juego["vidas"] == 0:
        retorno = "terminado"

    respuestas_visibles = datos_juego["respuestas_visibles"]

    imagen_bomba = pygame.transform.scale(pygame.image.load("bomba.png"), (40, 40))
    rect_bomba = imagen_bomba.get_rect(center=(80, 450))

    imagen_doble_chance = pygame.transform.scale(pygame.image.load("doble_chance.png"), (40, 40))
    rect_doble_chance = imagen_doble_chance.get_rect(center=(200, 450))

    imagen_por_dos = pygame.transform.scale(pygame.image.load("por_dos.png"), (40, 40))
    rect_por_dos = imagen_por_dos.get_rect(center=(380, 450))

    imagen_pasar = pygame.transform.scale(pygame.image.load("pasar.png"), (40, 40))
    rect_pasar = imagen_pasar.get_rect(center=(500, 450))

    for evento in cola_eventos:

        if evento.type == pygame.QUIT:
            retorno = "salir"

        elif evento.type == evento_tiempo:
            datos_juego["tiempo_pregunta"] -= 1
            if datos_juego["tiempo_pregunta"] <= 0:
                datos_juego["vidas"] -= 1
                datos_juego["indice"] += 1
                if datos_juego["indice"] >= len(lista_preguntas):
                    datos_juego["indice"] = 0
                    mezclar_lista(lista_preguntas)
                datos_juego["tiempo_pregunta"] = 20
                datos_juego["respuestas_visibles"] = [0, 1, 2, 3]
                datos_juego["doble_chance_activado"] = False
                datos_juego["por_dos_activado"] = False
                pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if rect_bomba.collidepoint(evento.pos) and datos_juego["comodines"]["bomba"]:
                datos_juego["respuestas_visibles"] = aplicar_bomba(pregunta_actual)
                datos_juego["comodines"]["bomba"] = False

            elif rect_por_dos.collidepoint(evento.pos) and datos_juego["comodines"]["por_dos"]:
                datos_juego["comodines"]["por_dos"] = False
                datos_juego["por_dos_activado"] = True

            elif rect_doble_chance.collidepoint(evento.pos) and datos_juego["comodines"]["doble_chance"]:
                datos_juego["comodines"]["doble_chance"] = False
                datos_juego["doble_chance_activado"] = True

            elif rect_pasar.collidepoint(evento.pos) and datos_juego["comodines"]["pasar"]:
                datos_juego["comodines"]["pasar"] = False
                datos_juego["indice"] += 1
                if datos_juego["indice"] >= len(lista_preguntas):
                    datos_juego["indice"] = 0
                    mezclar_lista(lista_preguntas)
                datos_juego["tiempo_pregunta"] = 20
                datos_juego["respuestas_visibles"] = [0, 1, 2, 3]
                datos_juego["doble_chance_activado"] = False
                datos_juego["por_dos_activado"] = False
                pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)

            for i in datos_juego["respuestas_visibles"]:
                if lista_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                    respuesta = str(i + 1)
                    resultado = verificar_respuesta(datos_juego, pregunta_actual, respuesta)

                    if resultado == "correcta":
                        if datos_juego["mute"] == False:
                          ACIERTO_SONIDO.play()
                        datos_juego["cantidad_aciertos"] += 1
                        if datos_juego["cantidad_aciertos"] == 5:
                            datos_juego["vidas"] += 1
                            datos_juego["cantidad_aciertos"] = 0
                        avanzar = True

                    elif resultado == "doble_chance":
                        if datos_juego["mute"] == False:
                          ERROR_SONIDO.play()
                        lista_respuestas[i]["visible"] = False
                        avanzar = False

                    elif resultado == "incorrecta":
                        if datos_juego["mute"] == False:
                          ERROR_SONIDO.play()
                        datos_juego["cantidad_aciertos"] = 0
                        avanzar = True

                    else:
                        avanzar = False

                    if avanzar:
                        datos_juego["indice"] += 1
                        if datos_juego["indice"] >= len(lista_preguntas):
                            datos_juego["indice"] = 0
                            mezclar_lista(lista_preguntas)
                        datos_juego["tiempo_pregunta"] = 20
                        datos_juego["respuestas_visibles"] = [0, 1, 2, 3]
                        for r in lista_respuestas:
                            r["visible"] = True
                        datos_juego["doble_chance_activado"] = False
                        datos_juego["por_dos_activado"] = False
                        pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)

    pantalla.blit(fondo_pantalla, (0, 0))
    pantalla.blit(cuadro_pregunta["superficie"], cuadro_pregunta["rectangulo"])
    cuadro_pregunta["superficie"].blit(textura_pregunta, (0, 0))
    mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual["pregunta"], (15, 15), FUENTE_GENERAL, COLOR_NEGRO)
    for i in datos_juego["respuestas_visibles"]:
        if lista_respuestas[i].get("visible", True):
            pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])
            lista_respuestas[i]["superficie"].blit(textura_respuesta,(0,0))
            mostrar_texto(lista_respuestas[i]["superficie"], pregunta_actual[f"respuesta_{i+1}"], (15, 15), FUENTE_RESPUESTA, COLOR_BLANCO)

    pygame.draw.circle(pantalla, COLOR_AMARILLO, (80, 450), 30)
    pygame.draw.circle(pantalla, COLOR_AMARILLO, (200, 450), 30)
    pygame.draw.circle(pantalla, COLOR_AMARILLO, (380, 450), 30)
    pygame.draw.circle(pantalla, COLOR_AMARILLO, (500, 450), 30)

    imagen_bomba.set_alpha(255 if datos_juego["comodines"]["bomba"] else 80)
    imagen_doble_chance.set_alpha(255 if datos_juego["comodines"]["doble_chance"] else 80)
    imagen_por_dos.set_alpha(255 if datos_juego["comodines"]["por_dos"] else 80)
    imagen_pasar.set_alpha(255 if datos_juego["comodines"]["pasar"] else 80)

    pantalla.blit(imagen_bomba, rect_bomba)
    pantalla.blit(imagen_doble_chance, rect_doble_chance)
    pantalla.blit(imagen_por_dos, rect_por_dos)
    pantalla.blit(imagen_pasar, rect_pasar)

    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 10), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 40), FUENTE_RANKING, COLOR_NEGRO)
    mostrar_texto(pantalla, f"TIEMPO: {datos_juego['tiempo_pregunta']} seg", (350, 10), FUENTE_TEXTO, COLOR_ROJO)

    return retorno