from equipment.equipment import Equipment

class Driver(Equipment):
    def __init__(self, equip_id, data):
        data["slot"] = "driver"
        super().__init__(equip_id, data)
