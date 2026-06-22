from equipment.equipment import Equipment

class Body(Equipment):
    def __init__(self, equip_id, data):
        data["slot"] = "body"
        super().__init__(equip_id, data)
