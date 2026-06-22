class Stats:
    """Gère les statistiques de base et calcule les statistiques totales avec équipement."""
    
    def __init__(self, hp: int, attack: int, defense: int, dodge: int):
        self.base_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_dodge = dodge
        
        # Les stats actuelles (modifiées par les combats ou l'équipement)
        self.current_hp = hp

    def get_total_stats(self, equipments: dict) -> dict:
        """Calcule les stats totales en additionnant les bonus/malus des équipements."""
        total_hp = self.base_hp
        total_attack = self.base_attack
        total_defense = self.base_defense
        total_dodge = self.base_dodge

        for eq in equipments.values():
            if eq:
                total_hp += eq.bonus_hp
                total_attack += eq.bonus_attack
                total_defense += eq.bonus_defense
                total_dodge += eq.bonus_dodge

        return {
            "max_hp": max(1, total_hp), # Empêche d'avoir des PV max négatifs ou nuls
            "attack": max(0, total_attack),
            "defense": max(0, total_defense),
            "dodge": max(0, total_dodge)
        }