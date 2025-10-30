# forest_scene.py
import pygame
import random
import math
import os
from player import TavernPlayer

# -------------------------------------------------------------
# --- CONFIGURACIÓN Y ESCALA ---

# Configuración de pantalla de alta resolución
WIDTH, HEIGHT = 1280, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Cuentos de Mentes Estrelladas - Demo 2.5D")
clock = pygame.time.Clock()

# FACTOR DE ESCALA: Ajusta este valor para cambiar el tamaño del personaje.
SCALE_FACTOR = 0.10 

# Habilitar anti-aliasing y suavizado
pygame.font.init()
# ELIMINADO: pygame.mixer.init()

# *** INICIALIZAR SISTEMA DE SONIDO ***
# ELIMINADO: sound_manager = SoundManager()
# ELIMINADO: init_game_sounds(sound_manager)
# ELIMINADO: sound_manager.play_sound("impacto", loops=-1)
# ELIMINADO: sound_manager.set_sfx_volume(0.3)

# Colores del código base
BLACK = (10, 10, 15)
DARK_GRAY = (30, 30, 40)
UI_DARK = (20, 15, 25, 200)
UI_BORDER = (80, 70, 90)
UI_TEXT = (200, 190, 180)
UI_HIGHLIGHT = (150, 120, 100)
class Forest:
#  Clase Bosque
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
        base_color = (15, 20, 15)
        shadow_surf = pygame.Surface((scaled_w + 40, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), shadow_surf.get_rect())
        ground_y = 350 + self.z * 0.4
        surface.blit(shadow_surf, (int(self.x - scaled_w//2 - 20 + sway), int(ground_y)))
        trunk_top_x = int(self.x + sway)
        trunk_bottom_x = int(self.x)
        trunk_y = int(screen_y + scaled_h)
        trunk_points = [
            (trunk_bottom_x - scaled_w//8, trunk_y),
            (trunk_bottom_x + scaled_w//8, trunk_y),
            (trunk_top_x + scaled_w//12, int(screen_y)),
            (trunk_top_x - scaled_w//12, int(screen_y))
        ]
        pygame.draw.polygon(surface, (*base_color, alpha), trunk_points)
        for i in range(4):
            offset = i * 20 * scale
            radius = int((scaled_w//2 + 30) * (1.3 - i * 0.15))
            color_mod = i * 5
            pygame.draw.circle(surface, (*base_color, alpha // max(1, i)), 
                             (trunk_top_x, int(screen_y + offset)), radius)

class GroundElement:
# ... (Clase GroundElement sin cambios)
    def __init__(self, x, z, type):
        self.x = x
        self.z = z
        self.type = type
        
    def get_scale(self):
        return 0.3 + (self.z * 0.003)
        
    def draw(self, surface):
        scale = self.get_scale()
        screen_y = 350 + self.z * 0.4
        
        if self.type == 'rock':
            size = int(15 * scale)
            pygame.draw.circle(surface, (40, 40, 45), (int(self.x), int(screen_y)), size)
            pygame.draw.circle(surface, (30, 30, 35), (int(self.x), int(screen_y)), int(size * 0.7))
        elif self.type == 'grass':
            for i in range(3):
                offset = (i - 1) * 5 * scale
                pygame.draw.line(surface, (30, 40, 30), 
                               (int(self.x + offset), int(screen_y)), 
                               (int(self.x + offset), int(screen_y - 15 * scale)), 2)

class UIManager:
# ... (Clase UIManager sin cambios)
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 54)
        self.font_small = pygame.font.Font(None, 42)
        self.messages = []
        self.message_timer = 0
        
    def draw_panel(self, surface, x, y, width, height, title=""):
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 150), (5, 5, width, height))
        pygame.draw.rect(panel, UI_DARK, (0, 0, width, height))
        pygame.draw.rect(panel, UI_BORDER, (0, 0, width, height), 3)
        pygame.draw.line(panel, (100, 90, 110), (3, 3), (width-3, 3), 2)
        pygame.draw.line(panel, (100, 90, 110), (3, 3), (3, height-3), 2)
        pygame.draw.line(panel, (40, 35, 45), (width-3, 3), (width-3, height-3), 2)
        pygame.draw.line(panel, (40, 35, 45), (3, height-3), (width-3, height-3), 2)
        
        if title:
            title_surf = self.font_medium.render(title, True, UI_HIGHLIGHT)
            panel.blit(title_surf, (15, 10))
            pygame.draw.line(panel, UI_BORDER, (10, 45), (width-10, 45), 2)
        
        surface.blit(panel, (x, y))
        return (x, y, width, height)
    
    def draw_objective(self, surface):
        x, y = 30, HEIGHT - 140
        width, height = 350, 120
        self.draw_panel(surface, x, y, width, height, "Objetivo")
        text1 = self.font_small.render("Adentrarse en el bosque", True, UI_TEXT)
        text2 = self.font_small.render("Encontrar al Caza Sombras", True, UI_HIGHLIGHT)
        text3 = self.font_small.render("Distancia: ???m", True, (150, 150, 160))
        surface.blit(text1, (x + 15, y + 55))
        surface.blit(text2, (x + 15, y + 85))
        surface.blit(text3, (x + 15, y + 115))
    
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
            y_offset += 60

class FogParticle3D:
# ... (Clase FogParticle3D sin cambios)
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

# -------------------------------------------------------------
# --- INICIALIZACIÓN DE OBJETOS ---

# ELIMINADO: player_sound = PlayerSoundController(sound_manager)
trees_3d = [Forest(random.randint(100, WIDTH-100), random.randint(-50, 300)) for _ in range(25)]
ground_elements = [GroundElement(random.randint(100, WIDTH-100), random.randint(-50, 300), 
                                 random.choice(['rock', 'grass', 'rock'])) for _ in range(40)]
ui_manager = UIManager()

title_font = pygame.font.Font(None, 108)
subtitle_font = pygame.font.Font(None, 63)

# Variables
show_title = True
title_timer = 0
game_time = 0
objective_timer = 0
show_objective = False
fog_particles = [FogParticle3D() for _ in range(30)]

ui_manager.show_message("Bienvenido al Bosque del Caza Sombras", 4)

# -------------------------------------------------------------
# --- BUCLE PRINCIPAL ---

running = True
while running:
    dt = clock.tick(60) / 1000
    game_time += dt
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if show_title:
                show_title = False
                show_objective = True
                objective_timer = 0
                ui_manager.show_message("Usa WASD o Flechas para moverte", 3)
            # ELIMINADOS: Controles de volumen y mute (K_PLUS, K_MINUS, K_m)
            elif event.key == pygame.K_SPACE and not show_title:
                TavernPlayer.attack()
            
    keys = pygame.key.get_pressed()
    
    # Actualizar
    if not show_title:
        TavernPlayer.update(keys, WIDTH, HEIGHT) 
        # ELIMINADO: player_sound.update(player, dt)
        ui_manager.update_messages(dt)
        
        if show_objective:
            objective_timer += dt
            if objective_timer >= 20:
                show_objective = False
        
        for fog in fog_particles:
            fog.update()
    
    # Dibujar
    screen.fill(BLACK)
    
    # Cielo con gradiente
    for i in range(HEIGHT // 2):
        alpha = i / (HEIGHT // 2)
        color = (
            int(BLACK[0] + (DARK_GRAY[0] - BLACK[0]) * alpha),
            int(BLACK[1] + (DARK_GRAY[1] - BLACK[1]) * alpha),
            int(BLACK[2] + (DARK_GRAY[2] - BLACK[2]) * alpha)
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))
    
    # Luna
    moon_surf = pygame.Surface((150, 150), pygame.SRCALPHA)
    pygame.draw.circle(moon_surf, (220, 220, 240, 180), (75, 75), 60)
    pygame.draw.circle(moon_surf, (220, 220, 240, 100), (75, 75), 70)
    screen.blit(moon_surf, (WIDTH - 200, 50))
    
    if not show_title:
        # Suelo base
        for y_line in range(350, HEIGHT, 2):
            depth = (y_line - 350) * 0.8
            darkness = max(15, min(50, 50 - int(depth * 0.1)))
            pygame.draw.line(screen, (darkness, min(255, darkness + 5), darkness), (0, y_line), (WIDTH, y_line))
        
        # Ordenar elementos por profundidad Z
        all_objects = []
        for tree in trees_3d:
            all_objects.append(('tree', tree.z, tree))
        for elem in ground_elements:
            all_objects.append(('ground', elem.z, elem))
        all_objects.append(('TavernPlayer', TavernPlayer.z, TavernPlayer))
        for fog in fog_particles:
            all_objects.append(('fog', fog.z, fog))
        
        all_objects.sort(key=lambda obj: obj[1])
        
        # Dibujar en orden de profundidad
        for obj_type, z, obj in all_objects:
            if obj_type == 'tree':
                obj.draw(screen, game_time)
            elif obj_type == 'ground':
                obj.draw(screen)
            elif obj_type == 'player':
                obj.draw(screen)
            elif obj_type == 'fog':
                obj.draw(screen)
        
        if show_objective:
            ui_manager.draw_objective(screen)
        
        ui_manager.draw_messages(screen)
        
        # Controles en pantalla actualizados
        controls_panel = ui_manager.draw_panel(screen, WIDTH//2 - 300, HEIGHT - 70, 600, 55)
        controls_text = ui_manager.font_small.render("WASD/Flechas: Mover | Espacio: ATACAR", True, UI_TEXT)
        screen.blit(controls_text, (controls_panel[0] + 20, controls_panel[1] + 15))
    
    # Pantalla de título
    if show_title:
        title_timer += dt
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        panel_w, panel_h = 700, 350
        ui_manager.draw_panel(screen, WIDTH//2 - panel_w//2, HEIGHT//2 - panel_h//2, panel_w, panel_h)
        
        title = title_font.render("Cuentos de Mentes Estrelladas", True, UI_HIGHLIGHT)
        subtitle = subtitle_font.render("El Bosque del Caza Sombras", True, UI_TEXT)
        subtitle2 = ui_manager.font_medium.render("Una aventura de suspenso y terror", True, (130, 130, 140))
        prompt = ui_manager.font_medium.render("Presiona cualquier tecla para comenzar", True, UI_TEXT)
        
        title_alpha = min(255, int(title_timer * 200))
        title.set_alpha(title_alpha)
        subtitle.set_alpha(max(0, title_alpha - 50))
        subtitle2.set_alpha(max(0, title_alpha - 80))
        prompt_alpha = int(max(0, title_alpha - 100) * (0.5 + 0.5 * math.sin(title_timer * 3)))
        prompt.set_alpha(prompt_alpha)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 40))
        screen.blit(subtitle2, (WIDTH//2 - subtitle2.get_width()//2, HEIGHT//2 + 10))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 100))
    
    pygame.display.flip()

# ELIMINADO: Detener sonido antes de salir
pygame.quit()