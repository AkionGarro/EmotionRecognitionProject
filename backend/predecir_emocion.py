import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

longitud, altura = 48, 48
modelo = 'C:\\Users\\bryam\\Downloads\\archive\\modelo.h5'
pesos_modelo = 'C:\\Users\\bryam\\Downloads\\archive\\pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

def predict(img):
    #randon 1 a 1000
    n = np.random.randint(1,1000)
    #guardar imagen
    #cv2.imwrite('C:\\Users\\bryam\\Downloads\\test\\img_' + str(n) + '.jpg', img)    
    x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x = np.expand_dims(x, axis=0)  # Agregar una dimensión adicional para el lote (batch)
    x = x / 255.0  # Normalizar los valores de píxeles entre 0 y 1
    arreglo = cnn.predict(x)  # [[1,0,0]]

    max = np.amax(arreglo)

    resultado = arreglo[0]  # [1,0,0]
    respuesta = np.argmax(resultado)  # 0
    emocion = None
    if respuesta == 0:
        print('Enojado')
        emocion = 'Enojado'
    elif respuesta == 1:
        print('Disgusto')
        emocion = 'Disgusto'
    elif respuesta == 2:
        print('Miedo')
        emocion = 'Miedo'
    elif respuesta == 3:
        print('Feliz')
        emocion = 'Feliz'
    elif respuesta == 4:
        print('Triste')
        emocion = 'Triste'
    elif respuesta == 5:
        print('Sorprendido')
        emocion = 'Sorprendido'
    elif respuesta == 6:
        print('Neutral')
        emocion = 'Neutral'
    #imprimir imagen con texto de la predicción
    return emocion + ' ' + str((max*100).round(2))+ '%'

#predecir imagen
#prediccion = predict('C:\\Users\\bryam\\Downloads\\rostro_recortado0.jpg')