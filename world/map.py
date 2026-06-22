from world.tile import Tile
from utils.enum import TileType
from utils.helpers import load_json

class Map:
    """Gère la grille de cases et le chargement des niveaux."""
    
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.tiles = []
        self.generate_empty_map()

    def generate_empty_map(self):
        """Génère une carte remplie de route par défaut."""
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Tile(x, y, TileType.ROAD))
            self.tiles.append(row)

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def load_from_file(self, file_path):
        """Charge une carte depuis un fichier JSON."""
        data = load_json(file_path)
        if not data:
            return
            
        self.width = data.get("width", self.width)
        self.height = data.get("height", self.height)
        
        # Mapping des caractères ou IDs vers TileType
        type_map = {
            "R": TileType.ROAD,
            "G": TileType.GRASS,
            "O": TileType.OBSTACLE
        }
        
        layout = data.get("layout", [])
        self.tiles = []
        for y, row_str in enumerate(layout):
            row = []
            for x, char in enumerate(row_str):
                tile_type = type_map.get(char, TileType.ROAD)
                row.append(Tile(x, y, tile_type))
            self.tiles.append(row)

    def draw(self, surface, camera_offset=(0, 0)):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface, camera_offset)
