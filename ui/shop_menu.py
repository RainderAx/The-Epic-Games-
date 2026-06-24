import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils.helpers import draw_text
from equipment.equipment import Equipment

class ShopMenu:
    """Gère l'interface de la boutique."""
    
    def __init__(self, screen, player, equipment_data):
        self.screen = screen
        self.player = player
        self.equipment_data = equipment_data
        self.selected_index = 0
        self.mode = "buy" # "buy" ou "sell"
        
        # Liste d'objets à vendre (aléatoire ou fixe)
        self.shop_items = list(equipment_data.keys())[:5]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.mode = "sell" if self.mode == "buy" else "buy"
                self.selected_index = 0
            elif event.key == pygame.K_UP:
                limit = len(self.shop_items) if self.mode == "buy" else len(self.player.inventory)
                if limit > 0:
                    self.selected_index = (self.selected_index - 1) % limit
            elif event.key == pygame.K_DOWN:
                limit = len(self.shop_items) if self.mode == "buy" else len(self.player.inventory)
                if limit > 0:
                    self.selected_index = (self.selected_index + 1) % limit
            elif event.key == pygame.K_RETURN:
                if self.mode == "buy":
                    self.buy_item()
                else:
                    self.sell_item()
            elif event.key == pygame.K_ESCAPE:
                return "close"
        return None

    def buy_item(self):
        if not self.shop_items: return
        item_id = self.shop_items[self.selected_index]
        item_data = self.equipment_data[item_id]
        price = 50 # Prix fixe pour l'exemple
        
        if self.player.money >= price:
            self.player.money -= price
            new_item = Equipment(item_id, item_data)
            self.player.add_to_inventory(new_item)
            print(f"Acheté : {new_item.name}")

    def sell_item(self):
        if not self.player.inventory: return
        item = self.player.inventory.pop(self.selected_index)
        sell_price = 25 # Prix de vente fixe
        self.player.money += sell_price
        self.selected_index = max(0, self.selected_index - 1)
        print(f"Vendu : {item.name}")

    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        title = "BOUTIQUE - ACHAT" if self.mode == "buy" else "BOUTIQUE - VENTE"
        draw_text(self.screen, title, 36, SCREEN_WIDTH // 2, 50, color=WHITE, center=True)
        draw_text(self.screen, f"Argent: {self.player.money} $", 24, 50, 50, color=(0, 255, 0))
        draw_text(self.screen, "[TAB] Changer Mode | [ESC] Quitter", 18, SCREEN_WIDTH // 2, 450, color=WHITE, center=True)
        
        items_to_draw = self.shop_items if self.mode == "buy" else [f"{i.name} ({i.slot})" for i in self.player.inventory]
        
        if not items_to_draw:
            draw_text(self.screen, "Rien ici...", 24, SCREEN_WIDTH // 2, 200, color=WHITE, center=True)
        else:
            for i, item_name in enumerate(items_to_draw):
                color = (255, 255, 0) if i == self.selected_index else WHITE
                name = item_name if self.mode == "sell" else self.equipment_data[item_name]["name"]
                price = "50$" if self.mode == "buy" else "25$"
                draw_text(self.screen, f"{name} - {price}", 24, 100, 120 + i * 35, color=color)
