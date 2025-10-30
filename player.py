# player.py
import pygame
import os
import math

# --- VARIABLES DE CONFIGURACIÓN ---
SCALE_FACTOR = 0.15 
AXE_GRAY = (128, 138, 145)

# -------------------------------------------------------------
# --- AXE CLASS (Placeholder) ---
class Axe:
    def __init__(self):
        self.attack_angle = 0
    
    def draw(self, surface, x, y, direction, is_attacking, attack_frame):
        if is_attacking:
            color = AXE_GRAY if attack_frame % 5 < 3 else (255, 0, 0)
            pygame.draw.circle(surface, color, (int(x + 20), int(y - 20)), 10)

class TavernPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, manager_width, manager_height): 
        super().__init__()
        
        # Las variables manager_width/height se ignoran aquí, pero se mantienen para no romper el constructor de las escenas
        self.speed = 200     
        self.depth_speed_factor = 0.5 

        self.x = float(x)
        self.y = float(y)
        self.direction = 'front'
        self.is_walking = False
        self.is_attacking = False
        
        self.animation_speed = 0.2 
        self.attack_duration = 10 
        self.attack_frame = 0
        self.axe = Axe()
        
        self.animations = self._load_animations()
        self.current_animation_key = 'front_idle'
        self.animation_step = 0.0
        
        self.image = self.animations[self.current_animation_key][0]
        self.rect = self.image.get_rect(midbottom=(int(self.x), int(self.y))) 
        
    def get_scale(self, floor_y_min, floor_y_max):
        # ... (código de escalado 2.5D) ...
        min_scale = 0.6
        max_scale = 0.9
        y_range = max(1, floor_y_max - floor_y_min)
        y_normalized = (self.y - floor_y_min) / y_range
        y_normalized = max(0.0, min(1.0, y_normalized)) 
        return min_scale + y_normalized * (max_scale - min_scale)

    def _load_animations(self):
        """
        Loads all sprite images, SCALING them by SCALE_FACTOR using smoothscale.
        """
        animations = {}
        base_path = 'assets'
        
        def scale_image(image):
            """Helper to scale a single image using smoothscale."""
            new_width = int(image.get_width() * SCALE_FACTOR)
            new_height = int(image.get_height() * SCALE_FACTOR)
            # Usando smoothscale para mejor calidad
            return pygame.transform.smoothscale(image, (new_width, new_height))

        def load_walk_sequence(folder_name, count):
            """Loads numbered files (1.png to N.png) from a subfolder and scales."""
            frames = []
            folder_path = os.path.join(base_path, folder_name)
            for i in range(1, count + 1):
                file_path = os.path.join(folder_path, f'{i}.png')
                try:
                    image = pygame.image.load(file_path).convert_alpha()
                    image = scale_image(image)
                    frames.append(image)
                except pygame.error:
                    print(f"Warning: Missing sprite {file_path}. Using placeholder.")
                    placeholder = pygame.Surface((30, 60), pygame.SRCALPHA)
                    placeholder.fill((255, 0, 255, 100)) 
                    placeholder = scale_image(placeholder)
                    frames.append(placeholder)
            return frames
        
        # --- IDLE (Front) ---
        front_idle_path = os.path.join(base_path, 'Idle', 'Front.png')
        try:
            front_idle_image = pygame.image.load(front_idle_path).convert_alpha()
            front_idle_image = scale_image(front_idle_image)
        except pygame.error:
            print(f"ERROR: Missing Front Idle sprite at {front_idle_path}. Using placeholder.")
            front_idle_image = pygame.Surface((30, 60), pygame.SRCALPHA)
            front_idle_image.fill((0, 0, 255, 150))
            front_idle_image = scale_image(front_idle_image)
            
        animations['front_idle'] = [front_idle_image]
        
        # --- IDLE (Back) ---
        back_idle_path = os.path.join(base_path, 'Idle', 'Back.png')
        try:
            back_idle_image = pygame.image.load(back_idle_path).convert_alpha()
            back_idle_image = scale_image(back_idle_image)
        except pygame.error:
            print(f"ERROR: Missing Back Idle sprite at {back_idle_path}. Using front_idle fallback.")
            back_idle_image = front_idle_image 

        # --- IDLE (Right/Left) ---
        right_left_idle_path = os.path.join(base_path, 'Idle', 'Right_Left.png')
        try:
            right_idle_image = pygame.image.load(right_left_idle_path).convert_alpha()
            right_idle_image = scale_image(right_idle_image)
        except pygame.error:
            print(f"ERROR: Missing Right/Left Idle sprite at {right_left_idle_path}. Using front_idle placeholder.")
            right_idle_image = front_idle_image 
            
        # ------------------------------------------------
        # --- SECCIONES DE WALK CORREGIDAS Y AÑADIDAS ---
        # ------------------------------------------------
            
        # --- WALK (Right/Left - 16 Frames) ---
        walk_frames_right = load_walk_sequence('Right_Left_Walk', 16)
        animations['right_walk'] = walk_frames_right
        animations['left_walk'] = [pygame.transform.flip(f, True, False) for f in walk_frames_right]
        
        # --- WALK (Front - Asumiendo 12 Frames) ---
        # Si tienes más o menos frames, cambia el número '12' aquí.
        walk_frames_front = load_walk_sequence('Front_Walk', 12) 
        animations['front_walk'] = walk_frames_front
        
        # --- WALK (Back - Usando placeholder por ahora, si no tienes sprites Back_Walk) ---
        # Si tienes una carpeta 'Back_Walk' con sprites, usa: load_walk_sequence('Back_Walk', N)
        placeholder_walk_frame = walk_frames_front[0] if walk_frames_front else front_idle_image 
        animations['back_walk'] = [placeholder_walk_frame] * 4 

        # --- ANIMACIONES ESTÁTICAS FINALES ---
        animations['back_idle'] = [back_idle_image] 
        animations['right_idle'] = [right_idle_image] 
        animations['left_idle'] = [pygame.transform.flip(right_idle_image, True, False)]
        
        # --- ATTACK PLACEHOLDERS ---
        placeholder_attack = [front_idle_image] * self.attack_duration
        animations['front_attack'] = placeholder_attack
        animations['back_attack'] = placeholder_attack
        animations['right_attack'] = placeholder_attack
        animations['left_attack'] = placeholder_attack
        
        return animations
    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            self.animation_step = 0.0

    # === MÉTODO UPDATE CORREGIDO: SOLO RECIBE DT Y LÍMITES ===
    def update(self, dt, floor_y_min, floor_y_max, wall_left_x, wall_right_x):
        keys = pygame.key.get_pressed() # <--- El jugador obtiene las teclas internamente
        
        # Ataque
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame >= self.attack_duration:
                self.is_attacking = False
                self.attack_frame = 0
        
        self.is_walking = False
        
        # Movimiento
        if not self.is_attacking:
            move_x, move_y = 0, 0
            
            # La lógica de movimiento usa las teclas obtenidas localmente
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move_x -= self.speed; self.direction = 'left'; self.is_walking = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move_x += self.speed; self.direction = 'right'; self.is_walking = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                move_y -= self.speed * self.depth_speed_factor; self.direction = 'back'; self.is_walking = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                move_y += self.speed * self.depth_speed_factor; self.direction = 'front'; self.is_walking = True
                
            self.x += move_x * dt
            self.y += move_y * dt
        
        # Colisión y Límites
        self.x = max(wall_left_x, min(self.x, wall_right_x))
        self.y = max(floor_y_min, min(self.y, floor_y_max))
        
        # Animación
        if self.is_walking or self.is_attacking:
            self.animation_step += self.animation_speed 
        else:
            self.animation_step = 0.0

        state = 'attack' if self.is_attacking else ('walk' if self.is_walking else 'idle')
        self.current_animation_key = f'{self.direction}_{state}'

        frames = self.animations.get(self.current_animation_key, self.animations['front_idle'])
        num_frames = len(frames)
        frame_index = int(self.animation_step) % num_frames if not self.is_attacking else self.attack_frame
        frame_index = min(frame_index, num_frames - 1)
        
        # Aplicar Escala 2.5D y Actualizar Rect
        current_scale = self.get_scale(floor_y_min, floor_y_max)
        base_image = frames[frame_index]
        
        scaled_width = int(base_image.get_width() * current_scale)
        scaled_height = int(base_image.get_height() * current_scale)
        
        self.image = pygame.transform.smoothscale(base_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(midbottom=(int(self.x), int(self.y))) 


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.is_attacking:
            self.axe.draw(surface, self.x, self.rect.centery, self.direction, 
                          self.is_attacking, self.attack_frame)