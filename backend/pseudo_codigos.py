import pandas as pd
import numpy as np

def calculate_emotions_factors(dataset_path = "./MES_dataset.csv"):
    # Cargar el conjunto de datos desde el archivo CSV
    dataset = pd.read_csv(dataset_path, na_values='-')

    # Rellenar los valores nulos con 0
    dataset.fillna(0, inplace=True)

    # Calcular la suma de las frecuencias de cada emoción
    emotions_sum = dataset.sum(axis=0)

    # Asignar pesos a cada emoción basados en su frecuencia
    emotions_weights = emotions_sum / emotions_sum.sum()

    # Normalizar los pesos para asegurarse de que sumen 1
    emotions_factors = emotions_weights / emotions_weights.sum()

    return emotions_factors.tolist()

def engaged(focused_value, emotions_weights):
    # Definir el peso de cada emoción (puedes ajustar estos valores según tus necesidades)
    emotions_factors = calculate_emotions_factors()
    print(emotions_factors)

    # Multiplicar cada peso de emoción por su respectivo valor en emotions_weights
    weighted_emotions = [factor * weight for factor, weight in zip(emotions_factors, emotions_weights)]

    # Calcular el tercer parámetro como la suma ponderada del valor de focused y las emociones
    sum_emotions = sum(weighted_emotions)
    engagement_level = focused_value + sum_emotions

    # Comparar con el umbral y determinar si está "engaged" o "not engaged"
    if engagement_level > 0.7:
        return ["engaged", engagement_level]
    else:
        return ["not engaged", engagement_level]
    

result = calculate_emotions_factors('D:\\Memoria huawei pc\\MES_dataset.csv')
suma = 0

for i in result:
    suma = suma + i
    print(i)

print("suma: ", suma)

# focused_value = 0.5
# emotions_weights = [0.99938309, 0.00000000, 0.00000593, 0.00000000, 0.00000001, 0.00000000, 0.00061098]

# result = engaged(focused_value, emotions_weights)
# print(result)  # Imprime "engaged" o "not engaged" según el umbral establecido
