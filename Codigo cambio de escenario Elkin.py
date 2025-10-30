# main.py - Sistema completo del juego
import pygame
import random
import math
import os
import sys

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================
WIDTH, HEIGHT = 1280, 720
SCALE_FACTOR = 0.10

# Colores
BLACK = (10, 10, 15)
DARK_GRAY = (30, 30, 40)
UI_DARK = (20, 15, 25, 200)
UI_BORDER = (80, 70, 90)
UI_TEXT = (200, 190, 180)
UI_HIGHLIGHT = (150, 120, 100)
AXE_GRAY = (128, 138, 145)
HANDLE_BROWN = (76, 47, 28)
DARK_METAL_GRAY = (90, 95, 100)

# ============================================================================
# CLASE AXE (Hacha del jugador)
# ============================================================================
class Axe:
    def __init__(self):
        self.attack_angle = 0
        
    def draw(self, surface, x, y, direction, is_attacking, attack_frame):
        if direction == 'front':
            angle = -45 + (attack_frame * 15)
            axe_x = x + 15
            axe_y = y - 5 - attack_frame * 2
            self._draw_axe_side(surface, axe_x, axe_y, angle, False)
        elif direction == 'back':
            angle = -45 + (attack_frame * 15)
            axe_x = x - 15
            axe_y = y - 5 - attack_frame * 2
            self._draw_axe_side(surface, axe_x, axe_y, angle, True)
        elif direction == 'right':
            angle = -90 - (attack_frame * 20)
            axe_x = x + 12
            axe_y = y - attack_frame * 3
            self._draw_axe_horizontal(surface, axe_x, axe_y, angle)
        elif direction == 'left':
            angle = 90 + (attack_frame * 20)
            axe_x = x - 12
            axe_y = y - attack_frame * 3
            self._draw_axe_horizontal(surface, axe_x, axe_y, angle)
            
    def _draw_axe_side(self, surface, x, y, angle, flip):
        handle_length = 35
        x_end = x + handle_length * math.cos(math.radians(angle))
        y_end = y + handle_length * math.sin(math.radians(angle))
        pygame.draw.line(surface, HANDLE_BROWN, (x, y), (x_end, y_end), 4)
        
        axe_x, axe_y = x_end, y_end
        points = [
            (axe_x - 3, axe_y - 8), (axe_x - 10, axe_y - 4), 
            (axe_x - 12, axe_y), (axe_x - 10, axe_y + 4), 
            (axe_x - 3, axe_y + 8), (axe_x + 2, axe_y + 4), 
            (axe_x + 2, axe_y - 4)
        ]
        
        rotated_points = []
        for px, py in points:
            px_temp, py_temp = px - axe_x, py - axe_y
            angle_rad = math.radians(angle)
            px_rot = px_temp * math.cos(angle_rad) - py_temp * math.sin(angle_rad)
            py_rot = px_temp * math.sin(angle_rad) + py_temp * math.cos(angle_rad)
            rotated_points.append((px_rot + axe_x, py_rot + axe_y))
        
        pygame.draw.polygon(surface, AXE_GRAY, rotated_points)
        pygame.draw.polygon(surface, DARK_METAL_GRAY, rotated_points, 2)
        
    def _draw_axe_horizontal(self, surface, x, y, angle):
        handle_length = 35
        x_end = x + handle_length * math.cos(math.radians(angle))
        y_end = y + handle_length * math.sin(math.radians(angle))
        pygame.draw.line(surface, HANDLE_BROWN, (x, y), (x_end, y_end), 4)
        
        axe_x, axe_y = x_end, y_end
        points = [
            (axe_x - 8, axe_y - 3), (axe_x - 4, axe_y - 10), 
            (axe_x, axe_y - 12), (axe_x + 4, axe_y - 10), 
            (axe_x + 8, axe_y - 3), (axe_x + 4, axe_y + 2), 
            (axe_x - 4, axe_y + 2)
        ]
        
        rotated_points = []
        for px, py in points:
            px_temp, py_temp = px - axe_x, py - axe_y
            angle_rad = math.radians(angle)
            px_rot = px_temp * math.cos(angle_rad) - py_temp * math.sin(angle_rad)
            py_rot = px_temp * math.sin(angle_rad) + py_temp * math.cos(angle_rad)
            rotated_points.append((px_rot + axe_x, py_rot + axe_y))
        
        pygame.draw.polygon(surface, AXE_GRAY, rotated_points)
        pygame.draw.polygon(surface, DARK_METAL_GRAY, rotated_points, 2)

