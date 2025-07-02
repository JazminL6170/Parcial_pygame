import pygame 
from Constantes import *
from Preguntas import *
from Funciones import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS 114")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
corriendo = True
datos_juego = {"puntuacion":0,"vidas":CANTIDAD_VIDAS,"nombre":"","tiempo_restante":TIEMPO_JUEGO}

fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)
reloj = pygame.time.Clock()
indice = 0

mezclar_lista(lista_preguntas)
pregunta_actual = lista_preguntas[indice]

#Creando el cuadro de la pregunta
cuadro_pregunta = crear_elemento_juego("textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,80,80)
#Creando botones de respuesta
lista_respuestas = crear_lista_respuestas("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,125,245)
    
evento_tiempo = pygame.USEREVENT 
pygame.time.set_timer(evento_tiempo,1000)    


while corriendo:
    reloj.tick(FPS)
    
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        print("GAME OVER")
        corriendo = False
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:#Quiero que sea click izquierdo 
                for i in range(len(lista_respuestas)):#Recorro todos los botones de cada respuesta
                    if lista_respuestas[i]["rectangulo"].collidepoint(evento.pos): #Verifico si le hice click a uno
                        respuesta = (i + 1)
                        if verificar_respuesta(datos_juego,pregunta_actual,respuesta) == True:
                            CLICK_SONIDO.play()
                        else:
                            ERROR_SONIDO.play()
                        
                        indice += 1
                        
                        if indice >= len(lista_preguntas):
                            indice = 0
                            mezclar_lista(lista_preguntas)
                        
                        pregunta_actual = pasar_pregunta(lista_preguntas,indice,cuadro_pregunta,lista_respuestas)
                                        
    
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])
    
    for i in range(len(lista_respuestas)):
        pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])
        #mostrar_texto(lista_respuestas[i]["superficie"],pregunta_actual[f"respuesta_{i+1}"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
    
    mostrar_texto(cuadro_pregunta["superficie"],pregunta_actual["pregunta"],(15,15),FUENTE_PREGUNTA,COLOR_NEGRO)
    mostrar_texto(lista_respuestas[0]["superficie"],pregunta_actual["respuesta_1"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(lista_respuestas[1]["superficie"],pregunta_actual["respuesta_2"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(lista_respuestas[2]["superficie"],pregunta_actual["respuesta_3"],(15,15),FUENTE_RESPUESTA,COLOR_BLANCO)
        
    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,10),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,40),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(pantalla,f"TIEMPO: {datos_juego['tiempo_restante']} seg",(275,10),FUENTE_TEXTO,COLOR_NEGRO)

    #pygame.draw.rect(pantalla,COLOR_NEGRO,cuadro_pregunta["rectangulo"],3)
    
    pygame.display.flip()

pygame.quit()