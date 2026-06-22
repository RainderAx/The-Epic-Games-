from equipment.equipment import Equipment

class Tires(Equipment):
    def __init__(self, equip_id, data):
        data["slot"] = "tires"
        super().__init__(equip_id, data)
