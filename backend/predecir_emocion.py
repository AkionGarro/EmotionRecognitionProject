import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

longitud, altura = 48, 48
modelo = './data/modelo_emociones.h5'
pesos_modelo = './data/pesos_emociones.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

def predict(img):

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
    #covert array to diccionary
    # emociones = {}
    # emociones["Angry"] = "{:.9f}".format(arreglo[0][0])
    # emociones["Disgust"] = "{:.9f}".format(arreglo[0][1])
    # emociones["Fear"] = "{:.9f}".format(arreglo[0][2])
    # emociones["Happy"] = "{:.9f}".format(arreglo[0][3])
    # emociones["Sad"] = "{:.9f}".format(arreglo[0][4])
    # emociones["Surprise"] = "{:.9f}".format(arreglo[0][5])
    # emociones["Neutral"] = "{:.9f}".format(arreglo[0][6])
    emociones = []
    emociones.append(float("{:.5f}".format(arreglo[0][0])))
    emociones.append(float("{:.5f}".format(arreglo[0][1])))
    emociones.append(float("{:.5f}".format(arreglo[0][2])))
    emociones.append(float("{:.5f}".format(arreglo[0][3])))
    emociones.append(float("{:.5f}".format(arreglo[0][4])))
    emociones.append(float("{:.5f}".format(arreglo[0][5])))
    emociones.append(float("{:.5f}".format(arreglo[0][6])))

    return emociones