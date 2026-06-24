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
            try:
                self.background = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                self.background = None
            
        # Chargement des sprites des combattants (200x200 pixels)
        # Utilise .sprite_path ou l'attribut de l'entité contenant le chemin de l'image
        self.player_sprite = self.load_sprite(getattr(self.bm.player, 'sprite_path', None), (200, 200))
        self.enemy_sprite = self.load_sprite(getattr(self.bm.enemy, 'sprite_path', None), (200, 200))

    def load_sprite(self, path, size):
        """Tente de charger une image. En cas d'erreur de format ou fichier introuvable,"""
        """génère un carré de couleur unie pour éviter le crash du jeu."""
        if path and os.path.exists(path):
            try:
                sprite = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(sprite, size)
            except (pygame.error, TypeError) as e:
                print(f"⚠️ Erreur de format ou chargement sur l'image {path} : {e}")
        
        # Fallback : Création d'une surface de secours unie
        fallback_surface = pygame.Surface(size)
        fallback_surface.fill((200, 50, 50)) # Rouge par défaut
        return fallback_surface

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_index == 0:
                    self.bm.player_attack()
                elif self.selected_index == 1:
                    self.bm.player_use_potion()
                elif self.selected_index == 2:
                    # Logique de fuite (à lier avec ton système si présent)
                    self.bm.battle_log.append("Vous tentez de fuir !")

    def draw(self):
        # 1. Rendu du fond de combat
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((240, 240, 240))
            
        # 2. Rendu des sprites des voitures
        if self.player_sprite:
            # Joueur positionné en bas à gauche
            self.screen.blit(self.player_sprite, (80, SCREEN_HEIGHT - 320))
            
        if self.enemy_sprite:
            # Ennemi positionné en haut à droite
            self.screen.blit(self.enemy_sprite, (SCREEN_WIDTH - 280, 50))
            
        # 3. Rendu des barres de vie / Textes de statut
        p_stats = self.bm.player.get_active_stats()
        draw_text(self.screen, f"{self.bm.player.name}", 20, 50, SCREEN_HEIGHT - 360, color=BLACK)
        draw_text(self.screen, f"HP: {self.bm.player.stats.current_hp}/{p_stats['max_hp']}", 18, 50, SCREEN_HEIGHT - 335, color=BLACK)
        
        e_stats = self.bm.enemy.get_active_stats()
        draw_text(self.screen, f"{self.bm.enemy.name}", 20, SCREEN_WIDTH - 250, 260, color=BLACK)
        draw_text(self.screen, f"HP: {self.bm.enemy.stats.current_hp}/{e_stats['max_hp']}", 18, SCREEN_WIDTH - 250, 285, color=BLACK)
        
        # 4. Menu d'actions (Placé au-dessus du journal)
        # Rectangle de fond commençant à Y=380
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 380, SCREEN_WIDTH, 100))
        pygame.draw.line(self.screen, BLACK, (0, 380), (SCREEN_WIDTH, 380), 2)
        
        # Dessin des boutons du menu d'action
        for i, option in enumerate(self.options):
            x_pos = 100 + i * 200
            y_pos = 420
            color = (255, 0, 0) if i == self.selected_index else BLACK
            draw_text(self.screen, option, 22, x_pos, y_pos, color=color)
            
        # 5. Log de combat (Déplacé tout en bas, sous le menu d'actions)
        y_offset = 495
        for msg in self.bm.battle_log[-3:]:
            text_surface = pygame.Surface((SCREEN_WIDTH - 100, 30), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, 180))
            self.screen.blit(text_surface, (50, y_offset - 5))
            draw_text(self.screen, msg, 18, SCREEN_WIDTH // 2, y_offset, center=True, color=BLACK)
            y_offset += 35

    