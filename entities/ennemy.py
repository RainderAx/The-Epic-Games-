from entities.car import Car

class Ennemy(Car):
    """Représente un ennemi rencontré en combat."""
    
    def __init__(self, name, base_stats, sprite_path=None, level=1, loot_table=None):
        super().__init__(name, base_stats, sprite_path)
        self.level = level
        # On enregistre la liste des équipements que cet ennemi spécifique peut faire tomber
        self.loot_table = loot_table if loot_table is not None else []
       
    def get_loot_chance(self):
        """Retourne la probabilité de drop un équipement."""
        return 0.75
