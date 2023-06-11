import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from keras.models import load_model

# Cargar los clasificadores de Haar para la detección de rostros y ojos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
longitud, altura = 48, 48
modelo = './data/modelo_emociones.h5'
pesos_modelo = './data/pesos_emociones.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

def predict_emotions(img):
    try:
        x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        return [0,0,0,0,0,0,0]
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

    # Normalizar los pesos de emoción para que sumen 1
    total_weights = sum(emotions_weights)
    if total_weights == 0:
        return ["not engaged", 0.0]
    normalized_weights = [weight / total_weights for weight in emotions_weights]

    # Multiplicar cada peso de emoción normalizado por su respectivo factor
    weighted_emotions = [factor * weight for factor, weight in zip(emotions_factors, normalized_weights)]

    sum_emotions = sum(weighted_emotions)
    print("emotions_level: ", sum_emotions)

    # Calcular el tercer parámetro como una interpolación entre focused_value y sum_emotions
    engagement_level = focused_value * 0.7 + sum_emotions * 0.3

    # Limitar el engagement_level dentro del rango de 0.0 a 1.0
    engagement_level = max(0.0, min(1.0, engagement_level))

    # Comparar con el umbral y determinar si está "engaged" o "not engaged"
    if engagement_level >= 0.4:
        return ["engaged", engagement_level]
    else:
        return ["not engaged", engagement_level]
    

def extraer_rostros(imagen, exp=60):
    imagenes = []
    rostros = face_cascade.detectMultiScale(imagen, 1.3, 5)
    # Iterar sobre los rostros detectados, recortarlos a 5px más de cada lado y guardarlo en la lista
    cont=1
    for (x, y, w, h) in rostros:
        try:
            imagenes.append(imagen[y-exp:y+h+exp, x-exp:x+w+exp])
            #guardar imagen
            cv2.imwrite('C:\\Users\\bryam\\Pictures\\Camera Roll\\pruebas\\results\\img_' + str(cont) + '.jpg', imagen[y-exp:y+h+exp, x-exp:x+w+exp])
        except:
            print("error")
            imagenes.append(imagen[y:y+h, x:x+w])
            cv2.imwrite('C:\\Users\\bryam\\Pictures\\Camera Roll\\pruebas\\results\\img_' + str(cont) + '.jpg', imagen[y:y+h, x:x+w])
        cont+=1    
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
    try:
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    except:
        gray = imagen

    # Detectar rostros en la imagen
    rostros = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(rostros) == 0:
        # Dejar solo el centro de la imagen quitando el 10% de los píxeles de los bordes
        alto, ancho, canales = imagen.shape
        rostro_recortado = imagen[int(alto*0.1):int(alto*0.9), int(ancho*0.1):int(ancho*0.9)]

        try:
            rostro_recortado = cv2.resize(rostro_recortado, (48, 48))
        except:
            pass

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
