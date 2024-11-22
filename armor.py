# armor.py

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

    def get_defense(self):
        return self.defense

    def get_name(self):
        return self.name