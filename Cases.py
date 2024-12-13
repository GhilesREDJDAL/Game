from abc import ABC, abstractmethod
from unit import *

class Case(ABC):
    """ 
    Classe pour représenter une case
    """
    
    def __init__(self, x, y):
        """
        Construit une case avec une position, des paramètres indiquant si elle est occupée ou affectée par un effet.
    
        Paramètres
        ----------
        x : int
            La position x de la case sur la grille.
        y : int
            La position y de la case sur la grille.
        occupancy : Unit
            La santé de l'unité.
        effect : Effect
            L'effet par lequel la case est affectée.
        isaffected : bool
            Indique si la case est affectée.
        """
        self.__x = x
        self.__y = y
        self.__occupancy = None
        self.__effect = None
        self.__isaffected = False
        
    @abstractmethod
    def is_traversable(self):
        pass

    @abstractmethod
    def apply_effect(self, unit):
        pass

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def occupancy(self):
        return self.__occupancy

    # Setter for occupancy
    @occupancy.setter
    def occupancy(self, unit):
        if isinstance(unit, Unit):
            self.__occupancy = unit
        else: 
            raise TypeError("Value has to be Unit object")
    @property
    def effect(self):
        return self.__effect

    @effect.setter
    def effect(self, value):
        if value is None or isinstance(value, Effect):
            self.__effect = value
            self.__isaffected = True
        else:
            raise TypeError("Value has to be Effect object.")
            
    def apply_effect(self, unit):
        if self.__isaffected:
            self.effect.apply_effect(self.occupancy)
        else:
            pass
        
class Normal(Case):
    def is_traversable(self):
        return True
            
class Obstacle(Case):
    def is_traversable(self):
        return False


class Eau(Case):
    def is_traversable(self):
        return True
