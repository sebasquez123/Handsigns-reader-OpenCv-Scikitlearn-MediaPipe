
from demo import demo
import os

# Obtener el directorio absoluto de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir rutas absolutas relativas a este archivo
dir_model = os.path.join(BASE_DIR, './model/modelo_entrenado.pkl')
dir_audio = os.path.join(BASE_DIR, './audio/')

# Normalizar rutas
dir_model = os.path.normpath(dir_model)
dir_audio = os.path.normpath(dir_audio)

demo(dir_model, dir_audio)