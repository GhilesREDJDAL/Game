import pygame
import random
from abc import ABC, abstractmethod
from Competences import *
from Constantes import CELL_SIZE, RED, BLUE, GREEN, GRID_SIZE

class Unit(ABC):
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
        self.max_health = health
        self.attack_power = attack_power
        self.defense_power = defense_power
        self.speed = speed
        self.critical_rate = 1
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.effect_status = None

    def move(self, dx, dy, obstacles, water_zones):
        """Déplace l'unité de dx, dy."""
        if (0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE and (self.x + dx, self.y + dy) not in obstacles):
            self.x += dx
            self.y += dy

            if (self.x, self.y) in water_zones:
                print(f"L'unité de l'équipe {self.team} est tombée dans l'eau à ({self.x}, {self.y}) et est morte !")
                self.health = 0

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health = max(0, target.health - self.attack_power)

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if self.health <= 0:
            return

        bar_width = CELL_SIZE - 10
        bar_height = 5
        health_ratio = self.health / self.max_health

        x = self.x * CELL_SIZE + 5
        y = self.y * CELL_SIZE + CELL_SIZE - 10

        pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_ratio, bar_height))

        
    @abstractmethod
    def use_skill(self, target, skill):
        pass
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

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
            raise TypeError("La valeur de la santé doit être un entier positif.")

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
        super().__init__(x, y, 100, 100, 50, 125, team)
        self.type = "Ranged"
        self.skills = [TirArc(), FlecheEmpoisonnee()]

    def use_skill(self, target, skill):
        skill.use(self, target)

class Sorcier(Unit):
    def __init__(self, x, y, team):
        super().__init__(x, y, 75, 100, 75, 75, team)
        self.type = "Ranged"
        self.skills = [BouleDeFeu()] # Gele() à ajouter plus tard

    def use_skill(self, target, skill):
        skill.use(self, target)

class Guerrier(Unit):
    def __init__(self, x, y, team):
        super().__init__(x, y, 150, 100, 100, 20, team)
        self.type = "Physical"
        self.skills = [CoupDEpee(), CoupDeBouclier()]

    def use_skill(self, target, skill):
        skill.use(self, target)
