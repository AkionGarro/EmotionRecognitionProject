import cv2
import matplotlib.pyplot as plt

class ClasificadorHaar:
    def __init__(self):
        # Cargar los clasificadores Haar para rostros y ojos
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        self.eye_cascade_glass = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def detectar_atencion(self, imagen):
        # Convertir la imagen a escala de grises
        try:
            gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        except:

            gray = imagen

        # Detectar rostros en la imagen
        rostros = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        total_rostros_posibles = len(rostros)
        partes_detectadas = 0

        if total_rostros_posibles == 0:
            return 0.0

        # Detectar si hay rostro y ojos en el primer rostro detectado
        if len(rostros) > 0:
            partes_detectadas += 1
            (x, y, w, h) = rostros[0]  # Tomar solo el primer rostro detectado

            # Recortar la región del rostro de la imagen original
            rostro_recortado = imagen[y:y+h, x:x+w]

            # Detectar ojos en la imagen recortada
            ojos = self.eye_cascade.detectMultiScale(rostro_recortado, 1.3, 5)

            # Si se detecta un ojo
            if len(ojos) > 0:
                if len(ojos) == 1:
                    partes_detectadas += 1
                elif len(ojos) == 2:
                    partes_detectadas += 2
            else:
                ojos = self.eye_cascade_glass.detectMultiScale(rostro_recortado, 1.3, 5)
                if len(ojos) > 0:
                    if len(ojos) == 1:
                        partes_detectadas += 1
                    elif len(ojos) == 2:
                        partes_detectadas += 2
            

        # Calcular la probabilidad de atención
        probabilidad_detectada = partes_detectadas / 3.0
        return probabilidad_detectada
