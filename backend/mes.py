import algoritmos
import clasificador_haar
import predecir_emocion
import cv2
import io
import base64
from PIL import Image
import json
clasificador_haar = clasificador_haar.ClasificadorHaar()

def predic_one(img, id_user):
    detected_probability = clasificador_haar.detectar_atencion(img)
    pre_proccessed_img = algoritmos.calibrar_imagen(img)
    emotion = predecir_emocion.predict(pre_proccessed_img)
    
    engaged = algoritmos.engaged(detected_probability, emotion)
    data = {
        "Focused": detected_probability,
        "Emotion": emotion,
        "Engaged proba": engaged
    }
    print("Focused: ", detected_probability)
    print("Emotion: ", emotion)
    print("Engaged proba: ", engaged)
    return data



def base64_to_png(base64_string):
    output_file = "./images/imagen.png"
    # Decodificar la cadena Base64 a bytes
    image_bytes = base64.b64decode(base64_string)

    # Crear un objeto BytesIO para leer los bytes como archivo
    image_buffer = io.BytesIO(image_bytes)

    # Abrir la imagen utilizando PIL (Python Imaging Library)
    image = Image.open(image_buffer)

    # Guardar la imagen en formato PNG
    image.save(output_file, "PNG")

    return output_file




def predic_many(img, ids_user):
    pass

"""
if __name__ == "__main__":

    ruta = 'D:\\TEC-GIT\\Git\\Operativos\\EmotionRecognition\\EmotionRecognitionProject\\backend\\images\imagen.png'
    img = cv2.imread(ruta)
    predic_one(img, 1)

"""


