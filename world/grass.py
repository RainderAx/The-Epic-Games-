import random
from utils.enum import TileType

class GrassLogic:
    """Gère les rencontres aléatoires dans les hautes herbes."""
    
    @staticmethod
    def check_encounter(tile_type):
        """Retourne True si un combat est déclenché."""
        if tile_type == TileType.GRASS:
            # 15% de chance de rencontre par pas dans l'herbe
            return random.random() <= 0.15
        return False
