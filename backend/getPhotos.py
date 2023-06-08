import cv2
import pyautogui
import numpy as np
import mes


def obtener_fotos():
    # Dimensiones de la pantalla
    screen_info = pyautogui.size()
    # Crea una ventana para mostrar el video
    cv2.namedWindow("Capturando", cv2.WINDOW_NORMAL)
    #Duración entre que se toma cada foto
    duracion = 0
    #Numero de imagen
    i=0
    while True:
        print(duracion)
        # Captura la pantalla
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        # Muestra el video en tiempo real
        cv2.imshow("Capturando", frame)
        #Cada 60 guarda la foto
        if duracion == 60:
            #cv2.imwrite('nueva_imagen'+str(i)+'.jpg', frame)
            #falta id_user
            result = mes.predic_one(frame, None)
            i = i+1
            duracion = 0    
        duracion += 1

        #IMPORTANTE
        # Detiene la ejecución si se presiona la tecla 'q'
        if cv2.waitKey(1) == ord("q"):
            break

    # Libera los recursos y cierra las ventanas
    cv2.destroyAllWindows()

if __name__ == '__main__':
    obtener_fotos()