from abc import ABC, abstractmethod
from Effects import *

class Competence(ABC):
    def __init__(self, nom, puissance, portee, aoe_radius, effet=None):
        self.nom = nom
        self.puissance = puissance
        self.portee = portee
        self.aoe_radius = aoe_radius  # Area of effect radius
        self.effet = effet

    @abstractmethod
    def use(self, utilisateur, cible):
        pass

class TirArc(Competence):
    def __init__(self):
        super().__init__("Tir à l'arc", 15, 10, 1)

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))

class FlecheEmpoisonnee(Competence):
    def __init__(self):
        super().__init__("Flèche empoisonnée", 10, 10, 1, Poison())

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))
            cible.effect_status = self.effet

class BouleDeFeu(Competence):
    def __init__(self):
        super().__init__("Boule de feu", 25, 5, 3, Feu())  # Corrected to pass 3 as positional argument

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
        super().__init__("Coup d'épée", 25, 1, 1)

    def use(self, utilisateur, cible):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            cible.health = max(0, cible.health - (utilisateur.attack_power + self.puissance))

class CoupDeBouclier(Competence):
    def __init__(self):
        super().__init__("Coup de bouclier", 10, 1, 1)

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
class Heal(Competence):
    def __init__(self):
        
        super().__init__("Soin", 20, 5, 1)  
    def use(self, utilisateur, cible):
        """
        Heals the target unit if within range, without exceeding their maximum health.

        Parameters:
        utilisateur: Unit
            The unit using the heal ability.
        cible: Unit
            The unit being healed.
        """
        # Check if the target is within the healing range
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            # Heal the target without exceeding their max health
            cible.health = min(cible.max_health, cible.health + self.puissance)
            print(f"{utilisateur.team} heals {cible.team} unit for {self.puissance} health.")
        else:
            print("Target out of range for healing.")
