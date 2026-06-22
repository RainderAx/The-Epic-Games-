import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils.helpers import draw_text

class EquipmentMenu:
    """Gère l'équipement des pièces sur la voiture."""
    
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.slots = list(player.equipments.keys())
        self.selected_slot_index = 0
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_slot_index = (self.selected_slot_index - 1) % len(self.slots)
            elif event.key == pygame.K_DOWN:
                self.selected_slot_index = (self.selected_slot_index + 1) % len(self.slots)
            elif event.key == pygame.K_ESCAPE:
                return "close"
        return None

    def draw(self):
        # Overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        draw_text(self.screen, "Équipement de la voiture", 36, SCREEN_WIDTH // 2, 50, color=WHITE, center=True)
        
        for i, slot in enumerate(self.slots):
            eq = self.player.equipments[slot]
            eq_name = eq.name if eq else "Vide"
            color = (255, 255, 0) if i == self.selected_slot_index else WHITE
            
            draw_text(self.screen, f"{slot.capitalize()}: {eq_name}", 24, 100, 150 + i * 40, color=color)
            
        # Afficher les stats actuelles à droite
        stats = self.player.get_active_stats()
        draw_text(self.screen, "Statistiques Totales", 28, 450, 150, color=WHITE)
        draw_text(self.screen, f"PV Max: {stats['max_hp']}", 22, 450, 190, color=WHITE)
        draw_text(self.screen, f"Attaque: {stats['attack']}", 22, 450, 220, color=WHITE)
        draw_text(self.screen, f"Défense: {stats['defense']}", 22, 450, 250, color=WHITE)
        draw_text(self.screen, f"Esquive: {stats['dodge']}%", 22, 450, 280, color=WHITE)
