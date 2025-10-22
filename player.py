import pygame
import math

# Colores para el personaje detallado
GRIS_OSCURO = (60, 60, 65)
MARRON = (101, 67, 33)
MARRON_BOTA = (61, 43, 31)
MARRON_MANGO = (76, 47, 28)
PIEL = (255, 220, 177)
NEGRO = (30, 30, 30)
GRIS_HACHA = (128, 138, 145)
GRIS_METAL_OSCURO = (90, 95, 100)

class Hacha:
    def __init__(self):
        self.angulo_ataque = 0
        self.atacando = False
        self.frame_ataque = 0
        
    def dibujar(self, surface, x, y, direccion, atacando, frame_ataque, scale=1.0):
        """Dibuja el hacha en la mano del personaje con escala"""
        if direccion == 'frente':
            if atacando:
                angulo = -45 + (frame_ataque * 15)
                hacha_x = x + 15 * scale
                hacha_y = y - 5 * scale - frame_ataque * 2 * scale
            else:
                angulo = -45
                hacha_x = x + 15 * scale
                hacha_y = y
            self.dibujar_hacha_lado(surface, hacha_x, hacha_y, angulo, False, scale)
            
        elif direccion == 'atras':
            if atacando:
                angulo = -45 + (frame_ataque * 15)
                hacha_x = x - 15 * scale
                hacha_y = y - 5 * scale - frame_ataque * 2 * scale
            else:
                angulo = -45
                hacha_x = x - 15 * scale
                hacha_y = y
            self.dibujar_hacha_lado(surface, hacha_x, hacha_y, angulo, True, scale)
            
        elif direccion == 'derecha':
            if atacando:
                angulo = -90 - (frame_ataque * 20)
                hacha_x = x + 12 * scale
                hacha_y = y - frame_ataque * 3 * scale
            else:
                angulo = -90
                hacha_x = x + 12 * scale
                hacha_y = y
            self.dibujar_hacha_horizontal(surface, hacha_x, hacha_y, angulo, scale)
            
        elif direccion == 'izquierda':
            if atacando:
                angulo = 90 + (frame_ataque * 20)
                hacha_x = x - 12 * scale
                hacha_y = y - frame_ataque * 3 * scale
            else:
                angulo = 90
                hacha_x = x - 12 * scale
                hacha_y = y
            self.dibujar_hacha_horizontal(surface, hacha_x, hacha_y, angulo, scale)
    
    def dibujar_hacha_lado(self, surface, x, y, angulo, flip, scale):
        largo_mango = 35 * scale
        x_fin = x + largo_mango * math.cos(math.radians(angulo))
        y_fin = y + largo_mango * math.sin(math.radians(angulo))
        pygame.draw.line(surface, MARRON_MANGO, (x, y), (x_fin, y_fin), max(1, int(4 * scale)))
        
        x_hacha = x_fin
        y_hacha = y_fin
        
        puntos = [
            (x_hacha - 3 * scale, y_hacha - 8 * scale),
            (x_hacha - 10 * scale, y_hacha - 4 * scale),
            (x_hacha - 12 * scale, y_hacha),
            (x_hacha - 10 * scale, y_hacha + 4 * scale),
            (x_hacha - 3 * scale, y_hacha + 8 * scale),
            (x_hacha + 2 * scale, y_hacha + 4 * scale),
            (x_hacha + 2 * scale, y_hacha - 4 * scale)
        ]
        
        puntos_rotados = []
        for px, py in puntos:
            px_temp = px - x_hacha
            py_temp = py - y_hacha
            angulo_rad = math.radians(angulo)
            px_rot = px_temp * math.cos(angulo_rad) - py_temp * math.sin(angulo_rad)
            py_rot = px_temp * math.sin(angulo_rad) + py_temp * math.cos(angulo_rad)
            puntos_rotados.append((px_rot + x_hacha, py_rot + y_hacha))
        
        pygame.draw.polygon(surface, GRIS_HACHA, puntos_rotados)
        pygame.draw.polygon(surface, GRIS_METAL_OSCURO, puntos_rotados, max(1, int(2 * scale)))
    
    def dibujar_hacha_horizontal(self, surface, x, y, angulo, scale):
        largo_mango = 35 * scale
        x_fin = x + largo_mango * math.cos(math.radians(angulo))
        y_fin = y + largo_mango * math.sin(math.radians(angulo))
        pygame.draw.line(surface, MARRON_MANGO, (x, y), (x_fin, y_fin), max(1, int(4 * scale)))
        
        x_hacha = x_fin
        y_hacha = y_fin
        
        puntos = [
            (x_hacha - 8 * scale, y_hacha - 3 * scale),
            (x_hacha - 4 * scale, y_hacha - 10 * scale),
            (x_hacha, y_hacha - 12 * scale),
            (x_hacha + 4 * scale, y_hacha - 10 * scale),
            (x_hacha + 8 * scale, y_hacha - 3 * scale),
            (x_hacha + 4 * scale, y_hacha + 2 * scale),
            (x_hacha - 4 * scale, y_hacha + 2 * scale)
        ]
        
        puntos_rotados = []
        for px, py in puntos:
            px_temp = px - x_hacha
            py_temp = py - y_hacha
            angulo_rad = math.radians(angulo)
            px_rot = px_temp * math.cos(angulo_rad) - py_temp * math.sin(angulo_rad)
            py_rot = px_temp * math.sin(angulo_rad) + py_temp * math.cos(angulo_rad)
            puntos_rotados.append((px_rot + x_hacha, py_rot + y_hacha))
        
        pygame.draw.polygon(surface, GRIS_HACHA, puntos_rotados)
        pygame.draw.polygon(surface, GRIS_METAL_OSCURO, puntos_rotados, max(1, int(2 * scale)))

