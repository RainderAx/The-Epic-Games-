import pygame
import json
import os
import sys

# Constantes calquées sur ton projet
TILE_SIZE = 40
MAP_WIDTH = 15   # Nombre de cases en largeur
MAP_HEIGHT = 12  # Nombre de cases en hauteur
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE + 200 # +200px à droite pour l'interface/menu
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (70, 70, 70)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class TileEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Epic Games - Éditeur de Cartes")
        self.clock = pygame.time.Clock()
        
        # Configuration des types de tuiles
        self.tile_types = {
            0: {"name": "Route", "color": (200, 200, 200), "img_path": "assets/tiles/road.png"},
            1: {"name": "Herbe", "color": (34, 139, 34), "img_path": "assets/tiles/grass.png"},
            2: {"name": "Obstacle", "color": (100, 100, 100), "img_path": "assets/tiles/obstacle.png"},
            3: {"name": "Teleportation", "color": (255, 215, 0), "img_path": "assets/tiles/teleportation.png"}
        }
        
        self.current_type = 0
        self.spawn_point = {"x": 1, "y": 1}
        self.map_name = "map1" # Nom du fichier par défaut
        
        # Initialisation de la grille vide (Remplie de routes '0')
        self.grid = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        self.load_textures()
        self.font = pygame.font.SysFont("Arial", 16)

    def load_textures(self):
        self.textures = {}
        for t_id, info in self.tile_types.items():
            try:
                img = pygame.image.load(info["img_path"]).convert_alpha()
                self.textures[t_id] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except:
                self.textures[t_id] = None

    def save_map(self):
        """Formate et sauvegarde la map en JSON conforme à ton architecture."""
        map_data = {
            "map_name": f"Zone {self.map_name}",
            "width": MAP_WIDTH,
            "height": MAP_HEIGHT,
            "spawn_point": self.spawn_point,
            "tile_mapping": {
                "0": "road",
                "1": "tall_grass",
                "2": "obstacle",
                "3": "teleportation"
            },
            "grid": self.grid,
            "encounter_rate": 0.15,
            "available_enemies": ["rusty_sedan", "drift_king", "mad_truck"]
        }
        
        os.makedirs("data/maps", exist_ok=True)
        file_path = f"data/maps/{self.map_name}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(map_data, f, indent=4)
        print(f"🎉 Carte sauvegardée avec succès dans : {file_path}")

    def draw_sidebar(self):
        """Dessine le panneau de contrôle à droite."""
        start_x = MAP_WIDTH * TILE_SIZE
        pygame.draw.rect(self.screen, DARK_GRAY, (start_x, 0, 200, SCREEN_HEIGHT))
        
        # Titre
        text = self.font.render("OUTILS ÉDITEUR", True, WHITE)
        self.screen.blit(text, (start_x + 10, 10))
        
        # Liste des tuiles sélectionnables
        y_offset = 50
        for t_id, info in self.tile_types.items():
            # Encadré si sélectionné
            if self.current_type == t_id:
                pygame.draw.rect(self.screen, RED, (start_x + 8, y_offset - 2, 184, 44), 2)
                
            # Dessin de l'aperçu (Image ou couleur)
            rect = pygame.Rect(start_x + 15, y_offset, TILE_SIZE, TILE_SIZE)
            if self.textures[t_id]:
                self.screen.blit(self.textures[t_id], rect.topleft)
            else:
                pygame.draw.rect(self.screen, info["color"], rect)
                
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            
            # Label
            lbl = self.font.render(f"{t_id}: {info['name']}", True, WHITE)
            self.screen.blit(lbl, (start_x + 65, y_offset + 10))
            y_offset += 55
            
        # Infos raccourcis
        y_offset += 20
        infos = [
            "Clic Gauche : Peindre",
            "Clic Droit : Effacer (Route)",
            "S : Sauvegarder dans JSON",
            "P : Définir Spawn ici",
            f"Spawn actuel : ({self.spawn_point['x']},{self.spawn_point['y']})"
        ]
        for line in infos:
            txt = self.font.render(line, True, WHITE)
            self.screen.blit(txt, (start_x + 10, y_offset))
            y_offset += 22

    def draw_grid(self):
        """Dessine le monde modifiable."""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                t_id = self.grid[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if self.textures[t_id]:
                    self.screen.blit(self.textures[t_id], rect.topleft)
                else:
                    color = self.tile_types[t_id]["color"]
                    pygame.draw.rect(self.screen, color, rect)
                    
                pygame.draw.rect(self.screen, BLACK, rect, 1) # Grille visible
                
                # Dessiner l'indicateur de Spawn
                if self.spawn_point["x"] == x and self.spawn_point["y"] == y:
                    pygame.draw.circle(self.screen, RED, rect.center, 8)

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # Gestion des entrées souris pour peindre en continu
            mouse_left, _, mouse_right = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE
            
            # Si la souris est dans la zone de la grille
            if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                if mouse_left:
                    self.grid[grid_y][grid_x] = self.current_type
                elif mouse_right:
                    self.grid[grid_y][grid_x] = 0 # Remet de la route

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_map()
                    elif event.key == pygame.K_p:
                        # Place le point d'apparition sous le curseur de la souris
                        if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                            self.spawn_point = {"x": grid_x, "y": grid_y}
                    # Raccourcis chiffrés pour changer de tuile
                    elif event.key == pygame.K_0: self.current_type = 0
                    elif event.key == pygame.K_1: self.current_type = 1
                    elif event.key == pygame.K_2: self.current_type = 2
                    elif event.key == pygame.K_3: self.current_type = 3
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Permet aussi de sélectionner la tuile en cliquant directement sur la barre latérale
                    if mouse_x >= MAP_WIDTH * TILE_SIZE:
                        click_y = mouse_y - 50
                        clicked_id = click_y // 55
                        if clicked_id in self.tile_types:
                            self.current_type = clicked_id

            self.draw_grid()
            self.draw_sidebar()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    editor = TileEditor()
    editor.run()