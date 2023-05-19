import cv2
import matplotlib.pyplot as plt
import argparse
import time
import clasificador_haar

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
            #rostro_recortado = cv2.resize(rostro_recortado, (48, 48))



            #guardar imagen recortada
            cv2.imwrite('C:\\Users\\bryam\\Downloads\\rostro_recortado1.jpg', rostro_recortado)

        # Iterar sobre los rostros detectados
        for (x, y, w, h) in rostros:
            # Recortar la región del rostro de la imagen original
            rostro_recortado = imagen[y:y+h, x:x+w]
           
            # Redimensionar el rostro recortado a 40x40
            #rostro_recortado = cv2.resize(rostro_recortado, (48, 48))

            # Guardar la imagen recortada (desarrollo)
            cv2.imwrite('C:\\Users\\bryam\\Downloads\\rostro_recortado.jpg', rostro_recortado)

        
        # Mostrar la imagen con el rectángulo dibujado
        # plt.imshow(cv2.cvtColor(rostro_recortado, cv2.COLOR_BGR2RGB))
        # plt.axis('off')
        # plt.show()
        return rostro_recortado


calibrar_imagen(cv2.imread('C:\\Users\\bryam\\Pictures\\Camera Roll\\pruebas\\yo3.jpg'))

def detectAndDisplay(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        detector = clasificador_haar.ClasificadorHaar()
        engaged = detector.detectar_atencion(frame)
        center_alt = (x + w//5, y-15)
        if engaged:
            #dibujar la palabra Engaged en la imagen en center_alt
            frame = cv2.putText(frame, 'Engaged', center_alt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        else:
            #dibujar la palabra Engaged en la imagen en center_alt
            frame = cv2.putText(frame, 'Not Engaged', center_alt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    cv2.imshow('Capture - Face detection', frame)

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

camera_device = args.camera
#-- 2. Read the video stream
cap = cv2.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    time.sleep(0.025)
    if cv2.waitKey(10) == 27:
        break