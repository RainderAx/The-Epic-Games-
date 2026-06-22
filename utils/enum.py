from enum import Enum, auto

class EquipmentSlot(Enum):
    ENGINE = "engine"
    TIRES = "tires"
    DRIVER = "driver"
    TURBO = "turbo"
    BODY = "body"
    BRAKES = "brakes"
    SUSPENSION = "suspension"

class TileType(Enum):
    ROAD = "road"
    GRASS = "grass"
    OBSTACLE = "obstacle"
    NPC = "npc"

class GameState(Enum):
    EXPLORATION = auto()
    BATTLE = auto()
    MENU = auto()
    EQUIPMENT_MENU = auto()
    INVENTORY_MENU = auto()
    GAME_OVER = auto()