# Clase para el jugador (Jaime) con perspectiva 2.5D y diseño detallado
class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.z = 0
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_z = 0
        self.vel_y = 0
        self.jumping = False
        self.facing_right = True
        self.direccion = 'frente'
        self.animation_frame = 0
        self.animation_timer = 0
        self.health = 100
        self.stamina = 100
        self.hacha = Hacha()
        self.atacando = False
        self.frame_ataque = 0
        self.duracion_ataque = 10
        
    def update(self, keys, WIDTH, HEIGHT):
        # Actualizar ataque
        if self.atacando:
            self.frame_ataque += 1
            if self.frame_ataque >= self.duracion_ataque:
                self.atacando = False
                self.frame_ataque = 0
        
        # Movimiento (bloqueado durante ataque)
        if not self.atacando:
            self.vel_x = 0
            self.vel_z = 0
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vel_x = -4
                self.facing_right = False
                self.direccion = 'izquierda'
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vel_x = 4
                self.facing_right = True
                self.direccion = 'derecha'
                
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vel_z = -3
                self.direccion = 'atras'
                if self.stamina > 0:
                    self.stamina -= 0.3
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vel_z = 3
                self.direccion = 'frente'
                
            # Salto
            if keys[pygame.K_SPACE] and not self.jumping:
                self.vel_y = -15
                self.jumping = True
        
        # Gravedad
        self.vel_y += 0.8
        if self.vel_y > 12:
            self.vel_y = 12
            
        # Actualizar posición
        self.x += self.vel_x
        self.z += self.vel_z
        self.y += self.vel_y
        
        # Colisión con el suelo
        ground_y = 350 + self.z * 0.4
        if self.y >= ground_y:
            self.y = ground_y
            self.vel_y = 0
            self.jumping = False
            
        # Límites del mundo
        if self.x < 100:
            self.x = 100
        if self.x > WIDTH - 100:
            self.x = WIDTH - 100
        if self.z < -50:
            self.z = -50
        if self.z > 300:
            self.z = 300
            
        # Recuperación de stamina
        if self.stamina < 100:
            self.stamina += 0.2
            
        # Animación
        if self.vel_x != 0 or self.vel_z != 0:
            self.animation_timer += 1
            if self.animation_timer > 5:
                self.animation_frame = (self.animation_frame + 1) % 4
                self.animation_timer = 0
    
    def atacar(self):
        """Inicia el ataque con el hacha"""
        if not self.atacando:
            self.atacando = True
            self.frame_ataque = 0
                
    def get_scale(self):
        return 1.0 + (self.z * 0.003)
        
    def get_screen_y(self):
        return self.y - self.z * 0.3
    
    def dibujar_personaje(self, surface, x, y, scale):
        """Dibuja el personaje detallado según su dirección"""
        offset_pierna = math.sin(self.animation_frame * 0.5) * 3 * scale if (self.vel_x != 0 or self.vel_z != 0) else 0
        brazo_offset = math.sin(self.animation_frame * 0.5) * 2 * scale if (self.vel_x != 0 or self.vel_z != 0) else 0
        
        if self.direccion == 'frente':
            self.dibujar_frente(surface, x, y, scale, offset_pierna, brazo_offset)
        elif self.direccion == 'atras':
            self.dibujar_atras(surface, x, y, scale, offset_pierna, brazo_offset)
        elif self.direccion == 'izquierda':
            self.dibujar_lado(surface, x, y, scale, offset_pierna, brazo_offset, True)
        elif self.direccion == 'derecha':
            self.dibujar_lado(surface, x, y, scale, offset_pierna, brazo_offset, False)
    
    def dibujar_frente(self, surface, x, y, scale, offset_pierna, brazo_offset):
        # Piernas
        pygame.draw.rect(surface, MARRON, (x - 8*scale, y + 15*scale - offset_pierna, 7*scale, 18*scale))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 9*scale, y + 30*scale - offset_pierna, 9*scale, 8*scale))
        pygame.draw.rect(surface, MARRON, (x + 1*scale, y + 15*scale + offset_pierna, 7*scale, 18*scale))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x, y + 30*scale + offset_pierna, 9*scale, 8*scale))
        
        # Torso
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 12*scale, y - 5*scale, 24*scale, 22*scale))
        
        # Brazo izquierdo
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 15*scale, y - 3*scale - brazo_offset, 6*scale, 16*scale))
        pygame.draw.ellipse(surface, PIEL, (x - 16*scale, y + 11*scale - brazo_offset, 7*scale, 7*scale))
        
        # Brazo derecho
        pygame.draw.rect(surface, GRIS_OSCURO, (x + 9*scale, y - 3*scale, 6*scale, 16*scale))
        pygame.draw.ellipse(surface, PIEL, (x + 9*scale, y + 11*scale, 7*scale, 7*scale))
        
        # Hacha
        self.hacha.dibujar(surface, x, y, self.direccion, self.atacando, self.frame_ataque, scale)
        
        # Cuello
        pygame.draw.rect(surface, PIEL, (x - 3*scale, y - 8*scale, 6*scale, 5*scale))
        
        # Cabeza
        pygame.draw.ellipse(surface, PIEL, (x - 8*scale, y - 20*scale, 16*scale, 18*scale))
        pygame.draw.ellipse(surface, NEGRO, (x - 9*scale, y - 22*scale, 18*scale, 12*scale))
        for i in range(4):
            pygame.draw.circle(surface, NEGRO, (int(x - 7*scale + i * 5*scale), int(y - 18*scale)), max(1, int(3*scale)))
        
        # Cara
        pygame.draw.ellipse(surface, NEGRO, (x - 4*scale, y - 13*scale, 2*scale, 3*scale))
        pygame.draw.ellipse(surface, NEGRO, (x + 2*scale, y - 13*scale, 2*scale, 3*scale))
    
    def dibujar_atras(self, surface, x, y, scale, offset_pierna, brazo_offset):
        # Piernas
        pygame.draw.rect(surface, MARRON, (x - 8*scale, y + 15*scale, 7*scale, 18*scale))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 9*scale, y + 30*scale, 9*scale, 8*scale))
        pygame.draw.rect(surface, MARRON, (x + 1*scale, y + 15*scale - offset_pierna, 7*scale, 18*scale))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x, y + 30*scale - offset_pierna, 9*scale, 8*scale))
        
        # Torso
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 12*scale, y - 5*scale, 24*scale, 22*scale))
        
        # Brazo izquierdo
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 15*scale, y - 3*scale + brazo_offset, 6*scale, 16*scale))
        pygame.draw.ellipse(surface, PIEL, (x - 16*scale, y + 11*scale + brazo_offset, 7*scale, 7*scale))
        
        # Hacha
        self.hacha.dibujar(surface, x, y, self.direccion, self.atacando, self.frame_ataque, scale)
        
        # Brazo derecho
        pygame.draw.rect(surface, GRIS_OSCURO, (x + 9*scale, y - 3*scale, 6*scale, 16*scale))
        pygame.draw.ellipse(surface, PIEL, (x + 9*scale, y + 11*scale, 7*scale, 7*scale))
        
        # Cuello
        pygame.draw.rect(surface, PIEL, (x - 3*scale, y - 8*scale, 6*scale, 5*scale))
        
        # Cabeza
        pygame.draw.ellipse(surface, PIEL, (x - 8*scale, y - 20*scale, 16*scale, 18*scale))
        pygame.draw.ellipse(surface, NEGRO, (x - 9*scale, y - 22*scale, 18*scale, 12*scale))
        for i in range(4):
            pygame.draw.circle(surface, NEGRO, (int(x - 7*scale + i * 5*scale), int(y - 18*scale)), max(1, int(3*scale)))
    
    def dibujar_lado(self, surface, x, y, scale, offset_pierna, brazo_offset, flip):
        m = -1 if flip else 1
        
        # Pierna trasera
        pygame.draw.rect(surface, MARRON, (x - 3*scale*m, y + 15*scale - offset_pierna, 7*scale, 18*scale))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 3*scale*m, y + 30*scale - offset_pierna, 9*scale, 8*scale))
        
        # Torso
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 8*scale*m, y - 5*scale, 16*scale, 22*scale))
        
        # Brazo trasero
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 2*scale*m, y - 2*scale - brazo_offset, 6*scale, 16*scale))
        pygame.draw.ellipse(surface, PIEL, (x - 2*scale*m, y + 12*scale - brazo_offset, 6*scale, 6*scale))
        
        # Pierna delantera
        pygame.draw.rect(surface, MARRON, (x - 3*scale*m, y + 15*scale + offset_pierna, 7*scale, 18*scale))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 3*scale*m, y + 30*scale + offset_pierna, 9*scale, 8*scale))
        
        # Brazo delantero
        pygame.draw.rect(surface, GRIS_OSCURO, (x + 5*scale*m, y - 2*scale, 6*scale, 16*scale))
        pygame.draw.ellipse(surface, PIEL, (x + 5*scale*m, y + 12*scale, 6*scale, 6*scale))
        
        # Hacha
        self.hacha.dibujar(surface, x, y, self.direccion, self.atacando, self.frame_ataque, scale)
        
        # Cuello
        pygame.draw.rect(surface, PIEL, (x - 2*scale*m, y - 8*scale, 6*scale, 5*scale))
        
        # Cabeza
        pygame.draw.ellipse(surface, PIEL, (x - 8*scale*m, y - 20*scale, 16*scale, 18*scale))
        pygame.draw.ellipse(surface, NEGRO, (x - 9*scale*m, y - 22*scale, 18*scale, 12*scale))
        for i in range(3):
            pygame.draw.circle(surface, NEGRO, (int(x - 6*scale*m + i * 4*scale*m), int(y - 17*scale)), max(1, int(3*scale)))
        
        # Cara perfil
        pygame.draw.ellipse(surface, NEGRO, (x + 2*scale*m, y - 13*scale, 2*scale, 3*scale))
        
    def draw(self, surface):
        scale = self.get_scale()
        screen_y = self.get_screen_y()
        
        # Sombra
        shadow_size = int((40 + 20) * (1 + self.z * 0.002) * scale)
        shadow_surf = pygame.Surface((shadow_size, 15), pygame.SRCALPHA)
        alpha = max(30, 100 - int(self.z * 0.3))
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, alpha), shadow_surf.get_rect())
        ground_y = 350 + self.z * 0.4
        surface.blit(shadow_surf, (int(self.x - shadow_size//2), int(ground_y + 30*scale)))
        
        # Dibujar personaje detallado
        self.dibujar_personaje(surface, self.x, screen_y, scale)


# Funciones de UI relacionadas con el jugador
class PlayerUI:
    def __init__(self, font_small, font_medium):
        self.font_small = font_small
        self.font_medium = font_medium
        
    def draw_health_bar(self, surface, x, y, current, maximum, label=""):
        width = 220
        height = 35
        
        UI_BORDER = (80, 70, 90)
        UI_TEXT = (200, 190, 180)
        
        pygame.draw.rect(surface, (40, 30, 35), (x, y, width, height))
        pygame.draw.rect(surface, UI_BORDER, (x, y, width, height), 3)
        
        fill_width = int((current / maximum) * (width - 6))
        if current > 60:
            color = (80, 150, 80)
        elif current > 30:
            color = (180, 150, 60)
        else:
            color = (180, 60, 60)
        
        pygame.draw.rect(surface, color, (x + 3, y + 3, fill_width, height - 6))
        pygame.draw.rect(surface, tuple(min(255, c + 40) for c in color), 
                        (x + 3, y + 3, fill_width, height // 2 - 1))
        
        if label:
            text = self.font_small.render(f"{label}: {int(current)}/{maximum}", True, UI_TEXT)
            surface.blit(text, (x + width + 10, y + 5))
    
    def draw_minimap(self, surface, player, trees, WIDTH, HEIGHT, draw_panel_func):
        x, y = WIDTH - 330, 30
        size = 300
        
        draw_panel_func(surface, x, y, size, size, "Mapa")
        
        map_area = pygame.Surface((size - 30, size - 90), pygame.SRCALPHA)
        map_area.fill((15, 20, 25, 200))
        
        scale_x = (size - 30) / WIDTH
        scale_z = (size - 90) / 400
        
        for tree in trees:
            tree_x = int(tree.x * scale_x)
            tree_z = int((tree.z + 50) * scale_z)
            pygame.draw.circle(map_area, (40, 60, 40), (tree_x, tree_z), 4)
        
        player_x = int(player.x * scale_x)
        player_z = int((player.z + 50) * scale_z)
        pygame.draw.circle(map_area, (200, 80, 80), (player_x, player_z), 7)
        pygame.draw.circle(map_area, (255, 120, 120), (player_x, player_z), 4)
        
        surface.blit(map_area, (x + 15, y + 75))