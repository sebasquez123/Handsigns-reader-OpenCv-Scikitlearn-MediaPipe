## THIS FILE FOR LOCAL DEMO ONLY
from src.local.core.data_preprocess import procesar_imagenes
from src.local.core.model_training import preentrenamiento, entrenamiento_final
from src.local.core.inference import test_model
from src.local.serverless.demo import demo

dir_processed = 'data/gestures.csv'
dir_model = 'models/modelo_entrenado.pkl'


print(" What do you want to do?")
print("1. Recolectar gestos (MediaPipe Hands).")
print("2. Train model & find best parameters")
print("   (Do not forget to extract the best tree depth!!)")
print("3. Start testing with trained model")
print("   (Make sure you have at least one model already set (test in live))")
print("4. Start demo (lectura de QR en vivo)")
print("   (Cámara requerida. Pulsa q para salir.)")

comand = input("select an option: ")
if(comand == '1'):
    # Lanza interfaz de recolección. Se pedirá etiqueta si no se pasa.
    procesar_imagenes()
elif(comand == '2'):
    # entrenamiento parcial para encontrar la mejor profundidad del arbol
    preentrenamiento(dir_processed)
    comand2 = input("would you like to train the model with the best parameters? (y/n)")
    if comand2 == 'y':
        best_depth = input("introduce the best parameter of depth: ")
        entrenamiento_final(best_depth, dir_processed)
elif(comand == '3'):
    test_model(dir_model)
   
elif(comand == '4'):
    demo(dir_model)


