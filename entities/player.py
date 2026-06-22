import pygame
from entities.car import Car
from utils.constants import TILE_SIZE

class Player(Car):
    """Représente le joueur contrôlé sur la carte."""
    
    def __init__(self, name, base_stats, x, y):
        super().__init__(name, base_stats)
        self.grid_x = x
        self.grid_y = y
        self.target_x = x * TILE_SIZE
        self.target_y = y * TILE_SIZE
        self.pixel_x = float(self.target_x)
        self.pixel_y = float(self.target_y)
        self.moving = False
        self.move_speed = 4
        self.inventory = [] # Liste d'équipements non portés
        self.potions = 0
        self.direction = "down"

    def move(self, dx, dy):
        """Lance un déplacement si le joueur n'est pas déjà en mouvement."""
        if not self.moving:
            self.grid_x += dx
            self.grid_y += dy
            self.target_x = self.grid_x * TILE_SIZE
            self.target_y = self.grid_y * TILE_SIZE
            self.moving = True
            
            if dx > 0: self.direction = "right"
            elif dx < 0: self.direction = "left"
            elif dy > 0: self.direction = "down"
            elif dy < 0: self.direction = "up"

    def update(self):
        """Gère le déplacement fluide vers la cible."""
        if self.moving:
            if abs(self.pixel_x - self.target_x) < self.move_speed:
                self.pixel_x = self.target_x
            else:
                self.pixel_x += self.move_speed if self.target_x > self.pixel_x else -self.move_speed

            if abs(self.pixel_y - self.target_y) < self.move_speed:
                self.pixel_y = self.target_y
            else:
                self.pixel_y += self.move_speed if self.target_y > self.pixel_y else -self.move_speed

            if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
                self.moving = False

    def draw(self, surface, camera_offset=(0, 0)):
        """Affiche le joueur (rectangle pour l'instant, sprite plus tard)."""
        rect = pygame.Rect(self.pixel_x - camera_offset[0], 
                           self.pixel_y - camera_offset[1], 
                           TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, (0, 0, 255), rect) # Bleu pour le joueur

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def use_potion(self):
        if self.potions > 0:
            active_stats = self.get_active_stats()
            heal_amount = int(active_stats["max_hp"] * 0.5)
            self.stats.current_hp = min(active_stats["max_hp"], self.stats.current_hp + heal_amount)
            self.potions -= 1
            return True
        return False
