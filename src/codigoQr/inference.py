import joblib
import os
import cv2
import numpy as np
import pandas as pd

def test_model(dir_test):
    archivo = os.listdir(dir_test)
    if not archivo:
        raise FileNotFoundError(f'No se encontraron archivos en el gestor de muestras')
    if not archivo[0].endswith('.jpg'):
        raise FileExistsError(f'El archivo {archivo[0]} no es una imagen en formato jpg')
    path = os.path.join(dir_test, archivo[0])
    
    imagen = cv2.imread(path)
    imagen = cv2.resize(imagen, (128, 128))
    imagen = imagen.flatten()
    imagen = imagen/255.0 
    
    feature =[]
    feature.append(imagen)
    feature = np.array(feature)

    columnas_pixeles = [f'pixel_{i}' for i in range(feature.shape[1])]
    x_test = pd.DataFrame(feature, columns=columnas_pixeles)
    
    model = joblib.load('models/modelo_entrenado.pkl')
    prediccion = model.predict(x_test)
    
    return prediccion
