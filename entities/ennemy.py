from entities.car import Car

class Ennemy(Car):
    """Représente un ennemi rencontré en combat."""
    
    def __init__(self, name, base_stats, level=1):
        super().__init__(name, base_stats)
        self.level = level
       
        
    def get_loot_chance(self):
        """Retourne la probabilité de drop un équipement."""
        return 0.75 
