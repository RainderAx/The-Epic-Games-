import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils.helpers import draw_text

class Menu:
    """Gère l'affichage du menu principal."""
    
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Nouvelle Partie", "Charger Partie", "Quitter"]
        self.selected_index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]
        return None

    def draw(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, "The Epic Games: Car RPG", 48, SCREEN_WIDTH // 2, 100, center=True)
        
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index else BLACK
            draw_text(self.screen, option, 36, SCREEN_WIDTH // 2, 250 + i * 50, color=color, center=True)
