from abc import ABC, abstractmethod

class Effect(ABC):
    def __init__(self, name, x=None, y=None, target=None, effect_duration=None):
        self.name = name
        self.__x = x
        self.__y = y
        self.__effectTTL = effect_duration
        self.__target = target
        
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
    def effectTTL(self):
        return self.__effectTTL

    @effectTTL.setter
    def effectTTL(self, value):
        self.__effectTTL = value

    @abstractmethod
    def apply_effect(self, unit):
        pass

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if isinstance(value, Unit) or isinstance(value, Case):
            self.__target = value
        else:
            raise TypeError("Target has to be a unit or a case.")

class Soin(Effect):
    def __init__(self): 
        super().__init__("Soin", effect_duration=3)
        
    def apply_effect(self, unit):
        if self.effectTTL > 0:
            unit.health += 10  

class Feu(Effect):
    def __init__(self): 
        super().__init__("Feu", effect_duration=3)
        
    def apply_effect(self, unit):
        if self.effectTTL > 0:
            unit.health = max(0, unit.health - 15)  

class Poison(Effect):
    def __init__(self): 
        super().__init__("Poison", effect_duration=3)
        
    def apply_effect(self, unit):
        if self.effectTTL > 0:
            unit.health = max(0, unit.health - 25)
