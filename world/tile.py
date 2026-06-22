import pygame
from utils.enum import TileType
from utils.constants import TILE_SIZE

class Tile:
    """Représente une case individuelle sur la carte."""
    
    def __init__(self, x, y, tile_type: TileType):
        self.x = x
        self.y = y
        self.type = tile_type
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, surface, camera_offset=(0, 0)):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset[0]
        draw_rect.y -= camera_offset[1]
        
        color = (200, 200, 200) # Gris par défaut (Route)
        if self.type == TileType.GRASS:
            color = (34, 139, 34) # Vert (Herbe)
        elif self.type == TileType.OBSTACLE:
            color = (100, 100, 100) # Gris foncé (Obstacle)
            
        pygame.draw.rect(surface, color, draw_rect)
        # Bordure pour mieux voir les cases
        pygame.draw.rect(surface, (50, 50, 50), draw_rect, 1)
