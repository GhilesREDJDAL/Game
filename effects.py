from abc import ABC

# Classe abstraite mère pour les effets
class Effect(ABC):
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def apply(self, unit):
        pass

# Classe pour l'effet de poison
class Poison(Effect):
    def __init__(self):
        super().__init__("Poison", 3)

    def apply(self, unit):
        unit.health -= 1

# Classe pour l'effet de feu
class Feu(Effect):
    def __init__(self):
        super().__init__("Feu", 2)

    def apply(self, unit):
        unit.health -= 2
