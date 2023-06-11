import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

# Cargar los clasificadores de Haar para la detección de rostros y ojos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
longitud, altura = 48, 48
modelo = './data/modelo_emociones.h5'
pesos_modelo = './data/pesos_emociones.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

def predict_emotions(img):
    #randon 1 a 1000
    n = np.random.randint(1,1000)
    #guardar imagen
    #cv2.imwrite('C:\\Users\\bryam\\Downloads\\test\\img_' + str(n) + '.jpg', img)    
    try:
        x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        img = cv2.imread(img)
        x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x = np.expand_dims(x, axis=0)  # Agregar una dimensión adicional para el lote (batch)
    x = x / 255.0  # Normalizar los valores de píxeles entre 0 y 1
    arreglo = cnn.predict(x)  # [[1,0,0]]    
    emociones = []
    emociones.append(float("{:.5f}".format(arreglo[0][0])))
    emociones.append(float("{:.5f}".format(arreglo[0][1])))
    emociones.append(float("{:.5f}".format(arreglo[0][2])))
    emociones.append(float("{:.5f}".format(arreglo[0][3])))
    emociones.append(float("{:.5f}".format(arreglo[0][4])))
    emociones.append(float("{:.5f}".format(arreglo[0][5])))
    emociones.append(float("{:.5f}".format(arreglo[0][6])))

    return emociones

def calculate_emotions_factors(dataset_path = "'data\\MES_dataset.csv'"):
    
    # Cargar el conjunto de datos desde el archivo CSV
    dataset = pd.read_csv(dataset_path, na_values='-')

    # Rellenar los valores nulos con 0
    dataset.fillna(0, inplace=True)

    # Calcular la suma de las frecuencias de cada emoción
    emotions_sum = dataset.sum(axis=0)

    # Asignar pesos a cada emoción basados en su frecuencia
    emotions_weights = emotions_sum / emotions_sum.sum()

    # Normalizar los pesos para asegurarse de que sumen 1
    emotions_factors = emotions_weights / emotions_weights.sum()

    return emotions_factors.tolist()

def engaged(focused_value, emotions_weights):
    
    
    # Definir el peso de cada emoción a partir del conjunto de datos MES
    emotions_factors = calculate_emotions_factors('data\\MES_dataset.csv')
    print(emotions_factors)

    # Multiplicar cada peso de emoción por su respectivo valor en emotions_weights
    weighted_emotions = [factor * weight for factor, weight in zip(emotions_factors, emotions_weights)]
  
    
    sum_emotions = sum(weighted_emotions)

    # Calcular el tercer parámetro como una interpolación entre focused_value y sum_emotions
    engagement_level = focused_value * 0.6 + sum_emotions * 0.4

    # Limitar el engagement_level dentro del rango de 0.0 a 1.0
    engagement_level = max(0.0, min(1.0, engagement_level))

    # Comparar con el umbral y determinar si está "engaged" o "not engaged"
    if engagement_level >= 0.6:
        return ["engaged", engagement_level]
    else:
        return ["not engaged", engagement_level]
    

def extraer_rostros(imagen):
    imagenes = []
    rostros = face_cascade.detectMultiScale(imagen, 1.3, 5)
    # Iterar sobre los rostros detectados, recortarlos a 5px más de cada lado y guardarlo en la lista
    for (x, y, w, h) in rostros:
        try:
            imagenes.append(imagen[y-5:y+h+5, x-5:x+w+5])
        except:
            imagenes.append(imagen[y:y+h, x:x+w])
    return imagenes
    
    
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
        # recortar imagen al tamaño del rostro detectado
        rostro_recortado = imagen[y:y+h, x:x+w]
        # resize de la imagen al tamaño de entrada de la red neuronal
        rostro_recortado = cv2.resize(rostro_recortado, (48, 48))
        break# solo se toma el primer rostro 
    
    #guardar la imagen con el rectángulo dibujado
    #cv2.imwrite("C:\\Users\\bryam\\Downloads\\muu1.png", imagen)

    return rostro_recortado

# image_path = os.path.join("C:\\Users\\bryam\\Downloads\\muu.jpg")
# gray_image = cv2.imread(image_path)
# calibrar_imagen(gray_image)