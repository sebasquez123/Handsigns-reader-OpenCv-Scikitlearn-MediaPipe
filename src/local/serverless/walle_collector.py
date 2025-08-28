## este archivo se encarga de interactuar entre el archivo de camara y el archivo de acciones, es quien
## coordina la captura de imagenes y el procesamiento de las mismas para la toma de decisiones.

## Manejara logica de modelo-accion, habilitando la lectura de la camara y la ejecucion de acciones
## basado en tiempos prudentes de espera.

## REQUISITOS:
## el robot inicia viendo todo, debe esperar una señal de inicio con un QR. y una señal de parada con otro QR.
## si el robot esta habilitado para moverse, espera por cualquier señal de vision que pueda decodificar y enviar al colector.
## el robot debera procesar la primera señal recibida, esperara un tiempo prudente para detectar si la señal es la misma para poder ejecutarla.
## si durante XX segundos el robot recibe la misma señal especifica, la ejecuta, de lo contrario, anula la ejecucion y sigue esperando.
## el robot entra en un estado de espera activa, el algoritmo dira cuando ha terminado la accion para recibir nuevas señales y empezar de nuevo.


## la transmision por WEBRTC y la captura de imagenes se realizara de manera simultanea pero en diferentes interpretes o hilos.