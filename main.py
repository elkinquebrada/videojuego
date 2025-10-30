# scene_manager.py
import pygame
import random
import math
import os
import sys
#-------------------------------------------
#Las importaciones de las escenas iran aquí
#-------------------------------------------
from tavern_scene import TavernScene # Importa la escena de la taberna
from world_scene import WorldScene #Importa la escena de las afueras de la taberna

class SceneManager:
    def __init__(self):
        pygame.init()
        # Configuración de la Pantalla (Usando tus valores de alta resolución)
        self.WIDTH, self.HEIGHT = 1600, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 
                                                pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Cuentos de Mentes Estrelladas - Demo 2.5D")

        self.clock = pygame.time.Clock()
        self.running = True
    
        # Inicializar la escena de la taberna
        self.scenes = {
            "TavernScene": TavernScene(self),
            "WorldScene": WorldScene(self)
        }
        self.current_scene = self.scenes["TavernScene"]

    def change_scene(self, new_scene_name):
        # Aquí irá la lógica para cambiar a 'mundo', 'menu', etc.
        if new_scene_name == "TavernScene":
            self.current_scene = TavernScene(self)
        # elif new_scene_name == "mundo":
        #     self.current_scene = WolrdScene(self)
        if new_scene_name == "WorldScene":
            self.current_scene = WorldScene(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000 # Delta time y límite a 60 FPS

            # Manejo de Eventos y Salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Permite a la escena manejar eventos (como atacar o interactuar)
                self.current_scene.handle_input(event)
            
            # Actualizar la lógica de la escena
            scene_command = self.current_scene.update(dt)

            if scene_command and "change_to" in scene_command:
                self.change_scene(scene_command["change_to"])

            # Dibujar y mostrar
            self.current_scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game_manager = SceneManager()
    game_manager.run()