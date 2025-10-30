# 🌟 Cuentos de Mentes Estrelladas

**Demo 2.5D de Aventura, Suspenso y Terror**

Un juego de aventura con perspectiva 2.5D desarrollado en Python con Pygame, que combina exploración, combate y una narrativa de terror atmosférico.

![Version](https://img.shields.io/badge/version-2.5%20Demo-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Pygame](https://img.shields.io/badge/pygame-2.0+-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Cómo Jugar](#-cómo-jugar)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Escenas Disponibles](#-escenas-disponibles)
- [Sistema de Animación](#-sistema-de-animación)
- [Configuración y Personalización](#-configuración-y-personalización)
- [Desarrollo](#-desarrollo)
- [Créditos](#-créditos)

---

## ✨ Características

### Sistema de Juego
- **Perspectiva 2.5D**: Profundidad visual con escala dinámica basada en posición
- **Sistema de Escenas**: Arquitectura modular con múltiples escenas interconectadas
- **Animaciones Suaves**: Sistema completo de animación de sprites con interpolación
- **Combate**: Sistema de ataque con hacha y animaciones
- **Interfaz Pulida**: UI con paneles estilizados, mensajes contextuales y objetivos

### Escenas Actuales
1. **Taberna** - Punto de inicio, interior atmosférico
2. **Mundo Exterior** - Mapa de transición (en desarrollo)
3. **Bosque del Caza Sombras** - Escena principal con enemigos y exploración

### Características Técnicas
- Resolución adaptativa (1280x700 - 1400x800)
- Sistema de partículas (niebla, efectos ambientales)
- Ordenamiento por profundidad Z para renderizado 2.5D
- Detección de colisiones con zonas invisibles
- Sistema de eventos y cambio de escenas dinámico

---

## 📦 Requisitos

### Software Necesario
- **Python 3.8+** ([Descargar](https://www.python.org/downloads/))
- **Pygame 2.0+**

### Instalar Pygame
```bash
pip install pygame
```

### Verificar Instalación
```bash
python -c "import pygame; print(pygame.version.ver)"
```

---

## 🚀 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/cuentos-mentes-estrelladas.git
cd cuentos-mentes-estrelladas
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

*O manualmente:*
```bash
pip install pygame
```

### 3. Verificar Estructura de Assets
Asegúrate de tener la siguiente estructura de carpetas:
```
assets/
├── background/
│   ├── tavern_background.png
│   └── tavern_door.png
├── Idle/
│   └── Front.png
└── Right_Left_Walk/
    ├── 1.png
    ├── 2.png
    └── ... (hasta 15.png)
```

### 4. Ejecutar el Juego
```bash
python main.py
```

---

## 🎮 Cómo Jugar

### Controles

| Acción | Teclas |
|--------|--------|
| **Mover Arriba** | `W` o `↑` |
| **Mover Abajo** | `S` o `↓` |
| **Mover Izquierda** | `A` o `←` |
| **Mover Derecha** | `D` o `→` |
| **Atacar** | `ESPACIO` |
| **Volver (en Mundo)** | `ESC` |
| **Salir del Juego** | Cerrar ventana |

### Objetivo Actual
- Explora la **Taberna** inicial
- Atraviesa la puerta para salir al **Mundo Exterior**
- Accede al **Bosque del Caza Sombras** (cambio manual de escena)
- Encuentra al misterioso **Caza Sombras**

---

## 📁 Estructura del Proyecto

```
cuentos-mentes-estrelladas/
│
├── main.py                 # Gestor de escenas y bucle principal
├── player.py              # Clase del jugador y sistema de armas
├── tavern_scene.py        # Escena de la taberna
├── world_scene.py         # Escena del mundo exterior
├── forest_scene.py        # Escena del bosque (standalone)
│
├── assets/                # Recursos gráficos
│   ├── background/        # Fondos de escenas
│   ├── Idle/              # Sprites de personaje idle
│   └── Right_Left_Walk/   # Sprites de caminata
│
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

### Archivos Principales

#### `main.py` (SceneManager)
Gestiona el flujo del juego y el cambio entre escenas.

**Funciones clave:**
- `change_scene(scene_name)`: Cambia la escena activa
- `run()`: Bucle principal del juego

#### `player.py` (TavernPlayer)
Contiene la lógica del personaje jugable.

**Características:**
- Sistema de animación con 15 frames de caminata
- Escala dinámica 2.5D basada en posición Y
- Sistema de ataque con hacha
- Detección de colisiones con límites

#### `tavern_scene.py` (TavernScene)
Primera escena del juego.

**Elementos:**
- Fondo de taberna
- Puerta de salida interactiva
- Sistema de colisión con paredes invisibles
- Detección de zona de salida

#### `world_scene.py` (WorldScene)
Escena de transición (placeholder).

**Estado:** En desarrollo
**Función:** Conectar taberna con otras áreas

#### `forest_scene.py` (Forest Scene)
Escena standalone del bosque oscuro.

**Elementos:**
- Árboles 3D con animación de balanceo
- Sistema de partículas de niebla
- Elementos de suelo (rocas, pasto)
- UI de objetivos
- Sistema de mensajes contextuales

---

## 🎬 Escenas Disponibles

### 1. Taberna (TavernScene)
**Descripción:** Interior acogedor de una taberna medieval.

**Características:**
- Fondo completo renderizado
- Puerta funcional para salir
- Colisiones con paredes laterales
- Zona de suelo restringida

**Controles de Ajuste:**
```python
PLAYER_COLLISION_Y_MIN = 480
PLAYER_COLLISION_Y_MAX = HEIGHT - 10
WALL_LEFT_X = 300
WALL_RIGHT_X = WIDTH - 50
```

### 2. Mundo Exterior (WorldScene)
**Estado:** Placeholder
**Objetivo:** Punto de conexión entre áreas

**Próximas características:**
- Mapa del mundo
- NPCs
- Puntos de interés

### 3. Bosque del Caza Sombras (ForestScene)
**Descripción:** Bosque oscuro y misterioso con atmósfera de terror.

**Elementos visuales:**
- 25 árboles con profundidad 3D
- 40 elementos de suelo
- 30 partículas de niebla
- Luna con efecto de resplandor
- Gradiente de cielo nocturno

**Objetivos:**
- Explorar el bosque
- Localizar al Caza Sombras
- Sobrevivir a los encuentros

---

## 🎨 Sistema de Animación

### Estados del Personaje
- **Idle (Reposo)**: 4 direcciones (front, back, left, right)
- **Walk (Caminata)**: 15 frames de animación suave
- **Attack (Ataque)**: 10 frames con movimiento de hacha

### Formato de Sprites
- **Tipo:** PNG con transparencia (RGBA)
- **Escala Base:** Controlada por `SCALE_FACTOR = 0.10`
- **Suavizado:** Activado con `smoothscale()`

### Agregar Nuevas Animaciones

1. Coloca los sprites en `assets/[nombre_carpeta]/`
2. Nombra los archivos secuencialmente: `1.png`, `2.png`, etc.
3. Modifica `_load_animations()` en `player.py`:

```python
# Ejemplo: Agregar animación de correr
run_frames = load_walk_sequence('Run_Animation', 12)
animations['front_run'] = run_frames
```

---

## ⚙️ Configuración y Personalización

### Ajustar Resolución
En `main.py`:
```python
self.WIDTH, self.HEIGHT = 1400, 800  # Cambia estos valores
```

### Cambiar Velocidad del Jugador
En `player.py`:
```python
self.speed = 3  # Mayor = más rápido
```

### Modificar Escala 2.5D
En `player.py` → `get_scale()`:
```python
min_scale = 0.8  # Escala mínima (arriba)
max_scale = 1.2  # Escala máxima (abajo)
```

### Ajustar Colisiones de la Taberna
En `tavern_scene.py`:
```python
self.PLAYER_COLLISION_Y_MIN = 480  # Límite superior
self.PLAYER_COLLISION_Y_MAX = HEIGHT - 10  # Límite inferior
self.WALL_LEFT_X = 300  # Pared izquierda
self.WALL_RIGHT_X = WIDTH - 50  # Pared derecha
```

### Cambiar Posición de la Puerta
```python
self.DOOR_VISUAL_X = WIDTH // 2 - 350
self.DOOR_VISUAL_Y = 480 - 390
self.DOOR_SCALE_WIDTH = 400
self.DOOR_SCALE_HEIGHT = 380
```

---

## 🛠️ Desarrollo

### Roadmap

#### Versión 3.0 (Próxima)
- [ ] Integrar `forest_scene.py` en el flujo principal
- [ ] Sistema de combate completo
- [ ] Enemigos con IA básica
- [ ] Sistema de inventario
- [ ] Diálogos con NPCs

#### Versión 3.5
- [ ] Sistema de guardado/carga
- [ ] Más escenas explorables
- [ ] Boss: El Caza Sombras
- [ ] Sistema de puzzles

#### Versión 4.0 (Completa)
- [ ] Historia completa con múltiples capítulos
- [ ] Sistema de día/noche
- [ ] Efectos de sonido y música
- [ ] Cinemáticas
- [ ] Final múltiple

### Agregar Nueva Escena

1. **Crear archivo de escena:**
```python
# nueva_escena.py
import pygame

class NuevaEscena:
    def __init__(self, manager):
        self.manager = manager
        
    def handle_input(self, event):
        pass
        
    def update(self, dt):
        return None  # o nombre de escena para cambiar
        
    def draw(self, surface):
        surface.fill((100, 150, 200))
```

2. **Registrar en `main.py`:**
```python
from nueva_escena import NuevaEscena

# En change_scene():
elif new_scene_name == "NuevaEscena":
    self.current_scene = NuevaEscena(self)
```

3. **Activar desde otra escena:**
```python
# En cualquier escena, en update():
if condicion_cumplida:
    return "NuevaEscena"
```

### Debugging

**Activar líneas de colisión:**
En `tavern_scene.py` → `draw()`, descomenta:
```python
pygame.draw.rect(surface, (0, 255, 0), self.exit_rect, 2)
pygame.draw.line(surface, (255, 0, 0), (self.WALL_LEFT_X, 0), ...)
```

**Ver información del jugador:**
```python
# En player.py → update():
print(f"Pos: ({self.x}, {self.y}), Z: {self.z}, Escala: {current_scale}")
```

---

## 👥 Créditos

### Desarrollo
- **Programación:** [Tu Nombre]
- **Diseño de Juego:** [Tu Nombre]
- **Arte:** [Tus créditos o "Asset Pack: [nombre]"]

### Herramientas
- **Motor:** Pygame 2.0+
- **Lenguaje:** Python 3.8+
- **Editor:** [Tu editor preferido]

### Recursos
- Sprites de personaje: [Fuente]
- Fondos: [Fuente]
- Inspiración: Juegos clásicos 2.5D

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2024 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🐛 Reporte de Bugs

Si encuentras un error:
1. Verifica que tienes todos los assets en las carpetas correctas
2. Revisa que Pygame esté actualizado
3. Abre un Issue en GitHub con:
   - Descripción del problema
   - Pasos para reproducirlo
   - Captura de pantalla si es posible
   - Mensaje de error completo

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 📞 Contacto

- **GitHub:** [tu-usuario](https://github.com/tu-usuario)
- **Email:** tu-email@ejemplo.com
- **Discord:** [Servidor del proyecto]

---

## 🙏 Agradecimientos

- A la comunidad de Pygame por la documentación
- A los testers que ayudaron en el desarrollo
- A [menciones especiales]

---

**¡Gracias por jugar Cuentos de Mentes Estrelladas!** 🌟✨

*"En la oscuridad del bosque, las estrellas guían a los perdidos..."*