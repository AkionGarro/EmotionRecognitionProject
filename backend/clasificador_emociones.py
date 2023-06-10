import pandas as pd
import numpy as np
import cv2
import os
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
from tensorflow.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.keras import backend as K

from tensorflow.keras.utils import to_categorical

K.clear_session()

class Emociones:
    def __init__(self, path_entrenamiento, path_validacion, path_test):
        """
        Inicializa una instancia de la clase Emociones.

        Args:
            path_entrenamiento (str): Ruta al directorio de entrenamiento train.csv.
            path_validacion (str): Ruta al directorio de validación test.csv.
        """
        print("Constructor de la clase Emociones")
        self.path_entrenamiento = path_entrenamiento
        self.path_validacion = path_validacion
        self.path_test = path_test
        
        self.epocas = 20
        self.altura, self.longitud = 48, 48
        self.batch_size = 32
        self.pasos = 896
        self.pasos_validacion = 112
        self.filtros_conv1 = 32
        self.filtros_conv2 = 64
        self.filtros_conv3 = 128
        self.tamano_filtro1 = (3, 3)
        self.tamano_filtro2 = (2, 2)
        self.tamano_filtro3 = (1, 1)
        self.tamano_pool1 = (2, 2)
        self.tamano_pool2 = (2, 2)
        self.clases = 7
        self.lr = 0.001
        
        self.model = None
        self.data_gen_train = None
        self.data_gen_validation = None
        self.data_gen_test = None
        self.train_data = None
        self.validation_data = None
        self.test_data = None
        self.creacion_data_gen()
        self.cargar_datos_train_csv()
        self.cargar_datos_validation_csv()
        self.cargar_datos_test_csv()
        self.crear_red()
    
    def creacion_data_gen(self):
        """
        Creación de data generators
        """
        print("Creación de data generators")
        self.data_gen_train = ImageDataGenerator(rescale=1./255)
        self.data_gen_validation = ImageDataGenerator(rescale=1./255)
        self.data_gen_test = ImageDataGenerator(rescale=1./255)

    def cargar_datos_train_csv(self):
        print("Cargar datos train csv")
        data = pd.read_csv(self.path_entrenamiento)
        imagenes = []
        etiquetas = []
        for index, row in data.iterrows():
            pixels = row['pixels']
            etiqueta = row['emotion']
            imagen = (np.array(list(map(int, pixels.split()))).reshape(48, 48))
            imagenes.append(imagen)
            etiquetas.append(etiqueta)
        imagenes = np.array(imagenes)
        etiquetas = np.array(etiquetas)
        imagenes = np.expand_dims(imagenes, axis=-1)
        etiquetas = to_categorical(etiquetas, num_classes=self.clases)
        x_train = self.data_gen_train.flow(
            imagenes, 
            etiquetas, 
            batch_size=self.batch_size
        )
        self.train_data = x_train

    def cargar_datos_validation_csv(self):
        print("Cargar datos validación csv")
        data = pd.read_csv(self.path_validacion)
        imagenes = []
        etiquetas = []
        for index, row in data.iterrows():
            pixels = row['pixels']
            etiqueta = row['emotion']
            imagen = (np.array(list(map(int, pixels.split()))).reshape(48, 48))
            imagenes.append(imagen)
            etiquetas.append(etiqueta)
        imagenes = np.array(imagenes)
        etiquetas = np.array(etiquetas)
        imagenes = np.expand_dims(imagenes, axis=-1)
        etiquetas = to_categorical(etiquetas, num_classes=self.clases)
        validations = self.data_gen_validation.flow(
            imagenes, 
            etiquetas, 
            batch_size=self.batch_size
        )
        self.validation_data = tf.data.Dataset.from_generator(
            lambda: validations,
            output_signature=(
                tf.TensorSpec(shape=(None, self.altura, self.longitud, 1), dtype=tf.float32),
                tf.TensorSpec(shape=(None, self.clases), dtype=tf.float32)
            )
        )
    
    def cargar_datos_test_csv(self):
        print("Cargar datos test csv")
        data = pd.read_csv(self.path_test)
        imagenes = []
        etiquetas = []
        for index, row in data.iterrows():
            pixels = row['pixels']
            etiqueta = row['emotion']
            imagen = (np.array(list(map(int, pixels.split()))).reshape(48, 48))
            imagenes.append(imagen)
            etiquetas.append(etiqueta)
        imagenes = np.array(imagenes)
        etiquetas = np.array(etiquetas)
        imagenes = np.expand_dims(imagenes, axis=-1)
        etiquetas = to_categorical(etiquetas, num_classes=self.clases)
        x_train = self.data_gen_test.flow(
            imagenes, 
            etiquetas, 
            batch_size=self.batch_size
        )
        self.test_data = x_train
    
    def crear_red(self):
        print("Creacion de la red")
        cnn = tf.keras.models.Sequential() 
        cnn.add(Convolution2D(
            filters=self.filtros_conv1, 
            kernel_size=self.tamano_filtro1,
            padding='same', 
            input_shape=(self.altura, self.longitud, 1), 
            activation='relu'
        ))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool1))
        cnn.add(Convolution2D(
            filters=self.filtros_conv2, 
            kernel_size=self.tamano_filtro2,
            padding='same'
        ))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool1))
        # cnn.add(Convolution2D(
        #     filters=self.filtros_conv3, 
        #     kernel_size=self.tamano_filtro3,
        #     padding='same'
        # ))
        # cnn.add(MaxPooling2D(pool_size=self.tamano_pool1))
        cnn.add(tf.keras.layers.Flatten())
        cnn.add(tf.keras.layers.Dense(256, activation='relu'))
        cnn.add(tf.keras.layers.Dropout(0.5))
        cnn.add(tf.keras.layers.Dense(self.clases, activation='softmax')) 
        cnn.compile(
            loss='categorical_crossentropy', 
            optimizer=optimizers.Adam(learning_rate=self.lr), 
            metrics=['accuracy']
        )
        self.model = cnn
           

    

    def entrenar(self):
        print("Entrenamiento")
        #imprimir resumen de la red
        self.model.summary()
        self.model.fit(x=self.train_data, epochs=self.epocas, steps_per_epoch=self.pasos, batch_size=self.batch_size)
        print("Evaluación")
        self.model.evaluate(self.test_data)

    def save_model(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.model.save(path + "modelo_emociones.h5")
        self.model.save_weights(path + "pesos_emociones.h5")


if __name__ == '__main__':
    path_entrenamiento = "./data/train.csv"
    path_validacion = "./data/validation.csv"
    path_test = "./data/test.csv"
    emociones = Emociones(path_entrenamiento, path_validacion, path_test)
    emociones.entrenar()
    emociones.save_model("./data/")
