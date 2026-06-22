import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils.helpers import draw_text

class BattleUI:
    """Gère l'affichage des combats."""
    
    def __init__(self, screen, battle_manager):
        self.screen = screen
        self.bm = battle_manager
        self.options = ["Attaquer", "Potion", "Fuite"]
        self.selected_index = 0

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
        self.screen.fill((200, 200, 255))
        
        # Stats Joueur
        p_stats = self.bm.player.get_active_stats()
        draw_text(self.screen, f"{self.bm.player.name}", 24, 50, 300)
        draw_text(self.screen, f"HP: {self.bm.player.stats.current_hp}/{p_stats['max_hp']}", 20, 50, 330)
        
        # Stats Ennemi
        e_stats = self.bm.enemy.get_active_stats()
        draw_text(self.screen, f"{self.bm.enemy.name}", 24, 450, 50)
        draw_text(self.screen, f"HP: {self.bm.enemy.stats.current_hp}/{e_stats['max_hp']}", 20, 450, 80)
        
        # Log de combat
        y_offset = 150
        for msg in self.bm.battle_log[-5:]:
            draw_text(self.screen, msg, 18, SCREEN_WIDTH // 2, y_offset, center=True)
            y_offset += 25
            
        # Menu d'actions
        if not self.bm.is_finished:
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected_index else BLACK
                draw_text(self.screen, option, 24, 100 + i * 150, 420, color=color)
        else:
            draw_text(self.screen, "Appuyez sur Entrée pour continuer", 24, SCREEN_WIDTH // 2, 420, center=True)
