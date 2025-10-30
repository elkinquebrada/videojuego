# taberna_scene.py
import pygame
import os
from player import TavernPlayer

class TavernScene:
    
    def __init__(self, manager):
        self.manager = manager
        
        # ... (Configuración de límites y objetos visuales, sin cambios) ...
        self.PLAYER_COLLISION_Y_MIN = 480 
        self.PLAYER_COLLISION_Y_MAX = self.manager.HEIGHT - 10 
        self.WALL_LEFT_X = 300         
        self.WALL_RIGHT_X = self.manager.WIDTH - 50 
        
        self.DOOR_VISUAL_X = self.manager.WIDTH // 2 - 350
        self.DOOR_VISUAL_Y = self.PLAYER_COLLISION_Y_MIN - 360
        self.DOOR_SCALE_WIDTH = 400
        self.DOOR_SCALE_HEIGHT = 350

        COLLISION_HEIGHT = 40 
        self.exit_rect = pygame.Rect(
            self.DOOR_VISUAL_X, 
            self.DOOR_VISUAL_Y + self.DOOR_SCALE_HEIGHT - COLLISION_HEIGHT,
            self.DOOR_SCALE_WIDTH, 
            COLLISION_HEIGHT
        )
        # Aseguramos que el nombre de la escena esté en minúsculas para el manager
        self.next_scene_name = 'world' 
        
        self.COLUMN1_VISUAL_X = 550
        self.COLUMN1_VISUAL_Y = 580
        self.COLUMN_SCALE_WIDTH = 500
        self.COLUMN_SCALE_HEIGHT = 600
        self.COLUMN2_VISUAL_X = 950
        self.COLUMN2_VISUAL_Y = 580
        
        # --- CARGA DE IMÁGENES ---
        self.asset_dir = "assets"
        self.background_image = self._load_background()
        self.door_image = self._load_door()
        self.column_image = self._load_column() 

        # Inicialización del jugador 
        SUELO_INICIAL_Y = 500  
        self.player = TavernPlayer(
            self.manager.WIDTH // 2, 
            SUELO_INICIAL_Y,
            self.manager.WIDTH,
            self.manager.HEIGHT
        ) 
        
        
    def _load_background(self):
        # ... (código para cargar el fondo) ...
        bg_image = None
        bg_path = os.path.join(self.asset_dir, "background", "tavern_background.png") 
        try:
            bg_image = pygame.image.load(bg_path).convert_alpha() 
            bg_image = pygame.transform.scale(bg_image, (self.manager.WIDTH, self.manager.HEIGHT))
        except pygame.error as e:
            print(f"ERROR: No se pudo cargar el fondo en {bg_path}. Detalles: {e}")
            bg_image = pygame.Surface((self.manager.WIDTH, self.manager.HEIGHT)); bg_image.fill((30, 20, 10))
        return bg_image

    def _load_door(self):
        # ... (código para cargar la puerta) ...
        door_image = None
        door_path = os.path.join(self.asset_dir, "background", "tavern_door.png")
        try:
            door_image = pygame.image.load(door_path).convert_alpha()
            door_image = pygame.transform.scale(door_image, (self.DOOR_SCALE_WIDTH, self.DOOR_SCALE_HEIGHT))
        except pygame.error as e:
            print(f"ERROR: No se pudo cargar la puerta: {e}")
            door_image = pygame.Surface((self.DOOR_SCALE_WIDTH, self.DOOR_SCALE_HEIGHT), pygame.SRCALPHA); door_image.fill((255, 0, 0, 150)) 
        return door_image


    def _load_column(self):
        # ... (código para cargar la columna) ...
        column_image = None
        column_path = os.path.join(self.asset_dir, "background", "tavern_colum.png")
        try:
            column_image = pygame.image.load(column_path).convert_alpha()
            column_image = pygame.transform.scale(column_image, (self.COLUMN_SCALE_WIDTH, self.COLUMN_SCALE_HEIGHT))
        except pygame.error as e:
            print(f"ERROR: No se pudo cargar la columna: {e}")
            column_image = pygame.Surface((self.COLUMN_SCALE_WIDTH, self.COLUMN_SCALE_HEIGHT), pygame.SRCALPHA); column_image.fill((0, 0, 255, 150)) 
        return column_image


    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.attack()
        pass
        
    
    # === MÉTODO UPDATE CORREGIDO: LLAMADA LIMPIA ===
    def update(self, dt):
        
        self.player.update(
            dt, # <--- Se pasa dt primero
            self.PLAYER_COLLISION_Y_MIN, 
            self.PLAYER_COLLISION_Y_MAX, 
            self.WALL_LEFT_X,  
            self.WALL_RIGHT_X 
            # No se pasa 'keys'
        ) 
        
        if self.player.rect.colliderect(self.exit_rect):
            print(f"Saliendo de la taberna a la escena: {self.next_scene_name}")
            return {"change_to": self.next_scene_name} 
            
        return None

    def draw(self, surface):
        """Dibuja todos los elementos en orden de profundidad (Y)."""
        
        surface.fill((0, 0, 0)) 
        
        # 1. DIBUJAR FONDO Y PUERTA (elementos de fondo)
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        
        if self.door_image:
            surface.blit(self.door_image, (self.DOOR_VISUAL_X, self.DOOR_VISUAL_Y))
        
        # --- 2. GESTIÓN DE PROFUNDIDAD ---
        
        draw_elements = []
        
        draw_elements.append({
            'y': self.player.rect.bottom, 
            'type': 'player'
        })
        draw_elements.append({
            'y': self.COLUMN1_VISUAL_Y, 
            'type': 'column', 
            'x': self.COLUMN1_VISUAL_X
        })
        draw_elements.append({
            'y': self.COLUMN2_VISUAL_Y, 
            'type': 'column', 
            'x': self.COLUMN2_VISUAL_X
        })
        
        draw_elements.sort(key=lambda item: item['y'])
        
        # === CORRECCIÓN AQUÍ ===
        # Usamos COLUMN1_VISUAL_Y para calcular el desplazamiento Y, 
        # ya que ambas columnas están en el mismo plano Y (650)
        if self.column_image:
            # Calcula dónde empieza el dibujo de la columna (base Y - altura)
            column_draw_y_offset = self.COLUMN1_VISUAL_Y - self.COLUMN_SCALE_HEIGHT
        
        for element in draw_elements:
            if element['type'] == 'player':
                self.player.draw(surface)
                
            elif element['type'] == 'column':
                # El dibujo usa la posición X específica del elemento, pero el mismo offset Y
                surface.blit(self.column_image, (element['x'], column_draw_y_offset))