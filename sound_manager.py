import pygame
import random

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Volúmenes por defecto
        self.master_volume = 0.7
        self.music_volume = 0.5
        self.sfx_volume = 0.8
        
        # Diccionarios para almacenar sonidos
        self.sounds = {}
        self.music_tracks = {}
        
        # Estado de reproducción
        self.current_music = None
        self.is_music_playing = False
        
        # Canales de audio para efectos de sonido
        self.footstep_channel = pygame.mixer.Channel(0)
        self.ambient_channel = pygame.mixer.Channel(1)
        self.action_channel = pygame.mixer.Channel(2)
        
    def load_sound(self, name, filepath):
        """Cargar un efecto de sonido"""
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.sfx_volume * self.master_volume)
            self.sounds[name] = sound
            print(f"Sonido '{name}' cargado exitosamente")
            return True
        except Exception as e:
            print(f"Error al cargar sonido '{name}': {e}")
            return False
    
    def load_music(self, name, filepath):
        """Cargar una pista de música"""
        try:
            self.music_tracks[name] = filepath
            print(f"Música '{name}' registrada exitosamente")
            return True
        except Exception as e:
            print(f"Error al registrar música '{name}': {e}")
            return False
    
    def play_sound(self, name, loops=0, channel=None):
        """Reproducir un efecto de sonido"""
        if name in self.sounds:
            if channel:
                channel.play(self.sounds[name], loops=loops)
            else:
                self.sounds[name].play(loops=loops)
        else:
            print(f"Sonido '{name}' no encontrado")
    
    def play_music(self, name, loops=-1, fade_ms=1000):
        """Reproducir música de fondo"""
        if name in self.music_tracks:
            try:
                if self.is_music_playing:
                    pygame.mixer.music.fadeout(fade_ms)
                
                pygame.mixer.music.load(self.music_tracks[name])
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
                self.current_music = name
                self.is_music_playing = True
                print(f"Reproduciendo música: {name}")
            except Exception as e:
                print(f"Error al reproducir música '{name}': {e}")
        else:
            print(f"Música '{name}' no encontrada")
    
    def stop_music(self, fade_ms=1000):
        """Detener la música actual"""
        if self.is_music_playing:
            pygame.mixer.music.fadeout(fade_ms)
            self.is_music_playing = False
            self.current_music = None
    
    def pause_music(self):
        """Pausar la música"""
        if self.is_music_playing:
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Reanudar la música"""
        if self.is_music_playing:
            pygame.mixer.music.unpause()
    
    def play_footstep(self, surface_type="grass"):
        """Reproducir sonido de pasos según la superficie"""
        # Aquí puedes tener diferentes sonidos según el tipo de superficie
        if f"footstep_{surface_type}" in self.sounds:
            self.play_sound(f"footstep_{surface_type}", channel=self.footstep_channel)
    
    def play_ambient(self, ambient_type):
        """Reproducir sonidos ambientales"""
        if ambient_type in self.sounds:
            self.play_sound(ambient_type, loops=-1, channel=self.ambient_channel)
    
    def stop_ambient(self):
        """Detener sonidos ambientales"""
        self.ambient_channel.stop()
    
    def set_master_volume(self, volume):
        """Ajustar volumen maestro (0.0 a 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self.update_volumes()
    
    def set_music_volume(self, volume):
        """Ajustar volumen de música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def set_sfx_volume(self, volume):
        """Ajustar volumen de efectos de sonido (0.0 a 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self.update_volumes()
    
    def update_volumes(self):
        """Actualizar volúmenes de todos los sonidos"""
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def play_impact(self):
        """Método especial para reproducir el sonido de impacto"""
        self.play_sound("impacto", channel=self.action_channel)


class SoundGenerator:
    """Generador de sonidos procedurales simples cuando no hay archivos de audio"""
    
    @staticmethod
    def generate_footstep():
        """Generar sonido de paso simple"""
        duration = 100  # milisegundos
        frequency = 150
        sample_rate = 22050
        
        n_samples = int(sample_rate * duration / 1000)
        
        # Generar ruido blanco breve
        import numpy as np
        noise = np.random.uniform(-1, 1, n_samples)
        
        # Envelope para suavizar
        envelope = np.linspace(1, 0, n_samples)
        wave = (noise * envelope * 0.3 * 32767).astype(np.int16)
        
        # Crear surface de pygame
        stereo_wave = np.column_stack((wave, wave))
        sound = pygame.sndarray.make_sound(stereo_wave)
        
        return sound
    
    @staticmethod
    def generate_jump():
        """Generar sonido de salto simple"""
        duration = 200
        sample_rate = 22050
        
        n_samples = int(sample_rate * duration / 1000)
        
        import numpy as np
        t = np.linspace(0, duration/1000, n_samples)
        frequency = 300 + 200 * np.exp(-t * 10)  # Frecuencia descendente
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Envelope
        envelope = np.exp(-t * 8)
        wave = (wave * envelope * 0.3 * 32767).astype(np.int16)
        
        stereo_wave = np.column_stack((wave, wave))
        sound = pygame.sndarray.make_sound(stereo_wave)
        
        return sound
    
    @staticmethod
    def generate_ambient_wind():
        """Generar sonido de viento ambiental"""
        duration = 2000  # 2 segundos para loop
        sample_rate = 22050
        
        n_samples = int(sample_rate * duration / 1000)
        
        import numpy as np
        # Ruido rosa filtrado para simular viento
        noise = np.random.uniform(-1, 1, n_samples)
        
        # Filtro pasa-bajos simple
        from scipy import signal
        b, a = signal.butter(2, 0.05)
        filtered = signal.filtfilt(b, a, noise)
        
        wave = (filtered * 0.2 * 32767).astype(np.int16)
        
        stereo_wave = np.column_stack((wave, wave))
        sound = pygame.sndarray.make_sound(stereo_wave)
        
        return sound


# Función de inicialización rápida para el juego
def init_game_sounds(sound_manager):
    """
    Inicializar sonidos del juego
    Puedes reemplazar las rutas con tus propios archivos de audio
    """
    
    # *** CARGAR EL SONIDO DE IMPACTO ***
    sound_manager.load_sound("impacto", r"C:\Users\PC\Desktop\video_juego\imagenes\impacto.mp3")
    
    # Ejemplo de carga de otros sonidos (descomenta cuando tengas los archivos)
    # sound_manager.load_sound("footstep_grass", "assets/sounds/footstep_grass.wav")
    # sound_manager.load_sound("footstep_stone", "assets/sounds/footstep_stone.wav")
    # sound_manager.load_sound("jump", "assets/sounds/jump.wav")
    # sound_manager.load_sound("land", "assets/sounds/land.wav")
    # sound_manager.load_sound("ambient_wind", "assets/sounds/wind.wav")
    # sound_manager.load_sound("ambient_forest", "assets/sounds/forest_ambient.wav")
    # sound_manager.load_sound("ui_select", "assets/sounds/ui_select.wav")
    
    # Ejemplo de carga de música
    # sound_manager.load_music("theme_forest", "assets/music/forest_theme.mp3")
    # sound_manager.load_music("theme_menu", "assets/music/menu_theme.mp3")
    
    print("Sistema de sonido inicializado")
    print("✓ Sonido de impacto cargado y listo para usar")
    print("Nota: Agrega más archivos de audio en la carpeta 'assets/sounds/' y 'assets/music/'")
    
    return sound_manager


# Clase auxiliar para manejar sonidos del jugador
class PlayerSoundController:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.footstep_timer = 0
        self.footstep_interval = 0.35  # Segundos entre pasos
        self.last_grounded = True
        
    def update(self, player, dt):
        """Actualizar sonidos del jugador basado en su estado"""
        
        # Sonidos de pasos
        if (player.vel_x != 0 or player.vel_z != 0) and not player.jumping:
            self.footstep_timer += dt
            if self.footstep_timer >= self.footstep_interval:
                self.sound_manager.play_footstep("grass")
                self.footstep_timer = 0
        else:
            self.footstep_timer = 0
        
        # Sonido de aterrizaje
        if self.last_grounded == False and not player.jumping and player.vel_y == 0:
            if "land" in self.sound_manager.sounds:
                self.sound_manager.play_sound("land")
        
        self.last_grounded = not player.jumping


# ==== SCRIPT DE PRUEBA ====
if __name__ == "__main__":
    """Ejecuta este archivo directamente para probar el sonido de impacto"""
    
    print("=== Probando sonido de impacto ===")
    
    # Inicializar pygame
    pygame.init()
    
    # Crear sound manager
    sound_manager = SoundManager()
    
    # Cargar sonidos
    init_game_sounds(sound_manager)
    
    # Reproducir el sonido de impacto en loop durante 30 segundos
    print("\n▶ Reproduciendo impacto en loop por 30 segundos...")
    sound_manager.play_sound("impacto", loops=-1)  # -1 = loop infinito
    
    # Esperar 30 segundos
    print("⏱ Esperando 30 segundos...")
    pygame.time.wait(30000)  # 30000 milisegundos = 30 segundos
    
    # Detener el sonido
    sound_manager.action_channel.stop()
    print("⏹ Sonido detenido")
    
    print("✓ Prueba completada!\n")
    
    # Cerrar pygame
    pygame.quit()