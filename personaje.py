import pygame
import math

pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Personaje 2.5D con Hacha - Pygame")

# Colores
VERDE_PASTO = (34, 139, 34)
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
        
    def dibujar(self, surface, x, y, direccion, atacando=False, frame_ataque=0):
        """Dibuja el hacha en la mano del personaje"""
        
        # Calcular posición y ángulo del hacha según dirección
        if direccion == 'frente':
            if atacando:
                # Animación de ataque
                angulo = -45 + (frame_ataque * 15)
                hacha_x = x + 15
                hacha_y = y - 5 - frame_ataque * 2
            else:
                angulo = -45
                hacha_x = x + 15
                hacha_y = y
            self.dibujar_hacha_lado(surface, hacha_x, hacha_y, angulo, False)
            
        elif direccion == 'atras':
            if atacando:
                angulo = -45 + (frame_ataque * 15)
                hacha_x = x - 15
                hacha_y = y - 5 - frame_ataque * 2
            else:
                angulo = -45
                hacha_x = x - 15
                hacha_y = y
            self.dibujar_hacha_lado(surface, hacha_x, hacha_y, angulo, True)
            
        elif direccion == 'derecha':
            if atacando:
                angulo = -90 - (frame_ataque * 20)
                hacha_x = x + 12
                hacha_y = y - frame_ataque * 3
            else:
                angulo = -90
                hacha_x = x + 12
                hacha_y = y
            self.dibujar_hacha_horizontal(surface, hacha_x, hacha_y, angulo)
            
        elif direccion == 'izquierda':
            if atacando:
                angulo = 90 + (frame_ataque * 20)
                hacha_x = x - 12
                hacha_y = y - frame_ataque * 3
            else:
                angulo = 90
                hacha_x = x - 12
                hacha_y = y
            self.dibujar_hacha_horizontal(surface, hacha_x, hacha_y, angulo)
    
    def dibujar_hacha_lado(self, surface, x, y, angulo, flip):
        """Dibuja el hacha de lado"""
        # Mango
        largo_mango = 35
        x_fin = x + largo_mango * math.cos(math.radians(angulo))
        y_fin = y + largo_mango * math.sin(math.radians(angulo))
        pygame.draw.line(surface, MARRON_MANGO, (x, y), (x_fin, y_fin), 4)
        
        # Cabeza del hacha
        x_hacha = x_fin
        y_hacha = y_fin
        
        # Metal del hacha (forma de hacha)
        puntos = [
            (x_hacha - 3, y_hacha - 8),
            (x_hacha - 10, y_hacha - 4),
            (x_hacha - 12, y_hacha),
            (x_hacha - 10, y_hacha + 4),
            (x_hacha - 3, y_hacha + 8),
            (x_hacha + 2, y_hacha + 4),
            (x_hacha + 2, y_hacha - 4)
        ]
        
        # Rotar puntos según el ángulo
        puntos_rotados = []
        for px, py in puntos:
            # Trasladar al origen
            px_temp = px - x_hacha
            py_temp = py - y_hacha
            # Rotar
            angulo_rad = math.radians(angulo)
            px_rot = px_temp * math.cos(angulo_rad) - py_temp * math.sin(angulo_rad)
            py_rot = px_temp * math.sin(angulo_rad) + py_temp * math.cos(angulo_rad)
            # Trasladar de vuelta
            puntos_rotados.append((px_rot + x_hacha, py_rot + y_hacha))
        
        pygame.draw.polygon(surface, GRIS_HACHA, puntos_rotados)
        pygame.draw.polygon(surface, GRIS_METAL_OSCURO, puntos_rotados, 2)
    
    def dibujar_hacha_horizontal(self, surface, x, y, angulo):
        """Dibuja el hacha horizontal (vistas laterales)"""
        # Mango
        largo_mango = 35
        x_fin = x + largo_mango * math.cos(math.radians(angulo))
        y_fin = y + largo_mango * math.sin(math.radians(angulo))
        pygame.draw.line(surface, MARRON_MANGO, (x, y), (x_fin, y_fin), 4)
        
        # Cabeza del hacha
        x_hacha = x_fin
        y_hacha = y_fin
        
        puntos = [
            (x_hacha - 8, y_hacha - 3),
            (x_hacha - 4, y_hacha - 10),
            (x_hacha, y_hacha - 12),
            (x_hacha + 4, y_hacha - 10),
            (x_hacha + 8, y_hacha - 3),
            (x_hacha + 4, y_hacha + 2),
            (x_hacha - 4, y_hacha + 2)
        ]
        
        # Rotar puntos
        puntos_rotados = []
        for px, py in puntos:
            px_temp = px - x_hacha
            py_temp = py - y_hacha
            angulo_rad = math.radians(angulo)
            px_rot = px_temp * math.cos(angulo_rad) - py_temp * math.sin(angulo_rad)
            py_rot = px_temp * math.sin(angulo_rad) + py_temp * math.cos(angulo_rad)
            puntos_rotados.append((px_rot + x_hacha, py_rot + y_hacha))
        
        pygame.draw.polygon(surface, GRIS_HACHA, puntos_rotados)
        pygame.draw.polygon(surface, GRIS_METAL_OSCURO, puntos_rotados, 2)

