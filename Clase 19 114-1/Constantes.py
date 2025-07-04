import pygame
pygame.init()

COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_VIOLETA = (134,23,219)
COLOR_AMARILLO = ("#B5AD09")
ANCHO = 600
ALTO = 500
PANTALLA = (ANCHO,ALTO)
FPS = 30

BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3


ANCHO_PREGUNTA = 350
ALTO_PREGUNTA = 150
ANCHO_BOTON = 250
ALTO_BOTON = 60
TAMAÑO_BOTON_VOLUMEN = (60,60)
TAMAÑO_BOTON_VOLVER = (100,40)
CLICK_SONIDO = pygame.mixer.Sound("click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("error.mp3")
ACIERTO_SONIDO = pygame.mixer.Sound("sonido_acierto.mp3")
FUENTE_PREGUNTA = pygame.font.SysFont("timesnewroman",28,True)
FUENTE_RESPUESTA = pygame.font.SysFont("timesnewroman",20,True)
FUENTE_RANKING = pygame.font.SysFont("Comic Sans MS ",20,True)
FUENTE_TEXTO = pygame.font.Font("simpson.otf",30)
FUENTE_VOLUMEN = pygame.font.SysFont("Arial",50,True)

CANTIDAD_VIDAS = 3
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25
TIEMPO_JUEGO = 30