class Equipment:
    """Classe de base pour toutes les pièces de la voiture."""
    
    def __init__(self, equip_id: str, data: dict):
        self.id = equip_id
        self.name = data["name"]
        self.slot = data["slot"] # engine, tires, driver, turbo, body, brakes, suspension
        
        bonuses = data.get("bonuses", {})
        self.bonus_hp = bonuses.get("hp", 0)
        self.bonus_attack = bonuses.get("attack", 0)
        self.bonus_defense = bonuses.get("defense", 0)
        self.bonus_dodge = bonuses.get("dodge", 0)

    def __str__(self):
        return f"{self.name} (Atk:{self.bonus_attack}, Def:{self.bonus_defense})"