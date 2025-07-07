import random
from Constantes import *
import pygame
import json
import os

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')) -> None:
    """
    Dibuja texto en la superficie, manejando saltos de línea.

    Args:
        surface (Surface): Superficie donde se dibujará el texto.
        text (str): Texto a mostrar .
        pos (tuple): Coordenadas (x, y) de inicio.
        font (Font): Fuente Pygame utilizada para renderizar.
        color (Color): Color del texto (por defecto negro).
    """
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height
    return None

def crear_elemento_juego(textura: str, ancho: int, alto: int, pos_x: int, pos_y: int) -> dict:
    """
    Crea un diccionario con una superficie y su rectángulo.

    Args:
        textura (str): nombre de la imagen o ruta.
        ancho (int): Ancho deseado.
        alto (int): Alto deseado.
        pos_x (int): Posición horizontal.
        pos_y (int): Posición vertical.

    Returns:
        dict: Elemento con clave 'superficie', 'rectangulo' y 'visible'.
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura), (ancho, alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x, pos_y, ancho, alto)
    elemento_juego["visible"] = True
    return elemento_juego

def crear_lista_respuestas(textura: str, ancho: int, alto: int, pos_x: int, pos_y: int)  -> list:
    """
    Crea una lista de 4 elementos de respuesta, distribuidas en 2 columnas y 2 filas.

    Args:
        textura (str): Imagen de fondo.
        ancho (int): Ancho de cada botón.
        alto (int): Alto de cada botón.
        pos_x (int): Coordenada X inicial.
        pos_y (int): Coordenada Y inicial.

    Returns:
        list: Lista de elementos respuesta.
    """
    lista_respuestas = []
    for i in range(4):
        respuesta = crear_elemento_juego(textura, ancho, alto, pos_x, pos_y)
        lista_respuestas.append(respuesta)
        pos_y += 80
        if i == 1:
            pos_y -= 160
            pos_x = 310
    return lista_respuestas

def crear_comodines(textura: str, ancho: int, alto: int, pos_x: int, pos_y: int)  ->  list:
    """
    Genera una lista de 4 comodines alineados horizontalmente.

    Returns:
        list: Lista de comodines.
    """
    lista_comodin = []
    for i in range(4):
        comodin = crear_elemento_juego(textura, ancho, alto, pos_x, pos_y)
        lista_comodin.append(comodin)
        pos_x += 30

    return lista_comodin

def crear_botones_menu() -> list:
    """
    Crea los botones principales del menú.

    Returns:
        list: Lista de 4 botones con espaciado vertical.
    """
    lista_botones = []
    pos_x = 150
    pos_y = 115
    for i in range(4):
        boton = crear_elemento_juego("textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, pos_x, pos_y)
        pos_y += 80
        lista_botones.append(boton)
    return lista_botones

def limpiar_superficie(elemento_juego: dict, textura: str, ancho: int, alto: int) -> None:
    """
    Actualiza la textura de un elemento de juego.

    Args:
        elemento_juego (dict): Elemento a limpiar.
        textura (str): Ruta nueva o nombre de la imagen.
        ancho (int): Ancho de la nueva textura.
        alto (int): Alto de la nueva textura.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura), (ancho, alto))
    elemento_juego["visible"] = True
    return None

def verificar_respuesta(datos_juego: dict, pregunta_actual: dict, respuesta: str) -> str:
    """
    Verifica si la respuesta es correcta e impacta en los datos del juego.

    Returns:
        str: "correcta", "incorrecta" o "doble_chance".
    """
    correcta = str(pregunta_actual["respuesta_correcta"])
    if respuesta == correcta:
        puntos = PUNTUACION_ACIERTO
        if datos_juego.get("por_dos_activado", False):
            puntos *= 2
            datos_juego["por_dos_activado"] = False
        datos_juego["puntuacion"] += puntos
        datos_juego["doble_chance_activado"] = False
        retorno = "correcta"
    else:
        if datos_juego.get("doble_chance_activado") == True:
            datos_juego["doble_chance_activado"] = "esperando_segunda"
            return "doble_chance"
        elif datos_juego.get("doble_chance_activado") == "esperando_segunda":
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            datos_juego["vidas"] -= 1
            datos_juego["doble_chance_activado"] = False
            retorno = "correcta"
        else:
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            datos_juego["vidas"] -= 1
            retorno = "incorrecta"
    return retorno

def reiniciar_estadisticas(datos_juego: dict) -> None:
    """
    Reinicia todas las estadísticas y comodines del jugador para una nueva partida.

    Args:
        datos_juego (dict): Diccionario con los datos del juego a modificar.
    
    Return:
       None
    """
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""
    datos_juego["indice"] = 0
    datos_juego["cantidad_aciertos"] = 0
    datos_juego["doble_chance_activado"] = False
    datos_juego["por_dos_activado"] = False
    datos_juego["comodines"] = {
        "bomba": True,
        "por_dos": True,
        "doble_chance": True,
        "pasar": True
    }
    return None

def pasar_pregunta(lista_preguntas: list, indice: int, cuadro_pregunta: dict, lista_respuestas: list) -> dict:
    """
    Limpia los cuadros y muestra la siguiente pregunta.

    Returns:
        dict: Nueva pregunta actual.
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(cuadro_pregunta, "textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i], "textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON)
    return pregunta_actual

def mezclar_lista(lista_preguntas: list) -> None:
    """
    Mezcla aleatoriamente el orden de la lista de preguntas.
    """
    random.shuffle(lista_preguntas)
    return None

def generar_json(nombre_archivo: str, lista: list) -> bool:
    """
    Genera un archivo JSON a partir de una lista.

    Returns:
        bool: True si se generó correctamente, 
        False si la lista estaba vacía o era inválida.
    """
    if type(lista) == list and len(lista) > 0:
        with open(nombre_archivo, "w") as archivo:
            json.dump(lista, archivo, indent=4)
        return True
    else:
        return False

def leer_json(nombre_archivo: str) -> list:
    """
    Lee un archivo JSON y devuelve su contenido como lista.

    Returns:
        list: Lista obtenida del archivo o vacía si no existe.
    """
    lista = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as archivo:
            lista = json.load(archivo)
    return lista

def aplicar_bomba(pregunta: dict) -> list:
    """
    Devuelve los índices de respuestas que deben mantenerse visibles al aplicar el comodín bomba.

    Returns:
        list: Índices visibles (uno correcto + uno incorrecto aleatorio).
    """
    correcta = int(pregunta["respuesta_correcta"]) - 1
    indices = [0, 1, 2, 3]
    indices.remove(correcta)
    eliminar = random.sample(indices, 2)
    visibles = [i for i in range(4) if i not in eliminar]
    return visibles