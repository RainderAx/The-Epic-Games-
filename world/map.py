import pygame
from world.tile import Tile
from utils.enum import TileType
from utils.helpers import load_json
from utils.constants import TILE_SIZE

class Map:
    """Gère la grille de cases, le chargement des niveaux et les textures."""
    
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.tiles = []
        self.map_name = "Carte Inconnue"
        self.encounter_rate = 0.1
        self.spawn_point = {"x": 0, "y": 0}
        
        # Centralisation et redimensionnement automatique des textures
        self.textures = {}
        self.load_textures()
        
        self.generate_empty_map()

    def load_textures(self):
        """Charge et redimensionne les images pour qu'elles correspondent à TILE_SIZE."""
        paths = {
            TileType.ROAD: "assets/tiles/road.png",
            TileType.GRASS: "assets/tiles/grass.png",
            TileType.OBSTACLE: "assets/tiles/obstacle.png"
        }
        
        for tile_type, path in paths.items():
            try:
                # Chargement de l'image
                img = pygame.image.load(path).convert_alpha()
                # Redimensionnement forcé pour fitter parfaitement dans la case
                self.textures[tile_type] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except (pygame.error, FileNotFoundError):
                # Sécurité si l'image est manquante
                print(f"Erreur : Impossible de charger {path}. Une couleur unie sera utilisée.")
                self.textures[tile_type] = None

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
        """Charge une carte depuis un fichier JSON (compatible avec map1.json)."""
        data = load_json(file_path)
        if not data:
            return False
            
        self.map_name = data.get("map_name", "Route sans nom")
        self.width = data.get("width", self.width)
        self.height = data.get("height", self.height)
        self.encounter_rate = data.get("encounter_rate", 0.15)
        self.spawn_point = data.get("spawn_point", {"x": 0, "y": 0})
        
        # Correspondance avec le format numérique du JSON
        type_map = {
            0: TileType.ROAD,
            1: TileType.GRASS,
            2: TileType.OBSTACLE
        }
        
        grid = data.get("grid", [])
        if not grid:
            return False
            
        self.tiles = []
        for y, row_data in enumerate(grid):
            row = []
            for x, val in enumerate(row_data):
                tile_type = type_map.get(val, TileType.ROAD)
                row.append(Tile(x, y, tile_type))
            self.tiles.append(row)
        return True

    def draw(self, surface, camera_offset=(0, 0)):
        """Dessine chaque case en lui passant sa texture correspondante."""
        for row in self.tiles:
            for tile in row:
                texture = self.textures.get(tile.type)
                tile.draw(surface, texture, camera_offset)