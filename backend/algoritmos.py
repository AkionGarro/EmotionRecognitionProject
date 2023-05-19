import cv2
import matplotlib.pyplot as plt
import argparse
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def calibrar_imagen(imagen):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    rostros = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(rostros) == 0:
        #dejar solo el centro de la imagen quitando 10% de pixeles de los bordes
        alto, ancho, canales = imagen.shape
        rostro_recortado = imagen[int(alto*0.1):int(alto*0.9), int(ancho*0.1):int(ancho*0.9)]

        # Redimensionar el rostro recortado a 48x48
        rostro_recortado = cv2.resize(rostro_recortado, (48, 48))

        #guardar imagen recortada
        cv2.imwrite('C:\\Users\\bryam\\Downloads\\rostro_recortado1.jpg', rostro_recortado)

    # Iterar sobre los rostros detectados
    for (x, y, w, h) in rostros:
        # Recortar la región del rostro de la imagen original
        rostro_recortado = imagen[y:y+h, x:x+w]
        
        # Redimensionar el rostro recortado a 40x40
        rostro_recortado = cv2.resize(rostro_recortado, (48, 48))

        break #solo se toma el primer rostro detectado  


    return rostro_recortado