
from src.codigoQr.data_preprocess import procesar_imagenes, crear_dataframe
from src.codigoQr.model_training import preentrenamiento, entrenamiento_final
from src.codigoQr.inference import test_model
from src.codigoQr_Demo.demo import demo
dir_processed = 'data/process images/tensors'
dir_raw = 'data/process images/raw'
dir_labels = 'data/process images/labels/images.csv'
dir_test = 'data/single test'




print(" What do you want to do?")
print("1. Prepocess images and launch tensors")
print("   (Make sure you have the images in raw!!)")
print("   (Make sure you have also the labels in labels!!)")
# print("2. Train model & find best parameters")
# print("   (Do not forget to extract the best tree depth!!)")
# print("3. Test model with a single image")
# print("   (Make sure you have at least an image into the <test> folder!!)")
print("4. Start demo (lectura de QR en vivo, no usa el modelo de arbol)")
print("   (Cámara requerida. Pulsa q para salir.)")

comand = input("type 1 or 4: ")
df = None
if(comand == '1'):
    procesar_imagenes(dir_raw, dir_processed)
    df= crear_dataframe(dir_processed,dir_labels)
    print(df)
# elif(comand == '2'):
#     # entrenamiento parcial para encontrar la mejor profundidad del arbol
#     preentrenamiento(df)
#     comand2 = input("would you like to train the model with the best parameters? (y/n)")
#     if comand2 == 'y':
#         best_depth = input("introduce the best parameter of depth")
#         entrenamiento_final(best_depth,df)
# elif(comand == '3'):
#     y = test_model(dir_test)
#     print(y)
elif(comand == '4'):
    demo()
