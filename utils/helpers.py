import pygame
import json
import os

def load_image(path, scale=None):
    """Charge une image et la redimensionne si nécessaire."""
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Impossible de charger l'image {path}: {e}")
        # Retourne une surface colorée par défaut en cas d'erreur
        surf = pygame.Surface(scale if scale else (32, 32))
        surf.fill((255, 0, 255))
        return surf

def load_json(path):
    """Charge un fichier JSON en toute sécurité."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_json(path, data):
    """Sauvegarde des données dans un fichier JSON."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False

def draw_text(surface, text, size, x, y, color=(0, 0, 0), center=False):
    """Affiche du texte sur une surface."""
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
