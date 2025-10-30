# world_scene.py

import pygame
import sys # sys no es estrictamente necesario aquí, pero a veces se usa

class WorldScene:
    def __init__(self, manager):
        self.manager = manager
        print("¡ESCENA MUNDO CARGADA EXITOSAMENTE! (Presiona ESC para volver a la Taberna)")
        # Cargar una fuente para el texto
        self.font = pygame.font.Font(None, 74)
        
    def handle_input(self, event):
        # Maneja cualquier input específico del mapa mundial aquí
        pass

    # world_scene.py
# ...
    def update(self, dt):
        
        self.player.update(
            dt,  # <--- Debe ser dt primero
            self.PLAYER_COLLISION_Y_MIN, 
            self.PLAYER_COLLISION_Y_MAX,
            self.PLAYER_COLLISION_X_MIN,
            self.PLAYER_COLLISION_X_MAX
        )
# ...

    def draw(self, surface):
        surface.fill((50, 100, 50)) # Color verde oscuro para el mapa
        
        # Dibuja texto de placeholder
        text = self.font.render("MUNDO EXTERIOR", True, (255, 255, 255))
        surface.blit(text, (self.manager.WIDTH // 2 - text.get_width() // 2, 
                           self.manager.HEIGHT // 2 - text.get_height() // 2))