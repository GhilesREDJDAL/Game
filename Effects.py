from abc import ABC, abstractmethod

class Effect(ABC):
    """
    Classe abstraite pour représenter un effet appliqué aux unités

    ...
    Attributs
    ---------
    name : str
        Le nom de l'effet.
    x : int, optionnel
        La position x de l'effet sur la grille.
    y : int, optionnel
        La position y de l'effet sur la grille.
    effect_duration : int, optionnel
        La durée de l'effet.
    target : Unit, optionnel
        La cible de l'effet.

    Méthodes
    --------
    apply_effect(unit)
        Applique l'effet à une unité (méthode abstraite).
    """

    def __init__(self, name, x=None, y=None, target=None, effect_duration=None):
        """
        Construit un effet avec un nom, des coordonnées optionnelles, une durée et une cible.

        Paramètres
        ----------
        name : str
            Le nom de l'effet.
        x : int, optionnel
            La position x de l'effet sur la grille.
        y : int, optionnel
            La position y de l'effet sur la grille.
        target : Unit, optionnel
            La cible de l'effet.
        effect_duration : int, optionnel
            La durée de l'effet.
        """
        self.name = name
        self.__x = x
        self.__y = y
        self.__effectTTL = effect_duration
        self.__target = target
        
    @property
    def x(self):
        """Obtient la position x de l'effet."""
        return self.__x

    @x.setter
    def x(self, value):
        """Définit la position x de l'effet."""
        self.__x = value

    @property
    def y(self):
        """Obtient la position y de l'effet."""
        return self.__y

    @y.setter
    def y(self, value):
        """Définit la position y de l'effet."""
        self.__y = value
        
    @property
    def effectTTL(self):
        """Obtient la durée de l'effet."""
        return self.__effectTTL

    @effectTTL.setter
    def effectTTL(self, value):
        """Définit la durée de l'effet."""
        self.__effectTTL = value

    @abstractmethod
    def apply_effect(self, unit):
        """Applique l'effet à une unité (méthode abstraite)."""
        pass

    @property
    def target(self):
        """Obtient la cible de l'effet."""
        return self.__target

    @target.setter
    def target(self, value):
        """Définit la cible de l'effet."""
        if isinstance(value, Unit):
            self.__target = value
        else:
            raise TypeError("La cible doit être une unité.")

class Soin(Effect):
    """
    Classe représentant l'effet de soin.

    ...
    Méthodes
    --------
    apply_effect(unit)
        Applique l'effet de soin à une unité.
    """

    def __init__(self):
        """Initialise l'effet de soin avec une durée de 3 tours."""
        super().__init__("Soin", effect_duration=3)
        
    def apply_effect(self, unit):
        """Applique l'effet de soin à une unité."""
        if self.effectTTL > 0:
            unit.take_damage(self, -10)  

class Feu(Effect):
    """
    Classe représentant l'effet de feu.

    ...
    Méthodes
    --------
    apply_effect(unit)
        Applique l'effet de feu à une unité.
    """

    def __init__(self):
        """Initialise l'effet de feu avec une durée de 3 tours."""
        super().__init__("Feu", effect_duration=3)
        
    def apply_effect(self, unit):
        """Applique l'effet de feu à une unité."""
        if self.effectTTL > 0:
            unit.take_damage(self, 15)  

class Poison(Effect):
    """
    Classe représentant l'effet de poison.

    ...
    Méthodes
    --------
    apply_effect(unit)
        Applique l'effet de poison à une unité.
    """

    def __init__(self):
        """Initialise l'effet de poison avec une durée de 3 tours."""
        super().__init__("Poison", effect_duration=2)
        
    def apply_effect(self, unit):
        """Applique l'effet de poison à une unité."""
        if self.effectTTL > 0:
            unit.take_damage(self, 25)
