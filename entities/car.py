from entities.stats import Stats
from equipment.equipment import Equipment

class Car:
    """Représente une voiture (Joueur ou Ennemi) avec ses stats et son équipement."""
    
    def __init__(self, name: str, base_stats: Stats, sprite_path: str = None):
        self.name = name
        self.stats = base_stats
        self.sprite_path = sprite_path
        
        self.equipments = {
            "engine": None,
            "tires": None,
            "driver": None,
            "turbo": None,
            "body": None,
            "brakes": None,
            "suspension": None
        }

    def equip(self, item: Equipment) -> Equipment:
        """Équipe une pièce et retourne l'ancienne pièce s'il y en avait une."""
        old_item = self.equipments.get(item.slot)
        self.equipments[item.slot] = item
        
        total_stats = self.get_active_stats()
        if self.stats.current_hp > total_stats["max_hp"]:
            self.stats.current_hp = total_stats["max_hp"]
            
        return old_item

    def get_active_stats(self) -> dict:
        """Retourne les stats effectives en combat."""
        return self.stats.get_total_stats(self.equipments)

    def take_damage(self, amount: int):
        self.stats.current_hp = max(0, self.stats.current_hp - amount)

    def is_destroyed(self) -> bool:
        return self.stats.current_hp <= 0
