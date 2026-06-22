import json
import os
from utils.helpers import load_json, save_json
from equipment.equipment import Equipment

class SaveManager:
    """Gère la persistance des données du joueur (Roguelite)."""
    
    def __init__(self, file_path="save/save.json"):
        self.file_path = file_path

    def save_game(self, player):
        """Sauvegarde l'équipement et les potions du joueur."""
        data = {
            "name": player.name,
            "potions": player.potions,
            "equipments": {slot: (eq.id if eq else None) for slot, eq in player.equipments.items()},
            "inventory": [eq.id for eq in player.inventory]
        }
        return save_json(self.file_path, data)

    def load_game(self, player, equipment_data):
        """Charge l'équipement et les potions sauvegardés."""
        data = load_json(self.file_path)
        if not data:
            return False
            
        player.potions = data.get("potions", 0)
        
        # Recharger l'équipement porté
        saved_equipments = data.get("equipments", {})
        for slot, eq_id in saved_equipments.items():
            if eq_id and eq_id in equipment_data:
                player.equip(Equipment(eq_id, equipment_data[eq_id]))
                
        # Recharger l'inventaire
        saved_inventory = data.get("inventory", [])
        player.inventory = []
        for eq_id in saved_inventory:
            if eq_id in equipment_data:
                player.add_to_inventory(Equipment(eq_id, equipment_data[eq_id]))
                
        return True
