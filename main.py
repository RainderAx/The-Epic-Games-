import pygame
import sys
import os
import random
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, TILE_SIZE
from utils.enum import GameState, TileType
from utils.helpers import load_json, draw_text
from entities.player import Player
from entities.ennemy import Ennemy
from entities.stats import Stats
from equipment.equipment import Equipment
from world.map import Map
from world.collision import CollisionSystem
from world.grass import GrassLogic
from battle.battle_manager import BattleManager
from battle.loot_system import LootSystem
from save.save_manager import SaveManager
from ui.menu import Menu
from ui.battle_ui import BattleUI
from ui.inventory_menu import InventoryMenu
from ui.equipment_menu import EquipmentMenu
from ui.shop_menu import ShopMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Epic Games: Car RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.current_map_file = 'data/maps/map1.json'

        self.load_data()
        self.init_game_objects()

    def load_data(self):
        # 1. Chargement des équipements
        raw_equip = load_json('data/equipments.json')
        self.equipment_data = {}
        if raw_equip:
            for category in raw_equip.values():
                if isinstance(category, dict):
                    self.equipment_data.update(category)
        
        # 2. Chargement des voitures (joueur et ennemis)
        car_path = 'data/cars.json'
        self.car_data = load_json(car_path)

        # Fallbacks si fichiers vides ou manquants
        if not self.equipment_data:
            self.equipment_data = {
                "v8_engine": {"name": "Moteur V8", "slot": "engine", "bonuses": {"hp": 5, "attack": 10}},
                "sport_tires": {"name": "Pneus Sport", "slot": "tires", "bonuses": {"dodge": 8}}
            }
        
        if not self.car_data:
            self.car_data = {
                "player": {"name": "Voiture Héros", "sprite": "assets/cars/McQueenBack.png", "base_stats": {"hp": 50, "attack": 10, "defense": 5, "dodge": 5}},
                "enemies": {"rusty_sedan": {"name": "Berline Rouillée", "sprite": "assets/ennemies/Berline_Rouillee.png", "base_stats": {"hp": 30, "attack": 8, "defense": 2, "dodge": 3}}}
            }

    def init_game_objects(self):
        # Initialisation de la carte
        self.game_map = Map()
        if not self.game_map.load_from_file(self.current_map_file):
            self.game_map.generate_empty_map()

        # Initialisation du joueur avec les données de cars.json
        p_data = self.car_data.get("player", {})
        p_stats_data = p_data.get("base_stats", {"hp": 50, "attack": 10, "defense": 5, "dodge": 5})
        player_stats = Stats(
            hp=p_stats_data["hp"],
            attack=p_stats_data["attack"],
            defense=p_stats_data["defense"],
            dodge=p_stats_data["dodge"]
        )
        
        spawn_point = getattr(self.game_map, "spawn_point", {"x": 0, "y": 0})
        spawn_x = spawn_point.get("x", 0)
        spawn_y = spawn_point.get("y", 0)
        
        self.player = Player(p_data.get("name", "Héros"), player_stats, spawn_x, spawn_y, sprite_path=p_data.get("sprite"))
        
        # UI
        self.menu = Menu(self.screen)
        self.battle_ui = None
        self.inventory_menu = InventoryMenu(self.screen, self.player)
        self.equipment_menu = EquipmentMenu(self.screen, self.player)
        self.shop_menu = ShopMenu(self.screen, self.player, self.equipment_data)
        self.save_manager = SaveManager()

    def change_map(self, new_map_path):
        """Gère la transition entre deux cartes."""
        self.current_map_file = new_map_path
        if self.game_map.load_from_file(new_map_path):
            # Repositionner le joueur au nouveau spawn point
            spawn_point = self.game_map.spawn_point
            self.player.grid_x = spawn_point["x"]
            self.player.grid_y = spawn_point["y"]
            self.player.pixel_x = float(self.player.grid_x * TILE_SIZE)
            self.player.pixel_y = float(self.player.grid_y * TILE_SIZE)
            self.player.target_x = self.player.grid_x * TILE_SIZE
            self.player.target_y = self.player.grid_y * TILE_SIZE
            self.player.moving = False
            print(f"Transition vers {self.game_map.map_name}")

    def start_battle(self, boss_id=None):
        # Choisir un ennemi
        if boss_id:
            enemy_id = boss_id
        else:
            available = self.game_map.available_enemies
            if not available:
                available = list(self.car_data.get("enemies", {}).keys())
            enemy_id = random.choice(available)
            
        e_data = self.car_data["enemies"].get(enemy_id)
        if not e_data: # Fallback
            e_data = list(self.car_data["enemies"].values())[0]
        
        e_stats_data = e_data["base_stats"]
        enemy_stats = Stats(
            hp=e_stats_data["hp"],
            attack=e_stats_data["attack"],
            defense=e_stats_data["defense"],
            dodge=e_stats_data["dodge"]
        )
        
        enemy = Ennemy(e_data["name"], enemy_stats, sprite_path=e_data.get("sprite"), loot_table=e_data.get("loot_table", []))
        self.battle_manager = BattleManager(self.player, enemy)
        self.battle_ui = BattleUI(self.screen, self.battle_manager)
        self.state = GameState.BATTLE

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == GameState.MENU:
                choice = self.menu.handle_event(event)
                if choice == "Nouvelle Partie":
                    self.state = GameState.EXPLORATION
                elif choice == "Charger Partie":
                    if self.save_manager.load_game(self.player, self.equipment_data):
                        self.state = GameState.EXPLORATION
                    else:
                        self.state = GameState.EXPLORATION
                elif choice == "Quitter":
                    self.running = False

            elif self.state == GameState.EXPLORATION:
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP: dy = -1
                    elif event.key == pygame.K_DOWN: dy = 1
                    elif event.key == pygame.K_LEFT: dx = -1
                    elif event.key == pygame.K_RIGHT: dx = 1
                    elif event.key == pygame.K_i: self.state = GameState.INVENTORY_MENU
                    elif event.key == pygame.K_e: self.state = GameState.EQUIPMENT_MENU
                    elif event.key == pygame.K_s: self.save_manager.save_game(self.player)

                    if (dx != 0 or dy != 0) and not self.player.moving:
                        new_x = self.player.grid_x + dx
                        new_y = self.player.grid_y + dy
                        
                        if CollisionSystem.can_move_to(new_x, new_y, self.game_map):
                            self.player.move(dx, dy)
                            
                            # Vérifier téléportation
                            if self.game_map.check_teleport(new_x, new_y):
                                if "map1" in self.current_map_file:
                                    self.change_map('data/maps/map2.json')
                                elif "map2" in self.current_map_file:
                                    self.change_map('data/maps/map3.json')
                                elif "map3" in self.current_map_file:
                                    self.change_map('data/maps/map4.json')
                                elif "map4" in self.current_map_file:
                                    self.change_map('data/maps/map5.json')
                            
                            # Vérifier boutique
                            if self.game_map.check_shop(new_x, new_y):
                                self.state = GameState.SHOP_MENU
                            
                            # Vérifier rencontre
                            tile = self.game_map.get_tile(self.player.grid_x, self.player.grid_y)
                            if tile and tile.type == TileType.GRASS:
                                if random.random() <= self.game_map.encounter_rate:
                                    self.start_battle()
                            
                            # Boss final si Map 5 et condition spéciale (ex: spawn point atteint)
                            if "map5" in self.current_map_file and new_x == 7 and new_y == 1:
                                self.start_battle(boss_id="boss_final")

            elif self.state == GameState.BATTLE:
                action = self.battle_ui.handle_event(event)
                if action == "Attaquer":
                    self.battle_manager.player_attack()
                elif action == "Potion":
                    self.battle_manager.player_use_potion()
                elif action == "Fuite":
                    self.state = GameState.EXPLORATION
                
                if self.battle_manager.is_finished:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.battle_manager.winner == "player":
                            # Argent gagné en combat
                            self.player.money += random.randint(10, 30)
                            loot = LootSystem.generate_loot(self.battle_manager.enemy, self.equipment_data)
                            if loot:
                                self.player.add_to_inventory(loot)
                            self.player.potions += LootSystem.generate_potion()
                            self.state = GameState.EXPLORATION
                        else:
                            # Roguelite: Retour au début
                            self.player.stats.current_hp = self.player.get_active_stats()["max_hp"]
                            self.change_map('data/maps/map1.json')

            elif self.state == GameState.INVENTORY_MENU:
                res = self.inventory_menu.handle_event(event)
                if res == "close": self.state = GameState.EXPLORATION

            elif self.state == GameState.EQUIPMENT_MENU:
                res = self.equipment_menu.handle_event(event)
                if res == "close": self.state = GameState.EXPLORATION
                
            elif self.state == GameState.SHOP_MENU:
                res = self.shop_menu.handle_event(event)
                if res == "close": self.state = GameState.EXPLORATION

    def update(self):
        if self.state == GameState.EXPLORATION:
            self.player.update()
        elif self.state == GameState.BATTLE:
            if self.bm_turn == "enemy" and not self.battle_manager.is_finished:
                pygame.time.delay(500)
                self.battle_manager.enemy_turn()

    @property
    def bm_turn(self):
        return self.battle_manager.turn if hasattr(self, 'battle_manager') else None

    def draw(self):
        self.screen.fill(WHITE)
        
        if self.state == GameState.MENU:
            self.menu.draw()
        elif self.state == GameState.EXPLORATION:
            self.game_map.draw(self.screen)
            self.player.draw(self.screen)
            stats = self.player.get_active_stats()
            draw_text(self.screen, f"Carte: {self.game_map.map_name}", 18, 10, 10)
            draw_text(self.screen, f"HP: {self.player.stats.current_hp}/{stats['max_hp']} | $: {self.player.money}", 20, 10, 35)
            draw_text(self.screen, "I: Inventaire | E: Équipement | S: Sauvegarder", 18, 10, SCREEN_HEIGHT - 25)
        elif self.state == GameState.BATTLE:
            self.battle_ui.draw()
        elif self.state == GameState.INVENTORY_MENU:
            self.game_map.draw(self.screen)
            self.inventory_menu.draw()
        elif self.state == GameState.EQUIPMENT_MENU:
            self.game_map.draw(self.screen)
            self.equipment_menu.draw()
        elif self.state == GameState.SHOP_MENU:
            self.game_map.draw(self.screen)
            self.shop_menu.draw()

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
