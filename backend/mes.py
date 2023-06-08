import algoritmos
import clasificador_haar
import predecir_emocion
import cv2


clasificador_haar = clasificador_haar.ClasificadorHaar()

def predic_one(img, id_user):
    detected_probability = clasificador_haar.detectar_atencion(img)
    pre_proccessed_img = algoritmos.calibrar_imagen(img)
    emotion = predecir_emocion.predict(pre_proccessed_img)
    
    engaged = algoritmos.engaged(detected_probability, emotion)
    
    print("Focused: ", detected_probability)
    print("Emotion: ", emotion)
    print("Engaged proba: ", engaged)


def predic_many(img, ids_user):
    pass


if __name__ == "__main__":
    ruta = 'C:\\Users\\bryam\\Downloads\\yo3.jpg'
    img = cv2.imread(ruta)
    predic_one(img, 1)
    