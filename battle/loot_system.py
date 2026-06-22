import random
from equipment.equipment import Equipment

class LootSystem:
    """Gère la génération de butin après un combat."""
    
    @staticmethod
    def generate_loot(enemy, equipment_data):
        """
        Génère aléatoirement une pièce d'équipement basée sur les données disponibles.
        """
        if random.random() <= enemy.get_loot_chance():
            # Choisir une pièce au hasard parmi toutes les données d'équipement
            all_ids = list(equipment_data.keys())
            if not all_ids:
                return None
                
            loot_id = random.choice(all_ids)
            return Equipment(loot_id, equipment_data[loot_id])
        return None

    @staticmethod
    def generate_potion():
        """Petite chance de trouver une potion."""
        if random.random() <= 0.3: # 30% de chance
            return 1
        return 0
