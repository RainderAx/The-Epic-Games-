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
        
        color = (200, 200, 200) 
        if self.type == TileType.GRASS:
            color = (34, 139, 34) 
        elif self.type == TileType.OBSTACLE:
            color = (100, 100, 100) 
        pygame.draw.rect(surface, color, draw_rect)
       
        pygame.draw.rect(surface, (50, 50, 50), draw_rect, 1)
