import os

#PARSER -> Conversion 
#Pasar del archivo CSV a una lista de diccionarios (todos str)
#La cabecera del csv se van a convertir en las claves de mi diccionario

def mostrar_diccionario(diccionario) -> None:
    """
    Muestra por consola todas las claves y valores de un diccionario, con formato estético.

    Args:
        diccionario (dict): Diccionario cuyas claves y valores serán impresos por pantalla.

    Returns:
        None
    """
    for clave,valor in diccionario.items():
        print(f"{clave.title().replace("_"," ")} : {valor}")
        
def mostrar_lista_diccionarios(lista:list) -> bool:
    """
    Muestra una lista de diccionarios por consola, uno por uno.

    Args:
        lista (list): Lista de diccionarios a mostrar.

    Returns:
        bool: True si la lista tiene al menos un elemento, False si está vacía.
    """
    retorno = False
    for elemento in lista:
        retorno = True
        mostrar_diccionario(elemento)
        print("")
        
    return retorno

def obtener_claves(archivo,separador:str) -> list:
    """
    Lee la cabecera del archivo para obtener las claves del CSV.

    Args:
        archivo: Objeto de archivo abierto en modo lectura.
        separador (str): Carácter separador que detecta y separa cada clave.

    Returns:
        list: Lista de claves obtenidas del encabezado del CSV.
    """
    primer_linea = archivo.readline()
    primer_linea = primer_linea.replace("\n","")
    lista_claves = primer_linea.split(separador)
    
    return lista_claves

def obtener_valores(linea,separador:str) -> list:
    """
    Procesa una línea de texto y devuelve una lista de valores separados.

    Args:
        linea (str): Línea de texto a procesar.
        separador (str): Carácter separador de claves

    Returns:
        list: Lista de valores extraídos de la línea.
    """
    linea_aux = linea.replace("\n","")
    lista_valores = linea_aux.split(separador)
    return lista_valores

def crear_diccionario(lista_claves:list,lista_valores:list) -> dict:
    """
    Crea un diccionario combinando claves y valores por posición.

    Args:
        lista_claves (list): Lista de claves.
        lista_valores (list): Lista de valores correspondientes.

    Returns:
        dict: Diccionario generado combinando las claves y los valores.
    """

    diccionario_aux = {} 
    for i in range(len(lista_claves)):
        diccionario_aux[lista_claves[i]] = lista_valores[i]
        
    return diccionario_aux

def parse_csv(lista_elementos,nombre_archivo:str) -> bool: 
    """
    Parsea un archivo CSV y lo convierte en una lista de diccionarios de strings.

    Args:
        lista_elementos (list): Lista donde se almacenarán los diccionarios generados.
        nombre_archivo (str): Nombre del archivo CSV a leer.

    Returns:
        bool: True si el archivo fue leído correctamente, False si no existe.
    """
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo,"r", encoding="utf-8") as archivo:
            lista_claves = obtener_claves(archivo,",")
            for linea in archivo:
                lista_valores = obtener_valores(linea,",")
                diccionario_aux = crear_diccionario(lista_claves,lista_valores)
                lista_elementos.append(diccionario_aux)        
        return True
    else:
        return False

def cargar_dificultad(modo : str) -> list:
    """
    Carga preguntas desde un archivo CSV según el modo de dificultad seleccionado.

    Args:
        modo (str): Modo de dificultad ('bart' para fácil, 'lisa' para difícil).

    Returns:
        list: Lista de diccionarios con preguntas cargadas segun el modo y el archivo correspondiente.
    """
    lista_preguntas = []
    if modo == "bart":
      parse_csv(lista_preguntas, "Preguntas_faciles.csv")
    elif modo == "lisa":
        parse_csv(lista_preguntas, "Preguntas_dificiles.csv")
    
    return lista_preguntas
  





