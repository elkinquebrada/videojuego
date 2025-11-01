# village_scene.py
import pygame
import os
from player import TavernPlayer

class VillageScene:
    """
    Village Scene: contains the shop, creator's statue,
    forest entrance, and lumberjack's house.
    """

    def __init__(self, manager):
        self.manager = manager

        # ---------------------------------------------
        # === SCENE SETUP AND COLLISIONS ===
        # ---------------------------------------------

        # Player boundaries
        self.WALL_LEFT_X = 100
        self.WALL_RIGHT_X = self.manager.WIDTH - 100
        self.PLAYER_COLLISION_Y_MIN = 450
        self.PLAYER_COLLISION_Y_MAX = self.manager.HEIGHT - 10

        # Name of accessible scenes from this location
        self.next_scene_forest = "ForestScene"  # future forest scene
        self.next_scene_shop = None  # can be activated later

        # ---------------------------------------------
        # === VISUAL ELEMENTS ===
        # ---------------------------------------------
        self.asset_dir = "assets"
        self.background = self._load_background()
        self.shop_image = self._load_image("village_shop.png", (400, 300))
        self.statue_image = self._load_image("creator_statue.png", (180, 300))
        self.forest_entrance_image = self._load_image("forest_gate.png", (350, 280))
        self.lumberhouse_image = self._load_image("lumber_house.png", (380, 310))

        # Object positions on screen
        self.shop_pos = (100, 250)
        self.statue_pos = (self.manager.WIDTH // 2 - 90, 340)
        self.forest_pos = (self.manager.WIDTH - 450, 300)
        self.lumberhouse_pos = (self.manager.WIDTH // 2 - 500, 310)

        # Collision or interaction rectangles
        self.forest_exit_rect = pygame.Rect(self.forest_pos[0]+100, self.forest_pos[1]+200, 200, 80)
        self.statue_rect = pygame.Rect(self.statue_pos[0]+40, self.statue_pos[1]+240, 100, 60)
        self.shop_rect = pygame.Rect(self.shop_pos[0]+100, self.shop_pos[1]+200, 200, 100)
        self.lumberhouse_rect = pygame.Rect(self.lumberhouse_pos[0]+100, self.lumberhouse_pos[1]+200, 180, 110)

        # Font for text
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)

        # ---------------------------------------------
        # === PLAYER SETUP ===
        # ---------------------------------------------
        self.player = pygame.Rect(self.manager.WIDTH // 2, 600, 50, 100)
        
        # Movement speeds
        self.player_speed = 300  # Normal speed
        self.player_run_speed = 500  # Running speed (with Shift)
        
        # Jump mechanics
        self.player_velocity_y = 0
        self.gravity = 1500  # Gravity force
        self.jump_strength = -600  # Jump force (negative = up)
        self.is_jumping = False
        self.ground_y = 600  # Ground level
        
        # Interaction
        self.interaction_range = 100  # Distance for interaction
        self.can_interact = False
        self.interaction_target = None

        print("🌆 VILLAGE SCENE LOADED (Press ESC to return to Tavern)")

    # ============================================================
    # === IMAGE LOADING METHODS ===
    # ============================================================

    def _load_background(self):
        """Load the village background."""
        bg_path = os.path.join(self.asset_dir, "background", "village_background.png")
        try:
            bg = pygame.image.load(bg_path).convert_alpha()
            bg = pygame.transform.scale(bg, (self.manager.WIDTH, self.manager.HEIGHT))
        except pygame.error as e:
            print(f"[ERROR] Village background not loaded: {e}")
            bg = pygame.Surface((self.manager.WIDTH, self.manager.HEIGHT))
            bg.fill((120, 100, 80))
        return bg

    def _load_image(self, filename, size):
        """Load and scale any auxiliary image."""
        path = os.path.join(self.asset_dir, "background", filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
        except pygame.error:
            img = pygame.Surface(size, pygame.SRCALPHA)
            img.fill((200, 50, 50, 180))
        return img

    # ============================================================
    # === INPUT, UPDATE, AND DRAW LOGIC ===
    # ============================================================

    def handle_input(self, event):
        """Handle individual events."""
        if event.type == pygame.KEYDOWN:
            # Jump with SPACE
            if event.key == pygame.K_SPACE and not self.is_jumping:
                self.is_jumping = True
                self.player_velocity_y = self.jump_strength
                print("🦘 Jump!")
            
            # Interact with E
            elif event.key == pygame.K_e:
                self._attempt_interaction()
            
            # Enter locations with CAPS LOCK
            elif event.key == pygame.K_CAPSLOCK:
                self._attempt_enter_location()

    def _attempt_interaction(self):
        """Check if player is near an interactable object and interact."""
        player_center = self.player.center
        
        # Check statue interaction
        if self.statue_rect.collidepoint(player_center) or \
           self._distance_to_rect(player_center, self.statue_rect) < self.interaction_range:
            print("🗿 Interacting with Creator's Statue...")
            self.interaction_target = "statue"
            # Add your interaction logic here (dialogue, cutscene, etc.)
        
        # Check shop interaction
        elif self.shop_rect.collidepoint(player_center) or \
             self._distance_to_rect(player_center, self.shop_rect) < self.interaction_range:
            print("🏪 Interacting with Shop...")
            self.interaction_target = "shop"
            # Add shop interaction logic
        
        # Check lumberhouse interaction
        elif self.lumberhouse_rect.collidepoint(player_center) or \
             self._distance_to_rect(player_center, self.lumberhouse_rect) < self.interaction_range:
            print("🏠 Interacting with Lumberjack's House...")
            self.interaction_target = "lumberhouse"
            # Add house interaction logic
        
        else:
            print("❌ Nothing to interact with nearby")

    def _attempt_enter_location(self):
        """Enter a location if player is near the entrance (CAPS LOCK)."""
        player_center = self.player.center
        
        # Check forest entrance
        if self.forest_exit_rect.collidepoint(player_center) or \
           self._distance_to_rect(player_center, self.forest_exit_rect) < self.interaction_range:
            print("🌲 Entering the Forest...")
            return self.next_scene_forest
        
        # Check shop entrance
        elif self.shop_rect.collidepoint(player_center) or \
             self._distance_to_rect(player_center, self.shop_rect) < self.interaction_range:
            print("🏪 Entering the Shop...")
            if self.next_scene_shop:
                return self.next_scene_shop
            else:
                print("⚠️ Shop is not available yet")
                return None
        
        # Check lumberhouse entrance
        elif self.lumberhouse_rect.collidepoint(player_center) or \
             self._distance_to_rect(player_center, self.lumberhouse_rect) < self.interaction_range:
            print("🏠 Entering Lumberjack's House...")
            return "LumberjackHouse"  # You'll need to create this scene
        
        else:
            print("❌ No entrance nearby")
            return None

    def _distance_to_rect(self, point, rect):
        """Calculate distance from point to nearest edge of rectangle."""
        x, y = point
        dx = max(rect.left - x, 0, x - rect.right)
        dy = max(rect.top - y, 0, y - rect.bottom)
        return (dx * dx + dy * dy) ** 0.5

    def _check_nearby_interactions(self):
        """Check if player is near any interactable object."""
        player_center = self.player.center
        
        # Check all interactable objects and entrances
        objects = [
            (self.statue_rect, "statue", "Creator's Statue (E: interact)"),
            (self.shop_rect, "shop", "Village Shop (E: interact, CAPS: enter)"),
            (self.lumberhouse_rect, "lumberhouse", "Lumberjack's House (E: interact, CAPS: enter)"),
            (self.forest_exit_rect, "forest", "Forest Entrance (CAPS: enter)")
        ]
        
        for rect, obj_id, obj_name in objects:
            if self._distance_to_rect(player_center, rect) < self.interaction_range:
                self.can_interact = True
                self.interaction_target = obj_name
                return
        
        self.can_interact = False
        self.interaction_target = None

    def update(self, dt):
        """Update logic and player movement."""
        
        # Check if there's a pending scene change from CAPS LOCK
        if self.pending_scene_change:
            result = self.pending_scene_change
            self.pending_scene_change = None
            return result
        
        keys = pygame.key.get_pressed()

        # Determine current speed (running with Shift)
        current_speed = self.player_run_speed if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else self.player_speed

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.player.x -= int(current_speed * dt)
        if keys[pygame.K_RIGHT]:
            self.player.x += int(current_speed * dt)

        # Horizontal boundaries
        self.player.x = max(self.WALL_LEFT_X, min(self.player.x, self.WALL_RIGHT_X - self.player.width))

        # Jump and gravity mechanics
        if self.is_jumping:
            self.player_velocity_y += self.gravity * dt
            self.player.y += int(self.player_velocity_y * dt)
            
            # Landing on ground
            if self.player.y >= self.ground_y:
                self.player.y = self.ground_y
                self.player_velocity_y = 0
                self.is_jumping = False

        # Check nearby interactions
        self._check_nearby_interactions()

        # Return to tavern with ESC
        if keys[pygame.K_ESCAPE]:
            return "TavernScene"

        return None

    def draw(self, surface):
        """Draw all village elements."""
        # Background
        surface.blit(self.background, (0, 0))

        # Scene elements
        surface.blit(self.shop_image, self.shop_pos)
        surface.blit(self.statue_image, self.statue_pos)
        surface.blit(self.forest_entrance_image, self.forest_pos)
        surface.blit(self.lumberhouse_image, self.lumberhouse_pos)

        # Player (placeholder visual)
        player_color = (0, 255, 0) if self.is_jumping else (0, 0, 255)
        pygame.draw.rect(surface, player_color, self.player)

        # Draw interaction indicators (optional debug)
        # pygame.draw.rect(surface, (0, 255, 0), self.forest_exit_rect, 2)
        # pygame.draw.rect(surface, (255, 255, 0), self.statue_rect, 2)
        # pygame.draw.rect(surface, (255, 0, 255), self.shop_rect, 2)
        # pygame.draw.rect(surface, (0, 255, 255), self.lumberhouse_rect, 2)

        # Interaction prompt
        if self.can_interact:
            prompt_text = self.small_font.render(f"{self.interaction_target}", True, (255, 255, 0))
            text_x = self.manager.WIDTH // 2 - prompt_text.get_width() // 2
            surface.blit(prompt_text, (text_x, self.manager.HEIGHT - 100))

        # Control instructions
        info_text = self.font.render("ESC: Return | SPACE: Jump | E: Interact | CAPS: Enter | SHIFT: Run", True, (255, 255, 255))
        surface.blit(info_text, (self.manager.WIDTH // 2 - info_text.get_width() // 2, 20))
        
     