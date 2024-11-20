import pygame
import random
from abc import ABC, abstractmethod
# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit():
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, defense_power, speed, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.__x = x
        self.__y = y
        self.__health = health
        self.attack_power = attack_power
        self.defense_power = defense_power
        self.speed = speed
        self.critical_rate = 1
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.effect_status = None

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    @abstractmethod
    def use_skill(self, target, skill):
        pass
    
    def take_damage(self, damage):
        self.health -= damage

    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, valeur):
        if valeur >= 0 and isinstance(valeur, int):
            self.__x = valeur
        else:
            raise TypeError(f"La valeur doit être un entier compris entre 0 et {GRID_SIZE} ")
            
    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, valeur):
        if valeur >= 0 and isinstance(valeur, int):
            self.__health = valeur
        else:
            raise TypeError(f"La valeur doit être un entier compris entre 0 et {GRID_SIZE} ")

    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, valeur):
        if valeur >= 0 and isinstance(valeur, int):
            self.__y = valeur
        else:
            raise TypeError(f"La valeur doit être un entier compris entre 0 et {GRID_SIZE} ")    
   
class Archer(Unit):
    def __init__(self, x, y, team):
        super().__init__(self, x, y, health = 100, attack_power = 100, 
                         defense_power = 50, speed = 125, team = team)
        self.type = "Ranged"
        self.skills = [{"Skill name": "Tir à l'arc", "Power": 15, "Range": 10, "Effect": None},
                       {"Skill name": "Flèche empoisonnée", "Power": 10, "Range": 10, "Effect": "Poison"}
                       ]
    def use_skill(self, target, skill):
        if skill in self.skills:
            if abs(self.x - target.x) <= skill["Range"] and abs(self.y - target.y) <= skill["Range"]:
                target.health -= (self.attack_power + skill["Power"])
            if skill["Effect"] != None:
                target.effect_status = skill["Effect"]
class Sorcier(Unit):
    def __init__(self, x, y, team):
        super().__init__(self, x, y, health = 75, attack_power = 100, 
                         defense_power = 75, speed = 75, team = team)
        self.type = "Ranged"
        self.skills = [{"Skill name": "Boule de feu", "Power": 25, "Range": 5, "Effect": "Burn"},
                       {"Skill name": "Gèle", "Power": 0, "Range": 0, "Effect": "Freeze"}
                       ]
    def use_skill(self, target, skill):
        if skill in self.skills:
            if abs(self.x - target.x) <= skill["Range"] and abs(self.y - target.y) <= skill["Range"]:
                target.health -= (self.attack_power + skill["Power"])
            if skill["Effect"] != None:
                target.effect_status = skill["Effect"]
class Guerrier(Unit):
    def __init__(self, x, y, team):
        super().__init__(self, x = x, y = x, health = 150, attack_power = 100, 
                         defense_power = 100, speed = 20, team = team)
        self.type = "Physical"
        self.skills = [{"Skill name": "Coup d'épée", "Power": 25, "Range": 1, "Effect": None},
                       {"Skill name": "Coup de bouclier", "Power": 10, "Range": 1, "Effect": "Pushback"}
                       ]
    def use_skill(self, target, skill):
        if skill in self.skills:
            if abs(self.x - target.x) <= skill["Range"] and abs(self.y - target.y) <= skill["Range"]:
                target.health -= (self.attack_power + skill["Power"])
            if skill["Effect"] != None:
                target.effect_status = skill["Effect"]
