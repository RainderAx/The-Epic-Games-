import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils.helpers import draw_text

class InventoryMenu:
    """Gère l'inventaire des pièces récupérées."""
    
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.selected_index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.player.inventory:
                if event.key == pygame.K_ESCAPE: return "close"
                return None
                
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.player.inventory)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.player.inventory)
            elif event.key == pygame.K_RETURN:
                # Équiper l'objet sélectionné
                item = self.player.inventory.pop(self.selected_index)
                old_item = self.player.equip(item)
                if old_item:
                    self.player.add_to_inventory(old_item)
                self.selected_index = 0
                return "equipped"
            elif event.key == pygame.K_ESCAPE:
                return "close"
        return None

    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        draw_text(self.screen, "Inventaire (Pièces de rechange)", 36, SCREEN_WIDTH // 2, 50, color=WHITE, center=True)
        
        if not self.player.inventory:
            draw_text(self.screen, "L'inventaire est vide", 24, SCREEN_WIDTH // 2, 250, color=WHITE, center=True)
        else:
            for i, item in enumerate(self.player.inventory):
                color = (255, 255, 0) if i == self.selected_index else WHITE
                draw_text(self.screen, f"{item.name} ({item.slot})", 24, 100, 150 + i * 30, color=color)
                
            # Afficher les bonus de l'objet sélectionné
            if self.selected_index < len(self.player.inventory):
                item = self.player.inventory[self.selected_index]
                draw_text(self.screen, "Bonus de la pièce :", 28, 450, 150, color=WHITE)
                draw_text(self.screen, f"ATK: {item.bonus_attack}", 22, 450, 190, color=WHITE)
                draw_text(self.screen, f"DEF: {item.bonus_defense}", 22, 450, 220, color=WHITE)
                draw_text(self.screen, f"HP: {item.bonus_hp}", 22, 450, 250, color=WHITE)
                draw_text(self.screen, f"Dodge: {item.bonus_dodge}", 22, 450, 280, color=WHITE)
