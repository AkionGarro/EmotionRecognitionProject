import cv2
import matplotlib.pyplot as plt
import argparse
import time

# Cargar los clasificadores de Haar para la detección de rostros y ojos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def calibrar_imagen(imagen):
    """
    Realiza la calibración de una imagen detectando y recortando el rostro.

    Args:
        imagen (numpy.ndarray): La imagen de entrada en formato BGR.

    Returns:
        numpy.ndarray: El rostro recortado y redimensionado a 48x48 en formato BGR.
    """
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    rostros = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(rostros) == 0:
        # Dejar solo el centro de la imagen quitando el 10% de los píxeles de los bordes
        alto, ancho, canales = imagen.shape
        rostro_recortado = imagen[int(alto*0.1):int(alto*0.9), int(ancho*0.1):int(ancho*0.9)]

        rostro_recortado = cv2.resize(rostro_recortado, (48, 48))

    # Iterar sobre los rostros detectados
    for (x, y, w, h) in rostros:
        # Recortar la región del rostro de la imagen original
        rostro_recortado = imagen[y:y+h, x:x+w]

        # Redimensionar el rostro recortado a 48x48
        rostro_recortado = cv2.resize(rostro_recortado, (48, 48))

        break  # Solo se toma el primer rostro detectado

    return rostro_recortado