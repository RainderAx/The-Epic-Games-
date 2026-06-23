import pygame
import os
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils.helpers import draw_text

class BattleUI:
    """Gère l'affichage des combats avec les assets graphiques."""
    
    def __init__(self, screen, battle_manager):
        self.screen = screen
        self.bm = battle_manager
        self.options = ["Attaquer", "Potion", "Fuite"]
        self.selected_index = 0
        
        # Chargement du background
        self.background = None
        bg_path = "assets/ui/battle_background.png"
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
        # Chargement des sprites des combattants
        self.player_sprite = self.load_sprite(self.bm.player.sprite_path, (200, 200))
        self.enemy_sprite = self.load_sprite(self.bm.enemy.sprite_path, (200, 200))

    def load_sprite(self, path, size):
        if path and os.path.exists(path):
            sprite = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(sprite, size)
        return None

    def handle_event(self, event):
        if self.bm.turn == "player" and not self.bm.is_finished:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_RIGHT:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_index]
        return None

    def draw(self):
        # Fond de combat
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((200, 200, 255))
        
        # Affichage des sprites
        # Le joueur est en bas à gauche (vue de dos/côté)
        if self.player_sprite:
            self.screen.blit(self.player_sprite, (50, 200))
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), (50, 200, 150, 100))
            
        # L'ennemi est en haut à droite
        if self.enemy_sprite:
            self.screen.blit(self.enemy_sprite, (400, 50))
        else:
            pygame.draw.rect(self.screen, (255, 0, 0), (400, 50, 150, 100))

        # Interface (Stats et Log)
        # Panneau de stats joueur (en bas à droite)
        pygame.draw.rect(self.screen, (240, 240, 240), (400, 280, 220, 100), border_radius=10)
        pygame.draw.rect(self.screen, BLACK, (400, 280, 220, 100), 2, border_radius=10)
        p_stats = self.bm.player.get_active_stats()
        draw_text(self.screen, f"{self.bm.player.name}", 20, 415, 290, color=BLACK)
        draw_text(self.screen, f"HP: {self.bm.player.stats.current_hp}/{p_stats['max_hp']}", 18, 415, 320, color=BLACK)
        
        # Panneau de stats ennemi (en haut à gauche)
        pygame.draw.rect(self.screen, (240, 240, 240), (20, 20, 220, 100), border_radius=10)
        pygame.draw.rect(self.screen, BLACK, (20, 20, 220, 100), 2, border_radius=10)
        e_stats = self.bm.enemy.get_active_stats()
        draw_text(self.screen, f"{self.bm.enemy.name}", 20, 35, 30, color=BLACK)
        draw_text(self.screen, f"HP: {self.bm.enemy.stats.current_hp}/{e_stats['max_hp']}", 18, 35, 60, color=BLACK)
        
        # Log de combat (au milieu)
        y_offset = 150
        for msg in self.bm.battle_log[-3:]:
            # Petit fond semi-transparent pour le texte
            text_surface = pygame.Surface((SCREEN_WIDTH - 100, 30), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, 180))
            self.screen.blit(text_surface, (50, y_offset - 5))
            draw_text(self.screen, msg, 18, SCREEN_WIDTH // 2, y_offset, center=True, color=BLACK)
            y_offset += 35
            
        # Menu d'actions (en bas)
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 380, SCREEN_WIDTH, 100))
        pygame.draw.line(self.screen, BLACK, (0, 380), (SCREEN_WIDTH, 380), 2)
        
        if not self.bm.is_finished:
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected_index else BLACK
                # Petit indicateur pour la sélection
                if i == self.selected_index:
                    draw_text(self.screen, ">", 24, 80 + i * 200, 420, color=color)
                draw_text(self.screen, option, 24, 100 + i * 200, 420, color=color)
        else:
            draw_text(self.screen, "Appuyez sur Entrée pour continuer", 24, SCREEN_WIDTH // 2, 420, center=True, color=BLACK)
