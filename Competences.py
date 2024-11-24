from abc import ABC, abstractmethod
from Effects import *

class Competence(ABC):
    def __init__(self, nom, puissance, portee, effet=None):
        self.nom = nom
        self.puissance = puissance
        self.portee = portee
        self.effet = effet

    @abstractmethod
    def use(self, utilisateur, cible):
        pass

class TirArc(Competence):
    def __init__(self):
        super().__init__("Tir à l'arc", 15, 10)

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))

class FlecheEmpoisonnee(Competence):
    def __init__(self):
        super().__init__("Flèche empoisonnée", 10, 10, Poison())

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))
            cible.effect_status = self.effet

class BouleDeFeu(Competence):
    def __init__(self):
        super().__init__("Boule de feu", 25, 5, Feu())

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))
            cible.effect_status = self.effet

# To do: effet Gel, pas de mvmt possible pdt #tours
# class Gele(Competence):
#     def __init__(self):
#         super().__init__("Gèle", 0, 5, Gel())

#     def use(self, utilisateur, cible):
#         if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
#             cible.effect_status = self.effet

class CoupDEpee(Competence):
    def __init__(self):
        super().__init__("Coup d'épée", 25, 1)

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))

class CoupDeBouclier(Competence):
    def __init__(self):
        super().__init__("Coup de bouclier", 10, 1)

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))
            dx = cible.x - utilisateur.x
            dy = cible.y - utilisateur.y
            if dx > 0 and cible.x < GRID_SIZE - 1:
                cible.x += 1
            elif dx < 0 and cible.x > 0:
                cible.x -= 1
            if dy > 0 and cible.y < GRID_SIZE - 1:
                cible.y += 1
            elif dy < 0 and cible.y > 0:
                cible.y -= 1