# ============================================================================
# CLASE PLAYER (Jugador)
# ============================================================================
class Player:
    def __init__(self, x, y, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.x = x
        self.y = y
        self.z = 0
        self.speed = 3
        self.direction = 'front'
        self.is_walking = False
        self.is_attacking = False
        self.attack_duration = 10
        self.attack_frame = 0
        self.axe = Axe()
        self.animation_step = 0.0
        self.animation_speed = 4
        
        # Crear sprites simples procedurales
        self.image = self._create_sprite()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def _create_sprite(self):
        """Crea un sprite simple del personaje"""
        size = 60
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Cuerpo
        pygame.draw.ellipse(sprite, (100, 70, 50), (15, 35, 30, 20))
        # Cabeza
        pygame.draw.circle(sprite, (220, 180, 140), (30, 20), 12)
        # Ojos
        pygame.draw.circle(sprite, (50, 50, 80), (26, 18), 3)
        pygame.draw.circle(sprite, (50, 50, 80), (34, 18), 3)
        # Piernas
        pygame.draw.rect(sprite, (60, 40, 30), (22, 50, 6, 10))
        pygame.draw.rect(sprite, (60, 40, 30), (32, 50, 6, 10))
        
        return sprite
        
    def get_scale(self, floor_y_min, floor_y_max):
        min_scale = 0.8
        max_scale = 1.2
        y_range = floor_y_max - floor_y_min
        if y_range == 0:
            return min_scale
        y_normalized = (self.y - floor_y_min) / y_range
        y_normalized = max(0, min(1, y_normalized))
        return min_scale + y_normalized * (max_scale - min_scale)
    
    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
    
    def update(self, keys, floor_y_min, floor_y_max, wall_left_x, wall_right_x):
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame >= self.attack_duration:
                self.is_attacking = False
                self.attack_frame = 0
        
        self.is_walking = False
        move_speed_x = self.speed
        move_speed_y = self.speed * 0.5
        
        if not self.is_attacking:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= move_speed_x
                self.direction = 'left'
                self.is_walking = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += move_speed_x
                self.direction = 'right'
                self.is_walking = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y -= move_speed_y
                self.direction = 'back'
                self.is_walking = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y += move_speed_y
                self.direction = 'front'
                self.is_walking = True
        
        self.x = max(wall_left_x, min(self.x, wall_right_x))
        self.y = max(floor_y_min, min(self.y, floor_y_max))
        self.z = (self.y - floor_y_min) * 0.8
        
        if self.is_walking:
            self.animation_step += 1 / self.animation_speed
        
        current_scale = self.get_scale(floor_y_min, floor_y_max)
        base_sprite = self._create_sprite()
        scaled_width = int(base_sprite.get_width() * current_scale)
        scaled_height = int(base_sprite.get_height() * current_scale)
        self.image = pygame.transform.smoothscale(base_sprite, (scaled_width, scaled_height))
        
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.is_attacking:
            self.axe.draw(surface, self.x, self.rect.centery, self.direction, 
                         self.is_attacking, self.attack_frame)

# ============================================================================
# ELEMENTOS DEL BOSQUE
# ============================================================================
class Tree:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.height = random.randint(180, 280)
        self.width = random.randint(50, 90)
        self.sway_offset = random.uniform(0, math.pi * 2)
        
    def get_scale(self):
        return 0.5 + (self.z * 0.004)
        
    def get_screen_y(self):
        base_y = 350 + self.z * 0.4
        return base_y - self.height * self.get_scale()
        
    def draw(self, surface, time):
        scale = self.get_scale()
        screen_y = self.get_screen_y()
        scaled_h = int(self.height * scale)
        scaled_w = int(self.width * scale)
        alpha = max(100, min(255, int(255 - self.z * 0.5)))
        sway = math.sin(time * 0.5 + self.sway_offset) * 3 * scale
        
        # Sombra
        shadow_surf = pygame.Surface((scaled_w + 40, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), shadow_surf.get_rect())
        ground_y = 350 + self.z * 0.4
        surface.blit(shadow_surf, (int(self.x - scaled_w//2 - 20 + sway), int(ground_y)))
        
        # Tronco
        trunk_top_x = int(self.x + sway)
        trunk_bottom_x = int(self.x)
        trunk_y = int(screen_y + scaled_h)
        trunk_points = [
            (trunk_bottom_x - scaled_w//8, trunk_y),
            (trunk_bottom_x + scaled_w//8, trunk_y),
            (trunk_top_x + scaled_w//12, int(screen_y)),
            (trunk_top_x - scaled_w//12, int(screen_y))
        ]
        pygame.draw.polygon(surface, (40, 30, 20, alpha), trunk_points)
        
        # Copa
        for i in range(4):
            offset = i * 20 * scale
            radius = int((scaled_w//2 + 30) * (1.3 - i * 0.15))
            pygame.draw.circle(surface, (20, 60, 20, alpha // max(1, i)), 
                             (trunk_top_x, int(screen_y + offset)), radius)

class Rock:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        
    def get_scale(self):
        return 0.3 + (self.z * 0.003)
        
    def draw(self, surface):
        scale = self.get_scale()
        screen_y = 350 + self.z * 0.4
        size = int(15 * scale)
        pygame.draw.circle(surface, (60, 60, 65), (int(self.x), int(screen_y)), size)
        pygame.draw.circle(surface, (40, 40, 45), (int(self.x), int(screen_y)), int(size * 0.7))

class FogParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT - 200)
        self.z = random.randint(-50, 300)
        self.radius = random.randint(40, 120)
        self.speed = random.uniform(0.3, 1.0)
        
    def update(self):
        self.x -= self.speed
        if self.x < -self.radius:
            self.x = WIDTH + self.radius
            
    def draw(self, surface):
        scale = 0.5 + (self.z * 0.003)
        alpha = max(10, min(40, int(40 - self.z * 0.1)))
        radius = int(self.radius * scale)
        fog_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(fog_surf, (40, 40, 50, alpha), (radius, radius), radius)
        surface.blit(fog_surf, (int(self.x - radius), int(self.y - radius)))

# ============================================================================
# UI MANAGER
# ============================================================================
class UIManager:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 54)
        self.font_small = pygame.font.Font(None, 42)
        self.messages = []
        
    def draw_panel(self, surface, x, y, width, height, title=""):
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 150), (5, 5, width, height))
        pygame.draw.rect(panel, UI_DARK, (0, 0, width, height))
        pygame.draw.rect(panel, UI_BORDER, (0, 0, width, height), 3)
        
        if title:
            title_surf = self.font_medium.render(title, True, UI_HIGHLIGHT)
            panel.blit(title_surf, (15, 10))
            pygame.draw.line(panel, UI_BORDER, (10, 45), (width-10, 45), 2)
        
        surface.blit(panel, (x, y))
    
    def show_message(self, message, duration=3):
        self.messages.append({"text": message, "timer": duration, "alpha": 255})
    
    def update_messages(self, dt):
        for msg in self.messages[:]:
            msg["timer"] -= dt
            if msg["timer"] < 0.5:
                msg["alpha"] = int(255 * (msg["timer"] / 0.5))
            if msg["timer"] <= 0:
                self.messages.remove(msg)
    
    def draw_messages(self, surface):
        y_offset = HEIGHT // 2 - 100
        for msg in self.messages:
            text_surf = self.font_medium.render(msg["text"], True, UI_TEXT)
            text_surf.set_alpha(msg["alpha"])
            bg_surf = pygame.Surface((text_surf.get_width() + 40, text_surf.get_height() + 20), pygame.SRCALPHA)
            bg_surf.fill((*UI_DARK[:3], min(200, msg["alpha"])))
            x = WIDTH // 2 - text_surf.get_width() // 2
            surface.blit(bg_surf, (x - 20, y_offset - 10))
            surface.blit(text_surf, (x, y_offset))
            y_offset += 60

# ============================================================================
# ESCENA DE LA TABERNA
# ============================================================================
class TavernScene:
    def __init__(self, manager):
        self.manager = manager
        self.player = Player(WIDTH // 2, HEIGHT - 200, WIDTH, HEIGHT)
        self.ui = UIManager()
        
        # Límites
        self.floor_y_min = 480
        self.floor_y_max = HEIGHT - 10
        self.wall_left = 300
        self.wall_right = WIDTH - 50
        
        # Puerta
        self.door_rect = pygame.Rect(WIDTH // 2 - 100, 380, 200, 80)
        
        self.ui.show_message("¡Bienvenido a la Taberna!", 3)
        
    def update(self, dt, keys):
        self.player.update(keys, self.floor_y_min, self.floor_y_max, self.wall_left, self.wall_right)
        self.ui.update_messages(dt)
        
        # Detectar salida
        if self.player.rect.colliderect(self.door_rect):
            return "forest"
        return None
    
    def draw(self, surface):
        # Fondo
        surface.fill((40, 25, 15))
        
        # Suelo
        pygame.draw.rect(surface, (80, 50, 30), (0, self.floor_y_min, WIDTH, HEIGHT - self.floor_y_min))
        
        # Paredes
        pygame.draw.rect(surface, (60, 40, 25), (0, 0, self.wall_left, HEIGHT))
        pygame.draw.rect(surface, (60, 40, 25), (self.wall_right, 0, WIDTH - self.wall_right, HEIGHT))
        
        # Puerta
        pygame.draw.rect(surface, (100, 60, 40), self.door_rect)
        pygame.draw.rect(surface, (80, 50, 30), self.door_rect, 3)
        
        # Jugador
        self.player.draw(surface)
        
        # UI
        self.ui.draw_messages(surface)
        self.ui.draw_panel(surface, 20, HEIGHT - 80, 500, 60)
        controls = self.ui.font_small.render("WASD: Mover | ESPACIO: Atacar", True, UI_TEXT)
        surface.blit(controls, (30, HEIGHT - 70))

# ============================================================================
# ESCENA DEL BOSQUE
# ============================================================================
class ForestScene:
    def __init__(self, manager):
        self.manager = manager
        self.player = Player(WIDTH // 2, HEIGHT - 100, WIDTH, HEIGHT)
        self.ui = UIManager()
        
        self.floor_y_min = 350
        self.floor_y_max = HEIGHT - 50
        self.wall_left = 100
        self.wall_right = WIDTH - 100
        
        # Elementos del bosque
        self.trees = [Tree(random.randint(100, WIDTH-100), random.randint(-50, 300)) for _ in range(25)]
        self.rocks = [Rock(random.randint(100, WIDTH-100), random.randint(-50, 300)) for _ in range(30)]
        self.fog = [FogParticle() for _ in range(30)]
        
        self.game_time = 0
        self.show_title = True
        self.title_timer = 0
        
        self.ui.show_message("Bienvenido al Bosque del Caza Sombras", 4)
        
    def update(self, dt, keys):
        self.game_time += dt
        
        if self.show_title:
            self.title_timer += dt
            return None
            
        self.player.update(keys, self.floor_y_min, self.floor_y_max, self.wall_left, self.wall_right)
        self.ui.update_messages(dt)
        
        for f in self.fog:
            f.update()
        
        # ESC para volver
        if keys[pygame.K_ESCAPE]:
            return "tavern"
        return None
    
    def draw(self, surface):
        # Cielo
        for i in range(HEIGHT // 2):
            alpha = i / (HEIGHT // 2)
            color = (
                int(BLACK[0] + (DARK_GRAY[0] - BLACK[0]) * alpha),
                int(BLACK[1] + (DARK_GRAY[1] - BLACK[1]) * alpha),
                int(BLACK[2] + (DARK_GRAY[2] - BLACK[2]) * alpha)
            )
            pygame.draw.line(surface, color, (0, i), (WIDTH, i))
        
        # Luna
        pygame.draw.circle(surface, (220, 220, 240, 180), (WIDTH - 150, 100), 60)
        
        if not self.show_title:
            # Suelo
            for y_line in range(350, HEIGHT, 2):
                depth = (y_line - 350) * 0.8
                darkness = max(15, min(50, 50 - int(depth * 0.1)))
                pygame.draw.line(surface, (darkness, darkness + 5, darkness), (0, y_line), (WIDTH, y_line))
            
            # Ordenar objetos
            all_objects = []
            for tree in self.trees:
                all_objects.append(('tree', tree.z, tree))
            for rock in self.rocks:
                all_objects.append(('rock', rock.z, rock))
            for f in self.fog:
                all_objects.append(('fog', f.z, f))
            all_objects.append(('player', self.player.z, self.player))
            all_objects.sort(key=lambda obj: obj[1])
            
            # Dibujar
            for obj_type, z, obj in all_objects:
                if obj_type == 'tree':
                    obj.draw(surface, self.game_time)
                elif obj_type == 'rock':
                    obj.draw(surface)
                elif obj_type == 'fog':
                    obj.draw(surface)
                elif obj_type == 'player':
                    obj.draw(surface)
            
            # UI
            self.ui.draw_messages(surface)
            self.ui.draw_panel(surface, WIDTH//2 - 250, HEIGHT - 70, 500, 55)
            controls = self.ui.font_small.render("WASD: Mover | ESPACIO: Atacar | ESC: Volver", True, UI_TEXT)
            surface.blit(controls, (WIDTH//2 - 240, HEIGHT - 60))
        
        # Pantalla de título
        if self.show_title:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            title = self.ui.font_large.render("Cuentos de Mentes Estrelladas", True, UI_HIGHLIGHT)
            subtitle = self.ui.font_medium.render("El Bosque del Caza Sombras", True, UI_TEXT)
            prompt = self.ui.font_medium.render("Presiona cualquier tecla", True, UI_TEXT)
            
            alpha = min(255, int(self.title_timer * 200))
            prompt_alpha = int(max(0, alpha - 100) * (0.5 + 0.5 * math.sin(self.title_timer * 3)))
            
            title.set_alpha(alpha)
            subtitle.set_alpha(max(0, alpha - 50))
            prompt.set_alpha(prompt_alpha)
            
            surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
            surface.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2))
            surface.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 80))

# ============================================================================
# SCENE MANAGER Y MAIN
# ============================================================================
class SceneManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cuentos de Mentes Estrelladas - Demo 2.5D")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.scenes = {
            "tavern": TavernScene(self),
            "forest": ForestScene(self)
        }
        self.current_scene = self.scenes["tavern"]
        
    def change_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_scene.player.attack()
                    if hasattr(self.current_scene, 'show_title') and self.current_scene.show_title:
                        self.current_scene.show_title = False
            
            keys = pygame.key.get_pressed()
            result = self.current_scene.update(dt, keys)
            
            if result:
                self.change_scene(result)
            
            self.current_scene.draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SceneManager()
    game.run()