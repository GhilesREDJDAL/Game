import pygame
import random
from abc import ABC, abstractmethod
from Competences import *
from Constantes import CELL_SIZE, RED, BLUE, GREEN, GRID_SIZE

# On charge les images utilisées pour les unités
player_archer = pygame.image.load('images/player_archer.png')
player_knight = pygame.image.load('images/player_knight.png')
player_mage = pygame.image.load('images/player_mage.png')
enemy_archer = pygame.image.load('images/enemy_archer.png')
enemy_knight = pygame.image.load('images/enemy_knight.png')
enemy_mage = pygame.image.load('images/enemy_mage.png')

# On met les images à la bonne échelle.
player_archer = pygame.transform.scale(player_archer, (CELL_SIZE*0.9, CELL_SIZE*0.9))
player_knight = pygame.transform.scale(player_knight, (CELL_SIZE*0.9, CELL_SIZE*0.9))
player_mage = pygame.transform.scale(player_mage, (CELL_SIZE*0.9, CELL_SIZE*0.9))
enemy_archer = pygame.transform.scale(enemy_archer, (CELL_SIZE*0.9, CELL_SIZE*0.9))
enemy_knight = pygame.transform.scale(enemy_knight, (CELL_SIZE*0.9, CELL_SIZE*0.9))
enemy_mage = pygame.transform.scale(enemy_mage, (CELL_SIZE*0.9, CELL_SIZE*0.9))

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

    def __init__(self, x, y, health, attack_power, defense_power, speed, crit, dodge, team):
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
        self.crit = crit
        self.dodge = dodge
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.effect_status = None #Deprec?
        self.item = None

    def move(self, dx, dy, obstacles, water_zones, units_list, screen):
        """Déplace l'unité de dx, dy en vérifiant les obstacles et les zones d'eau."""
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in [(obs.x, obs.y) for obs in obstacles]:
            for unit in units_list:
                if new_x == unit.x and new_y == unit.y:
                    return False
            self.x = new_x
            self.y = new_y
            if (self.x, self.y) in [(water.x, water.y) for water in water_zones]:
                draw_text(screen, f"L'unité de l'équipe {self.team} est tombée dans l'eau à ({self.x}, {self.y}) et est morte !", (10, HEIGHT + 10))
                pygame.display.flip()
                pygame.time.wait(1000)  # Attendre 2 secondes pour que le message soit visible
                self.health = 0  # L'unité meurt
            return True
        return False

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.take_damage(self, (self.attack_power - target.defense_power))
            print("attako")
    @abstractmethod
    def draw(self, screen):
        """Affiche l'unité sur l'écran."""        
        pass


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
    
    def take_damage(self, dmg_dealer, damage):
        dmg = self.weakness_rotation(dmg_dealer, damage)
        if isinstance(dmg_dealer, Unit):
            if dmg_dealer.team == self.team:
                dmg = 0
        self.health = int(max(0, self.health - dmg))
        return True

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
            if self.__health >= self.max_health:
                self.__health = self.max_health
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

    def use_skill(self, target, skill, screen, extra_aoelist=None):
        skill.use(self, target, screen, extra_aoelist)
        return True
    
    @abstractmethod
    def weakness_rotation(self, cible, dmg):
        pass
    
class Archer(Unit):
    """
    Classe représentant un archer.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    type : str
        Le type de l'unité (ici, "Ranged").
    skills : list
        La liste des compétences de l'unité.

    Méthodes
    --------
    __init__(x, y, team)
        Initialise les attributs spécifiques de l'unité Archer.
    """

    def __init__(self, x, y, team):
        """
        Initialise les attributs spécifiques de l'unité Archer.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        super().__init__(x, y, 100, 100, 65, 4, 0.1, 0.1, team)
        self.type = "Ranged"
        self.skills = [TirArc(), FlecheEmpoisonnee(), BarrageDeFleches()]

    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        if self.team == 'Joueur' or self.team == 'Equipe 1': 
            screen.blit(player_archer, (self.x * CELL_SIZE + (CELL_SIZE * 0.05),
                                        self.y * CELL_SIZE + (CELL_SIZE * 0.05)))
        else:
            screen.blit(enemy_archer, (self.x * CELL_SIZE + (CELL_SIZE * 0.05),
                                       self.y * CELL_SIZE + (CELL_SIZE * 0.05)))
        self.draw_health_bar(screen)
        
    def weakness_rotation(self, dmg_dealer, dmg):
        if isinstance(dmg_dealer, Sorcier):
            dmg *= 1.1
        elif isinstance(dmg_dealer, Guerrier):
            dmg *= 0.9
        return dmg
    
class Sorcier(Unit):
    """
    Classe représentant un sorcier.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    type : str
        Le type de l'unité (ici, "Ranged").
    skills : list
        La liste des compétences de l'unité.

    Méthodes
    --------
    __init__(x, y, team)
        Initialise les attributs spécifiques de l'unité Sorcier.
    """

    def __init__(self, x, y, team):
        """
        Initialise les attributs spécifiques de l'unité Sorcier.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        super().__init__(x, y, 75, 100, 75, 3, 0.1, 0.1, team)
        self.type = "Ranged"
        self.skills = [BouleDeFeu(), Teleportation(), ZoneDeSoin()]  # Gele() à ajouter plus tard
    
    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.team == 'Joueur' or self.team == 'Equipe 1': 
            screen.blit(player_mage, (self.x * CELL_SIZE + (CELL_SIZE * 0.05),
                                        self.y * CELL_SIZE + (CELL_SIZE * 0.05)))
        else:
            screen.blit(enemy_mage, (self.x * CELL_SIZE + (CELL_SIZE * 0.05),
                                       self.y * CELL_SIZE + (CELL_SIZE * 0.05)))
        self.draw_health_bar(screen)
    
    def weakness_rotation(self, dmg_dealer, dmg):
        if isinstance(dmg_dealer, Guerrier):
            dmg *= 1.1
        elif isinstance(dmg_dealer, Archer):
            dmg *= 0.9
        return dmg
    
class Guerrier(Unit):
    """
    Classe représentant un guerrier.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    type : str
        Le type de l'unité (ici, "Physical").
    skills : list
        La liste des compétences de l'unité.

    Méthodes
    --------
    __init__(x, y, team)
        Initialise les attributs spécifiques de l'unité Guerrier.
    """

    def __init__(self, x, y, team):
        """
        Initialise les attributs spécifiques de l'unité Guerrier.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        super().__init__(x, y, 150, 100, 80, 3, 0.1, 0.1, team)
        self.type = "Physical"
        self.skills = [CoupDEpee(), CoupDeBouclier(),EpeeDivine()]
    
    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.team == 'Joueur' or self.team == 'Equipe 1': 
            screen.blit(player_knight, (self.x * CELL_SIZE + (CELL_SIZE * 0.05),
                                        self.y * CELL_SIZE + (CELL_SIZE * 0.05)))
        else:
            screen.blit(enemy_knight, (self.x * CELL_SIZE + (CELL_SIZE * 0.05),
                                       self.y * CELL_SIZE + (CELL_SIZE * 0.05)))
        self.draw_health_bar(screen)
    
    def weakness_rotation(self, dmg_dealer, dmg):
        if isinstance(dmg_dealer, Archer):
            dmg *= 1.1
        elif isinstance(dmg_dealer, Sorcier):
            dmg *= 0.9
        return dmg
