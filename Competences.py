from abc import ABC, abstractmethod
import numpy as np
from Effects import *
from utils import draw_text
from Constantes import HEIGHT
import pygame

class Competence(ABC):
    def __init__(self, nom, puissance, portee, aoe_radius, effet=None):
        self.nom = nom
        self.puissance = puissance
        self.portee = portee
        self.aoe_radius = aoe_radius  # Area of effect radius
        self.effet = effet

    @abstractmethod
    def use(self, utilisateur, cible, screen):
        pass

    def crit_check(self, utilisateur):
        return np.random.choice([True, False], p=[utilisateur.crit, 1-utilisateur.crit])

    def dodge_check(self, cible):
        return np.random.choice([True, False], p=[cible.dodge, 1-cible.dodge])

    def display_message(self, screen, text):
        draw_text(screen, text, (10, HEIGHT + 10))  # Adjust position as needed
        pygame.display.flip()

class TirArc(Competence):
    def __init__(self):
        super().__init__("Tir à l'arc", 15, 10, 1)

    def use(self, utilisateur, cible, screen):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                dmg = (utilisateur.attack_power + self.puissance) * 2
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = utilisateur.attack_power + self.puissance
                self.display_message(screen, f"Dégâts infligés: {dmg}")
            if cible.health <= dmg:
                cible.health = 0
            else:
                cible.health -= dmg
            return True

class FlecheEmpoisonnee(Competence):
    def __init__(self):
        super().__init__("Flèche empoisonnée", 10, 10, 1, Poison())

    def use(self, utilisateur, cible, screen):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                dmg = (utilisateur.attack_power + self.puissance) * 2
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = utilisateur.attack_power + self.puissance
                self.display_message(screen, f"Dégâts infligés: {dmg}")
            if cible.health <= dmg:
                cible.health = 0
            else:
                cible.health -= dmg
            cible.effect_status = self.effet
            return True

class BouleDeFeu(Competence):
    def __init__(self):
        super().__init__("Boule de feu", 25, 5, 3, Feu())

    def use(self, utilisateur, cible, screen):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                dmg = (utilisateur.attack_power + self.puissance) * 2
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = utilisateur.attack_power + self.puissance
                self.display_message(screen, f"Dégâts infligés: {dmg}")
            if cible.health <= dmg:
                cible.health = 0
            else:
                cible.health -= dmg
            cible.effect_status = self.effet
            return True

class CoupDEpee(Competence):
    def __init__(self):
        super().__init__("Coup d'épée", 25, 1, 1)

    def use(self, utilisateur, cible, screen):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                dmg = (utilisateur.attack_power + self.puissance) * 2
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = utilisateur.attack_power + self.puissance
                self.display_message(screen, f"Dégâts infligés: {dmg}")
            if cible.health <= dmg:
                cible.health = 0
            else:
                cible.health -= dmg
            return True

class CoupDeBouclier(Competence):
    def __init__(self):
        super().__init__("Coup de bouclier", 10, 1, 1)

    def use(self, utilisateur, cible, screen):
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                dmg = (utilisateur.attack_power + self.puissance) * 2
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = utilisateur.attack_power + self.puissance
                self.display_message(screen, f"Dégâts infligés: {dmg}")
            if cible.health <= dmg:
                cible.health = 0
            else:
                cible.health -= dmg

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

            return True
