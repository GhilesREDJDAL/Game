from abc import ABC, abstractmethod
from unit import *

class Case(ABC):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__occupancy = None
        self.__effectTTL = None
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
    def effectTTL(self):
        return self.__effectTTL

    @effectTTL.setter
    def effectTTL(self, value):
        self.__effectTTL = value
        
    def efffect_countdown(self):
        if self.__effectTTL is not None:
            self.__effectTTL -= 1
            if self.__effectTTL <= 0:
                return True  
        return False
    
class Mur(Case):
    def is_traversable(self):
        return False

    def apply_effect(self, unit):
        pass  


class Eau(Case):
    def is_traversable(self):
        """Only traversable for flying units"""
        return True

    def apply_effect(self, unit):
        pass  

class Soin(Case):
    def __init__(self, x, y, effect_duration):
        super().__init__(x, y)
        self.__effectTTL = effect_duration

    def is_traversable(self):
        return True

    def apply_effect(self, unit):
        if self.__effectTTL > 0:
            unit.health += 10  # Healing effect

class Feu(Case):
    def __init__(self, x, y, effect_duration):
        super().__init__(x, y)
        self.__effectTTL = effect_duration

    def is_traversable(self):
        return True

    def apply_effect(self, unit):
        if self.__effectTTL > 0:
            unit.health -= 15  # Fire damage
