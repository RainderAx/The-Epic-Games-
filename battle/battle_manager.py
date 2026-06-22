from battle.attack_system import AttackSystem
import random

class BattleManager:
    """Gère le déroulement d'un combat au tour par tour."""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = "player" # Le joueur commence par défaut
        self.battle_log = []
        self.is_finished = False
        self.winner = None

    def player_attack(self):
        if self.turn != "player" or self.is_finished:
            return
            
        damage, dodged = AttackSystem.calculate_damage(self.player, self.enemy)
        if dodged:
            self.battle_log.append(f"{self.enemy.name} a esquivé l'attaque !")
        else:
            self.enemy.take_damage(damage)
            self.battle_log.append(f"{self.player.name} inflige {damage} dégâts à {self.enemy.name}")
            
        self.check_battle_status()
        if not self.is_finished:
            self.turn = "enemy"

    def player_use_potion(self):
        if self.turn != "player" or self.is_finished:
            return
            
        if self.player.use_potion():
            self.battle_log.append(f"{self.player.name} utilise une potion et récupère des PV")
            self.turn = "enemy"
        else:
            self.battle_log.append("Pas de potions disponibles !")

    def enemy_turn(self):
        if self.turn != "enemy" or self.is_finished:
            return
            
        damage, dodged = AttackSystem.calculate_damage(self.enemy, self.player)
        if dodged:
            self.battle_log.append(f"{self.player.name} a esquivé l'attaque !")
        else:
            self.player.take_damage(damage)
            self.battle_log.append(f"{self.enemy.name} inflige {damage} dégâts à {self.player.name}")
            
        self.check_battle_status()
        if not self.is_finished:
            self.turn = "player"

    def check_battle_status(self):
        if self.enemy.is_destroyed():
            self.is_finished = True
            self.winner = "player"
            self.battle_log.append(f"{self.enemy.name} est K.O. ! Victoire !")
        elif self.player.is_destroyed():
            self.is_finished = True
            self.winner = "enemy"
            self.battle_log.append(f"{self.player.name} est K.O. ! Défaite...")
