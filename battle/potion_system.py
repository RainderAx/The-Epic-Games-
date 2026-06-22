class PotionSystem:
    """Gère l'inventaire et l'utilisation des potions."""
    
    @staticmethod
    def use_potion(player):
        """Tente d'utiliser une potion sur le joueur."""
        return player.use_potion()

    @staticmethod
    def add_potions(player, amount):
        """Ajoute des potions au joueur."""
        player.potions += amount
