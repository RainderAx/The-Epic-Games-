import pygame
import sys
import json
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
from entities.car import Car
from entities.stats import Stats
from equipment.equipment import Equipment

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Car RPG Roguelite")
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_data()
        self.init_player()

    def load_data(self):
        """Charge les données JSON en mémoire."""
        # Dans un cas réel, utiliser open('data/equipments.json', 'r')
        # Ici, nous simulons le chargement pour la démonstration
        self.equipment_data = {
            "v8_engine": {"name": "Moteur V8", "slot": "engine", "bonuses": {"hp": 5, "attack": 10}},
            "sport_tires": {"name": "Pneus Sport", "slot": "tires", "bonuses": {"dodge": 8}}
        }

    def init_player(self):
        """Initialise le joueur avec des stats de base et un premier équipement."""
        player_stats = Stats(hp=50, attack=5, defense=2, dodge=5)
        self.player = Car("Voiture Héros", player_stats)
        
        # Exemple d'attribution de loot (Moteur V8)
        engine_data = self.equipment_data["v8_engine"]
        starter_engine = Equipment("v8_engine", engine_data)
        self.player.equip(starter_engine)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Logique de mise à jour (déplacement, collisions, déclenchement combats)
        pass

    def draw(self):
        self.screen.fill(WHITE)
        
        # Exemple basique d'UI pour afficher les stats en haut à gauche
        font = pygame.font.SysFont(None, 24)
        stats = self.player.get_active_stats()
        text = f"PV: {self.player.stats.current_hp}/{stats['max_hp']} | ATK: {stats['attack']}"
        img = font.render(text, True, (0, 0, 0))
        self.screen.blit(img, (20, 20))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()