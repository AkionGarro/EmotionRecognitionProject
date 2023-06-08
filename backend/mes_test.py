import argparse
import random
import time
import cv2
import clasificador_haar
import predecir_emocion_test
import algoritmos

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

emotion = "Emotion"
frame_for_emotion = None

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
        center_baj = (x + w//5, y+h+15)
        if engaged:
            #dibujar la palabra Engaged en la imagen en center_alt
            frame = cv2.putText(frame, 'Focused', center_alt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            #dibujar la emocion en la imagen en center_baj
            frame = cv2.putText(frame, emotion, center_baj, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        else:
            #dibujar la palabra Engaged en la imagen en center_alt
            frame = cv2.putText(frame, 'Not Focused', center_alt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            #dibujar la emocion en la imagen en center_baj
            frame = cv2.putText(frame, emotion, center_baj, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        count = 0
        for (x2,y2,w2,h2) in eyes:
            if count == 2:
                break
            count += 1
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
        break #solo se toma el primer rostro detectado
    cv2.imshow('Capture - Face detection', frame)

def start_stream():
    global frame_for_emotion
    global emotion
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
        frame_for_emotion = frame
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        frame_for_emotion = algoritmos.calibrar_imagen(frame_for_emotion)
        emotion = predecir_emocion_test.predict(frame_for_emotion)
        detectAndDisplay(frame)
        #esperar para no sobrecargar el procesador
        time.sleep(0.2)
        if cv2.waitKey(10) == 27:
            break

if __name__ == '__main__':
    print("Starting stream")
    start_stream()