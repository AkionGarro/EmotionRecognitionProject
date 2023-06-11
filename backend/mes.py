import algoritmos
import clasificador_haar
import cv2
import io
import base64
from PIL import Image
import json
clasificador_haar = clasificador_haar.ClasificadorHaar()

def predic_one(img, id_user):
    detected_probability = clasificador_haar.detectar_atencion(img)
    pre_proccessed_img = algoritmos.calibrar_imagen(img)
    emotion = algoritmos.predict_emotions(pre_proccessed_img)
    
    engaged = algoritmos.engaged(detected_probability, emotion)
    data = {
        "Id":id_user,
        "Focused": detected_probability,
        "Emotion": emotion,
        "EngagedProba": engaged
    }
    res = formatData(data)
    return res



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



def formatData(jsonData):

    categories = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    values = jsonData['Emotion']
    engaged = jsonData["EngagedProba"]
    focus = jsonData["Focused"]
    id = jsonData["Id"]
    emotionsInfo = {}
    for category, value in zip(categories, values):
        emotionsInfo[category] = value


    engagedInfo ={
        'result': engaged[0],
        'probability': engaged[1]
    }

    Id:"12345678"
    formatedJson = {
        'Id': id,
        'EmotionsInfo': emotionsInfo,
        'EngagedInfo': engagedInfo,
        'Focused': focus,
    }
    return formatedJson

def promediar(json_list):
    num_items = len(json_list)
    total_probability = 0.0
    total_focused = 0.0
    id = 0
    emotions_total = {'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}

    for json_data in json_list:
        total_probability += json_data['EngagedInfo']['probability']
        total_focused += json_data['Focused']
        print(json_data['Focused'])
        emotions = json_data['EmotionsInfo']
        for key in emotions_total:
            emotions_total[key] += emotions[key]

    id = json_list[0]['Id']

    average_probability = total_probability / num_items
    average_focused = total_focused / num_items
    average_emotions = {key: value / num_items for key, value in emotions_total.items()}

    result = 'Engaged' if average_probability >= 0.4 else 'Not Engaged'
    output_json = {
        'Id': id,
        'EmotionsInfo': average_emotions,
        'EngagedInfo': {'result': result, 'probability': average_probability},
        'Focused': average_focused
    }

    return output_json

def predic_many(img, ids_user):
    imagenes = algoritmos.extraer_rostros(img)
    results = []
    for imagen in imagenes:
        result = predic_one(imagen, ids_user)
        results.append(result)
    
    promedio = promediar(results)
    print("\n", promedio)
    return promedio

# if __name__ == "__main__":

#     ruta = 'C:\\Users\\bryam\\Pictures\\Camera Roll\\pruebas\\g4.jpg'
#     img = cv2.imread(ruta)
#     predic_many(img, 1)



