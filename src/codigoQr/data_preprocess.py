##Inicialmente se procesan las imagenes de redimensionandolas

import os
import cv2
import numpy as np
import pandas as pd




def tratamiento(ruta,i):
    
    imagen = cv2.imread(ruta) #Cargar imagen y la almacena en la variable imagen
    if imagen is None:
        raise FileNotFoundError(f'No se pudo cargar la imagen {ruta}')
    imagen = cv2.resize(imagen,(128,128)) #Redimensionar la imagen a 128x128
    # imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #Convertir la imagen a escala de grises
    imagenmpy = imagen.flatten() #Aplanar la imagen y devolverla. flatten convierte la matriz en un arreglo unidimensional
    imagenmpy = imagenmpy/255.0 #Normalizar la imagen dividiendo cada pixel por 255.0
    return imagenmpy




## preprocesamiento de la imagen
def procesar_imagenes(dir_raw, dir_processed):
    if not os.path.exists(dir_processed):
        os.makedirs(dir_processed)
    i = 0
    archivos = os.listdir(dir_raw)
    archivos_ordenados = sorted(archivos, key=lambda x: int(''.join(filter(str.isdigit, x))))
    print(archivos_ordenados)
    if not archivos:
        raise FileNotFoundError(f'No se encontraron archivos en el gestor de muestras')
    for file in archivos_ordenados:
       
        if not file.endswith('.jpg'):
           raise FileExistsError(f'El archivo {file} no es una imagen jpg')
        ruta = os.path.join(dir_raw, file)
        imagen_procesada= tratamiento(ruta,i)
        np.save(os.path.join(dir_processed, f"muestra{i}_reducida.npy"), imagen_procesada) ## se guarda la imagen con numpy porque numpy ofrece una forma de guardar y cargar matrices dimensionales eficiente. 
        i+=1
        print(f'Imagen {file} guardada en {dir_processed}')
    
    
    
def crear_dataframe(dir_processed,dir_labels):
    procesado = []
    i=0
    archivos_procesados = os.listdir(dir_processed)
    archivos_ordenados = sorted(archivos_procesados, key=lambda x: int(''.join(filter(str.isdigit, x))))
    for file in archivos_ordenados:
        
        if not file.endswith('.npy'):
            print (f'El archivo {file} no es un archivo numpy')
            continue
        dir_de_cada_archivo = os.path.join(dir_processed, file)
        numpyarray= np.load(dir_de_cada_archivo)
        procesado.append(numpyarray)

        print(f'Imagen {file} cargada en el dataframe')
        i+=1
    procesado = np.array(procesado)
    columnas_pixeles =[f'pixel_{i}' for i in range(procesado.shape[1])]  
   
    #data frame con las imagenes procesadas
    imagenes = pd.DataFrame(procesado, columns=columnas_pixeles)
    #data frame con los labels o salidas
    labels = pd.read_csv(dir_labels, sep=';')
    #dataframe completo
    fullDataFrame = pd.concat([labels,imagenes], axis=1)
 
    return fullDataFrame