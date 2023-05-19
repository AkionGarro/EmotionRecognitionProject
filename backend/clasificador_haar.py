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
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en la imagen
        rostros = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(rostros) == 0:
            return False

        face_deted = False
        eye_detected = False
        detectado = False

        # detectar si hay rostro
        for (x, y, w, h) in rostros:
            face_deted = True

            # Recortar la región del rostro de la imagen original
            rostro_recortado = imagen[y:y+h, x:x+w]

            # Detectar ojos en la imagen recortada
            ojos = self.eye_cascade.detectMultiScale(rostro_recortado, 1.3, 5)

            #si se detecta un ojo
            if len(ojos) > 0:
                eye_detected = True
            else:
                ojos = self.eye_cascade_glass.detectMultiScale(rostro_recortado, 1.3, 5)
                if len(ojos) > 0:
                    eye_detected = True
            break
        
        #si se detecta un rostro y un ojo
        if face_deted and eye_detected:
            detectado = True
        else:
            detectado = False

        return detectado


# # Crear una instancia de la clase Deteccion
# detector = ClasificadorHaar()

# # # Cargar imagenes desde una carpeta a una lista
# import os

# categories = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
# images = []
# labels = []



# for filename in os.listdir("C:\\Users\\bryam\\Pictures\\Camera Roll\\pruebas"):
#     image_path = os.path.join("C:\\Users\\bryam\\Pictures\\Camera Roll\\pruebas", filename)
#     gray_image = cv2.imread(image_path)

#     print("Engagement: ", detector.detectar_atencion(gray_image), "     File: ", filename)