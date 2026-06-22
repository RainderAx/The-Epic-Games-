from utils.enum import TileType

class CollisionSystem:
    """Gère les collisions sur la carte."""
    
    @staticmethod
    def can_move_to(grid_x, grid_y, game_map):
        """Vérifie si le joueur peut se déplacer sur une case donnée."""
        # Vérifier les limites de la carte
        if grid_x < 0 or grid_x >= game_map.width or grid_y < 0 or grid_y >= game_map.height:
            return False
            
        # Vérifier le type de case
        tile = game_map.get_tile(grid_x, grid_y)
        if tile.type == TileType.OBSTACLE:
            return False
            
        return True
