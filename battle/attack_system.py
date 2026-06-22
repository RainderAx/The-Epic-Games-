import random

class AttackSystem:
    """Gère la logique de calcul des dégâts et de l'esquive."""
    
    @staticmethod
    def calculate_damage(attacker, defender):
        """
        Calcule les dégâts infligés par l'attaquant au défenseur.
        Formule : degats = attaque_attaquant - defense_cible (min 1)
        """
        attacker_stats = attacker.get_active_stats()
        defender_stats = defender.get_active_stats()
        
        
        dodge_chance = defender_stats.get("dodge", 0)
        if random.randint(1, 100) <= dodge_chance:
            return 0, True
            
        damage = max(1, attacker_stats["attack"] - defender_stats["defense"])
        return damage, False
