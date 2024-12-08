from abc import ABC, abstractmethod
import numpy as np
from Effects import *
from utils import draw_text
from Constantes import HEIGHT
import pygame

class Competence(ABC):
    """ Classe abstraite mère pour les compétences
    ...
    Attributs
    ---------
    nom: str
        Le nom de la compétence
    puissance : int
        La puissance (dégats infligés) de la compétence
    portee : int
        La portée de la compétence
    aoe_radius : int
        La rayon d'effet de la compétence (si applicable)
    effet : Effect
        Effet associé à la compétence (si applicable)
    
    Méthodes
    --------
    use(utilisateur, cible, screen)
        Utilisation de la compétence et affichage selon les résultats de crit- et dodge_ check.
    crit_check(utilisateur)
        Determine si le cout critique a lieu
    dodge_check(cible)
        Determine si l'esquive a lieu
    display_message(screen, text)
        Affiche un message
    """
    
    def __init__(self, nom, puissance, portee, aoe_radius, effet=None):
        self.nom = nom
        self.puissance = puissance
        self.portee = portee
        self.aoe_radius = aoe_radius  # Area of effect radius
        self.effet = effet

    def use(self, utilisateur, cible, screen):
        """ Utilisation de la compétence """
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                crit_dmg = (utilisateur.attack_power + self.puissance) * 2
                dmg = max(0, crit_dmg - cible.defense_power)
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = max(0, utilisateur.attack_power - cible.defense_power)
                self.display_message(screen, f"Dégâts infligés: {dmg}")

            if cible.health <= dmg:
                cible.health = 0
            else:
                cible.health -= dmg

            if self.effet:
                cible.effect_status = self.effet

            return True
    
    def crit_check(self, utilisateur):
        """ Calcul aléatoire du coup critique, retourne True ou False selon le 
            taux critique de l'unité qui utilise la compétence"""
        return np.random.choice([True, False], p=[utilisateur.crit, 1-utilisateur.crit])

    def dodge_check(self, cible):
        """ Calcul aléatoire de l'evasion, retourne True ou False selon le 
            taux d'évasion de la cible """
        return np.random.choice([True, False], p=[cible.dodge, 1-cible.dodge])

    def display_message(self, screen, text):
        """ Affichage du message coup critique/evasion. """
        draw_text(screen, text, (10, HEIGHT + 10)) 
        pygame.display.flip()

class TirArc(Competence):
    """ Sous fille TirArc de Compétence """
    def __init__(self):
        super().__init__("Tir à l'arc", 15, 10, 1)

class FlecheEmpoisonnee(Competence):
    def __init__(self):
        super().__init__("Flèche empoisonnée", 10, 10, 1, Poison())

class BouleDeFeu(Competence):
    def __init__(self):
        super().__init__("Boule de feu", 25, 5, 3, Feu())

class CoupDEpee(Competence):
    def __init__(self):
        super().__init__("Coup d'épée", 25, 1, 1)

class CoupDeBouclier(Competence):
    def __init__(self):
        super().__init__("Coup de bouclier", 10, 1, 1)

    def use(self, utilisateur, cible, screen):
        """ Surcharge de la méthode d'utilisation de la compétence, adaptée à celle-ci"""
        success = super().use(utilisateur, cible, screen)
        if not success:
            return False
        #Si l'attaque n'a pas été esquivé:
        dx = cible.x - utilisateur.x
        dy = cible.y - utilisateur.y
        #La cible est déplacée d'une case selon l'orientation de l'utilisateur:
        if dx > 0 and cible.x < GRID_SIZE - 1:
            cible.x += 1
        elif dx < 0 and cible.x > 0:
            cible.x -= 1
        if dy > 0 and cible.y < GRID_SIZE - 1:
            cible.y += 1
        elif dy < 0 and cible.y > 0:
            cible.y -= 1
        return True
