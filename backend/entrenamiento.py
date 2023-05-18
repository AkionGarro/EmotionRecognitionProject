import pandas as pd
import numpy as np
import cv2
import os
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.keras import backend as K
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical

K.clear_session()

# Ruta al archivo CSV de entrenamiento y prueba
train_csv_path = 'C:\\Users\\bryam\\Downloads\\challenges-in-representation-learning-facial-expression-recognition-challenge\\train.csv'
test_csv_path = 'C:\\Users\\bryam\\Downloads\\challenges-in-representation-learning-facial-expression-recognition-challenge\\test.csv'

# Ruta a las carpetas de entrenamiento y prueba
train_image_folder = 'C:\\Users\\bryam\\Downloads\\archive\\train'
test_image_folder = 'C:\\Users\\bryam\\Downloads\\archive\\test'


class Emociones:
    def __init__(self, path_entrenamiento, path_validacion):
        self.epocas = 20
        self.altura, self.longitud = 48, 48
        self.batch_size = 32
        self.pasos = 895
        self.pasos_validacion = 200
        self.filtros_conv1 = 32
        self.filtros_conv2 = 64
        self.filtros_conv3 = 128
        self.tamano_filtro1 = (3, 3)
        self.tamano_filtro2 = (2, 2)
        self.tamano_filtro3 = (1, 1)
        self.tamano_pool = (2,2)
        self.clases = 7
        self.lr = 0.001

        self.model = None
        self.imagenes_entrenamiento = None
        self.imagenes_validacion = None
        self.path_entrenamiento = path_entrenamiento
        self.path_validacion = path_validacion
        self.data_gen_train = None
        self.data_gen_test = None
        self.creacion_data_gen()

        print("Constructor de la clase")
    
    def creacion_data_gen(self):
        print("Creación de data generators")

        self.data_gen_train = ImageDataGenerator(
            rescale=1./255,
        )

        self.data_gen_test = ImageDataGenerator(
            rescale=1./255
        )

        # self.imagenes_entrenamiento = entrenamiento_datagen.flow_from_directory(
        #     self.path_entrenamiento,
        #     target_size=(self.altura, self.longitud),
        #     color_mode='grayscale',
        #     batch_size=self.batch_size,
        #     class_mode='categorical'
        # )

        # self.imagenes_validacion = validacion_datagen.flow_from_directory(
        #     self.path_validacion,
        #     target_size=(self.altura, self.longitud),
        #     color_mode='grayscale',
        #     batch_size=self.batch_size,
        #     class_mode='categorical'
        # )
    
    def cargar_datos_train_csv(self, ruta_csv="C:\\Users\\bryam\\Downloads\\challenges-in-representation-learning-facial-expression-recognition-challenge\\train.csv"):
        print("Cargar datos train csv")
        # Cargar el archivo CSV usando Pandas
        data = pd.read_csv(ruta_csv)
        
        # Crear listas para almacenar las imágenes y las etiquetas
        imagenes = []
        etiquetas = []
        
        # Iterar sobre cada fila del DataFrame
        for index, row in data.iterrows():
            # Obtener el valor de píxeles y la etiqueta de la fila actual
            pixels = row['pixels']
            etiqueta = row['emotion']
            
            # Convertir los valores de píxeles a una matriz de imagen
            imagen = (np.array(list(map(int, pixels.split()))).reshape(48, 48))

            # Agregar la imagen y la etiqueta a las listas correspondientes
            imagenes.append(imagen)
            etiquetas.append(etiqueta)

        # Convertir las listas de imágenes y etiquetas a matrices NumPy
        imagenes = np.array(imagenes)
        etiquetas = np.array(etiquetas)
        # Expandir la dimensión de las imágenes para que tengan forma (número_de_muestras, altura, longitud, canales=1)
        imagenes = np.expand_dims(imagenes, axis=-1)
        #Convertir las etiquetas a un formato adecuado para la clasificación multiclase
        etiquetas = to_categorical(etiquetas, num_classes=self.clases)

        x_train = self.data_gen_train.flow(
            imagenes, 
            etiquetas, 
            batch_size=self.batch_size)
        
        return x_train

    def cargar_datos_test_csv(self, ruta_csv = "C:\\Users\\bryam\\Downloads\\challenges-in-representation-learning-facial-expression-recognition-challenge\\test.csv"):
        print("Cargar datos test csv")
        # Cargar el archivo CSV usando Pandas
        data = pd.read_csv(ruta_csv)
        
        # Crear listas para almacenar las imágenes
        imagenes = []
        
        # Iterar sobre cada fila del DataFrame
        for index, row in data.iterrows():
            # Obtener el valor de píxeles y la etiqueta de la fila actual
            pixels = row['pixels']
            
            # Convertir los valores de píxeles a una matriz de imagen
            imagen = (np.array(list(map(int, pixels.split()))).reshape(48, 48))
            
            # Agregar la imagen y la etiqueta a las listas correspondientes
            imagenes.append(imagen)
        
        # Devolver las imágenes y las etiquetas como matrices NumPy
        return np.array(imagenes)/255
    
    def crear_red(self):
        print("Creacion de la red")
        cnn = tf.keras.models.Sequential() 
        cnn.add(Convolution2D(filters = self.filtros_conv1, 
                                kernel_size = self.tamano_filtro1,
                                padding='same', 
                                input_shape=(self.altura, self.longitud, 1), 
                                activation='relu')
                )
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        cnn.add(Convolution2D(filters = self.filtros_conv2, 
                                kernel_size = self.tamano_filtro2,
                                padding='same',)
                )
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        
        cnn.add(tf.keras.layers.Flatten())
        cnn.add(tf.keras.layers.Dense(256, activation='relu'))
        cnn.add(tf.keras.layers.Dropout(0.5)) 
        cnn.add(tf.keras.layers.Dense(self.clases, activation='softmax')) 

        cnn.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(learning_rate=self.lr), metrics=['accuracy'])

        self.model = cnn
    

    def entrenar(self, train_data, test_data):
        print("Entrenamiento")
        #imprimir resumen de la red
        self.model.summary()
        self.model.fit(train_data, steps_per_epoch=self.pasos, epochs=self.epocas, validation_steps=self.pasos_validacion)
        print("Evaluación")
        self.model.evaluate(test_data)

    def save_model(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.model.save(path + "modelo.h5")
        self.model.save_weights(path + "pesos.h5")


if __name__ == '__main__':
    path_entrenamiento = "C:\\Users\\bryam\\Downloads\\archive\\train"
    path_validacion = "C:\\Users\\bryam\\Downloads\\archive\\test"
    emociones = Emociones(path_entrenamiento, path_validacion)
    train_data= emociones.cargar_datos_train_csv()
    test_data = emociones.cargar_datos_test_csv()
    emociones.crear_red()
    emociones.entrenar(train_data, test_data)
    emociones.save_model("C:\\Users\\bryam\\Downloads\\archive\\")