class Personaje:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 3
        self.direccion = 'frente'
        self.frame_animacion = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 8
        self.caminando = False
        self.hacha = Hacha()
        self.atacando = False
        self.frame_ataque = 0
        self.duracion_ataque = 10
        
    def dibujar_atras(self, surface, offset_x=0):
        """Dibuja el personaje visto desde atrás"""
        x = self.x + offset_x
        y = self.y
        
        # Piernas
        if self.caminando:
            offset_pierna = math.sin(self.frame_animacion * 0.5) * 3
        else:
            offset_pierna = 0
            
        pygame.draw.rect(surface, MARRON, (x - 8, y + 15, 7, 18))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 9, y + 30, 9, 8))
        
        pygame.draw.rect(surface, MARRON, (x + 1, y + 15 - offset_pierna, 7, 18))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x, y + 30 - offset_pierna, 9, 8))
        
        # Torso
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 12, y - 5, 24, 22))
        
        # Brazo izquierdo (sin hacha)
        brazo_offset = math.sin(self.frame_animacion * 0.5) * 2 if self.caminando else 0
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 15, y - 3 + brazo_offset, 6, 16))
        pygame.draw.ellipse(surface, PIEL, (x - 16, y + 11 + brazo_offset, 7, 7))
        
        # Hacha (detrás del personaje)
        self.hacha.dibujar(surface, self.x, self.y, self.direccion, self.atacando, self.frame_ataque)
        
        # Brazo derecho (con hacha)
        pygame.draw.rect(surface, GRIS_OSCURO, (x + 9, y - 3, 6, 16))
        pygame.draw.ellipse(surface, PIEL, (x + 9, y + 11, 7, 7))
        
        # Cuello
        pygame.draw.rect(surface, PIEL, (x - 3, y - 8, 6, 5))
        
        # Cabeza
        pygame.draw.ellipse(surface, PIEL, (x - 8, y - 20, 16, 18))
        pygame.draw.ellipse(surface, NEGRO, (x - 9, y - 22, 18, 12))
        for i in range(4):
            pygame.draw.circle(surface, NEGRO, (x - 7 + i * 5, y - 18), 3)
    
    def dibujar_frente(self, surface, offset_x=0):
        """Dibuja el personaje visto de frente"""
        x = self.x + offset_x
        y = self.y
        
        # Piernas
        if self.caminando:
            offset_pierna = math.sin(self.frame_animacion * 0.5) * 3
        else:
            offset_pierna = 0
            
        pygame.draw.rect(surface, MARRON, (x - 8, y + 15 - offset_pierna, 7, 18))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 9, y + 30 - offset_pierna, 9, 8))
        
        pygame.draw.rect(surface, MARRON, (x + 1, y + 15 + offset_pierna, 7, 18))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x, y + 30 + offset_pierna, 9, 8))
        
        # Torso
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 12, y - 5, 24, 22))
        
        # Brazo izquierdo
        brazo_offset = math.sin(self.frame_animacion * 0.5) * 2 if self.caminando else 0
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 15, y - 3 - brazo_offset, 6, 16))
        pygame.draw.ellipse(surface, PIEL, (x - 16, y + 11 - brazo_offset, 7, 7))
        
        # Brazo derecho (con hacha)
        pygame.draw.rect(surface, GRIS_OSCURO, (x + 9, y - 3, 6, 16))
        pygame.draw.ellipse(surface, PIEL, (x + 9, y + 11, 7, 7))
        
        # Hacha
        self.hacha.dibujar(surface, self.x, self.y, self.direccion, self.atacando, self.frame_ataque)
        
        # Cuello
        pygame.draw.rect(surface, PIEL, (x - 3, y - 8, 6, 5))
        
        # Cabeza
        pygame.draw.ellipse(surface, PIEL, (x - 8, y - 20, 16, 18))
        pygame.draw.ellipse(surface, NEGRO, (x - 9, y - 22, 18, 12))
        for i in range(4):
            pygame.draw.circle(surface, NEGRO, (x - 7 + i * 5, y - 18), 3)
        
        # Cara
        pygame.draw.ellipse(surface, NEGRO, (x - 4, y - 13, 2, 3))
        pygame.draw.ellipse(surface, NEGRO, (x + 2, y - 13, 2, 3))
        pygame.draw.arc(surface, NEGRO, (x - 3, y - 8, 6, 4), 3.14, 6.28, 1)
    
    def dibujar_lado(self, surface, flip=False):
        """Dibuja el personaje de lado"""
        x = self.x
        y = self.y
        
        multiplicador = -1 if flip else 1
        
        # Piernas
        if self.caminando:
            offset_pierna = math.sin(self.frame_animacion * 0.5) * 4
        else:
            offset_pierna = 0
        
        pygame.draw.rect(surface, MARRON, (x - 3 * multiplicador, y + 15 - offset_pierna, 7, 18))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 3 * multiplicador, y + 30 - offset_pierna, 9, 8))
        
        # Torso
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 8 * multiplicador, y - 5, 16, 22))
        
        # Brazo trasero
        brazo_offset = math.sin(self.frame_animacion * 0.5) * 3 if self.caminando else 0
        pygame.draw.rect(surface, GRIS_OSCURO, (x - 2 * multiplicador, y - 2 - brazo_offset, 6, 16))
        pygame.draw.ellipse(surface, PIEL, (x - 2 * multiplicador, y + 12 - brazo_offset, 6, 6))
        
        # Pierna delantera
        pygame.draw.rect(surface, MARRON, (x - 3 * multiplicador, y + 15 + offset_pierna, 7, 18))
        pygame.draw.ellipse(surface, MARRON_BOTA, (x - 3 * multiplicador, y + 30 + offset_pierna, 9, 8))
        
        # Brazo delantero (con hacha)
        pygame.draw.rect(surface, GRIS_OSCURO, (x + 5 * multiplicador, y - 2, 6, 16))
        pygame.draw.ellipse(surface, PIEL, (x + 5 * multiplicador, y + 12, 6, 6))
        
        # Hacha
        self.hacha.dibujar(surface, self.x, self.y, self.direccion, self.atacando, self.frame_ataque)
        
        # Cuello
        pygame.draw.rect(surface, PIEL, (x - 2 * multiplicador, y - 8, 6, 5))
        
        # Cabeza
        pygame.draw.ellipse(surface, PIEL, (x - 8 * multiplicador, y - 20, 16, 18))
        pygame.draw.ellipse(surface, NEGRO, (x - 9 * multiplicador, y - 22, 18, 12))
        for i in range(3):
            pygame.draw.circle(surface, NEGRO, (x - 6 * multiplicador + i * 4 * multiplicador, y - 17), 3)
        
        # Cara de perfil
        pygame.draw.ellipse(surface, NEGRO, (x + 2 * multiplicador, y - 13, 2, 3))
        pygame.draw.arc(surface, NEGRO, (x + 3 * multiplicador, y - 8, 4, 3), 0, 3.14, 1)
    
    def dibujar(self, surface):
        """Dibuja el personaje según su dirección"""
        if self.direccion == 'frente':
            self.dibujar_frente(surface)
        elif self.direccion == 'atras':
            self.dibujar_atras(surface)
        elif self.direccion == 'izquierda':
            self.dibujar_lado(surface, flip=True)
        elif self.direccion == 'derecha':
            self.dibujar_lado(surface, flip=False)
    
    def atacar(self):
        """Inicia el ataque con el hacha"""
        if not self.atacando:
            self.atacando = True
            self.frame_ataque = 0
    
    def actualizar(self, teclas):
        """Actualiza la posición y animación del personaje"""
        # Actualizar ataque
        if self.atacando:
            self.frame_ataque += 1
            if self.frame_ataque >= self.duracion_ataque:
                self.atacando = False
                self.frame_ataque = 0
        
        self.caminando = False
        
        # No permitir movimiento durante ataque
        if not self.atacando:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.x -= self.velocidad
                self.direccion = 'izquierda'
                self.caminando = True
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.x += self.velocidad
                self.direccion = 'derecha'
                self.caminando = True
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                self.y -= self.velocidad
                self.direccion = 'atras'
                self.caminando = True
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                self.y += self.velocidad
                self.direccion = 'frente'
                self.caminando = True
        
        # Mantener dentro de la pantalla
        self.x = max(30, min(self.x, ANCHO - 30))
        self.y = max(30, min(self.y, ALTO - 40))
        
        # Actualizar animación
        if self.caminando:
            self.contador_animacion += 1
            if self.contador_animacion >= self.velocidad_animacion:
                self.contador_animacion = 0
                self.frame_animacion += 0.5

# Crear personaje
personaje = Personaje(ANCHO // 2, ALTO // 2)

# Fuente para instrucciones
fuente = pygame.font.Font(None, 24)

# Bucle principal
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                personaje.atacar()
    
    # Obtener teclas presionadas
    teclas = pygame.key.get_pressed()
    
    # Actualizar personaje
    personaje.actualizar(teclas)
    
    # Dibujar
    pantalla.fill(VERDE_PASTO)
    
    # Dibujar sombra
    pygame.draw.ellipse(pantalla, (0, 0, 0, 50), 
                       (personaje.x - 12, personaje.y + 35, 24, 8))
    
    # Dibujar personaje
    personaje.dibujar(pantalla)
    
    # Instrucciones
    texto1 = fuente.render("Flechas/WASD: Mover", True, (255, 255, 255))
    texto2 = fuente.render("ESPACIO: Atacar con hacha", True, (255, 255, 255))
    pantalla.blit(texto1, (10, 10))
    pantalla.blit(texto2, (10, 35))
    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()