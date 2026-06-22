from equipment.equipment import Equipment

class Turbo(Equipment):
    def __init__(self, equip_id, data):
        data["slot"] = "turbo"
        super().__init__(equip_id, data)
