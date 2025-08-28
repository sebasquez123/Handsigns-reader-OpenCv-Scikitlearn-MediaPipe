import time
import os
import pygame

class CommandAudioPlayer:
    def __init__(self, audio_folder):
        self.audio_folder = os.path.abspath(audio_folder)
        self.last_command = None
        self.command_start_time = None
        self.is_playing = False
        pygame.mixer.init()

    def _play_audio(self, audio_path):
        self.is_playing = True
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        print("SI REPRODUCE")
        return True
    

    def process_command(self, handCommand,qrCommand):
        #si no hay comandos rompe la fila.
        if handCommand is None and qrCommand is None:
            return
        ## aqui hay que priorizar los Qr, cuando haya mas de 1 comando, se selecciona el Qr.
        command = qrCommand if qrCommand is not None else handCommand
        command = command.strip().upper()
        print(f"Comando procesado: {command}")
        now = time.time()        
        # pregunta si se esta reproduciendo el audio siempre.
        if self.is_playing and command != "SALUDA":
            self.is_playing = pygame.mixer.music.get_busy()
            #si se esta reproduciendo se rompe la fila
            return  
        #si el comando cambia en el tiempo el contador queda actualizado para no contener diferencias.
        if command != self.last_command:
            self.last_command = command
            self.command_start_time = now
            return
        # Si el comando se mantiene con el tiempo por 1 segundo. 
        if now - self.command_start_time >= 1  and command != "NO GESTURE":
            if command == 'SALUDA':
                self.is_playing = False
                self.last_command = None
                self.command_start_time = None
                pygame.mixer.music.stop()
                return
            audio_path = os.path.join(self.audio_folder, f"{command}.mp3")
            print(f"Reproduciendo audio: {audio_path}")
            if os.path.exists(audio_path):
                value = self._play_audio(audio_path)  
                self.is_playing = value                
            self.last_command = None
            self.command_start_time = None
