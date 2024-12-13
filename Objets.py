#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 01:57:08 2024

@author: seb
"""
from abc import ABC, abstractmethod
from Constantes import CELL_SIZE
import pygame

hp_pot = pygame.image.load('images/hp_pot.png')
crit_ring = pygame.image.load('images/crit_ring.png')
dodge_ring = pygame.image.load('images/dodge_ring.png')
speed_ring = pygame.image.load('images/speed_ring.png')


hp_pot = pygame.transform.scale(hp_pot, (CELL_SIZE, CELL_SIZE))
crit_ring = pygame.transform.scale(crit_ring, (CELL_SIZE, CELL_SIZE))
dodge_ring = pygame.transform.scale(dodge_ring, (CELL_SIZE, CELL_SIZE))
speed_ring = pygame.transform.scale(speed_ring, (CELL_SIZE, CELL_SIZE))


class Objet():
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = x
        self.y = y
        self.owner = None
        self.is_owned = False
        
    @abstractmethod
    def use_object(self):
        pass
        
    def draw(self, screen):
        """Affiche l'objet sur l'écran."""      
        pass
            

    
class AnneauCritique(Objet):
    def __init__(self, x, y):
        super().__init__("Anneau Critique", x, y)
        
    def use_object(self):
        if self.is_owned:
            if self.owner.dodge < 1:
                self.owner.crit = min(1, self.owner.crit + 0.3)

    def draw(self, screen):
        screen.blit(crit_ring, (self.x*CELL_SIZE, self.y*CELL_SIZE))
        
class AnneauEsquive(Objet):
    def __init__(self, x, y):
        super().__init__("Anneau d'esquive", x, y)
    
    def use_object(self):
        if self.is_owned:
            if self.owner.dodge <= 0.7:
                self.owner.dodge += 0.3
            
    def draw(self, screen):
        screen.blit(dodge_ring, (self.x*CELL_SIZE, self.y*CELL_SIZE))
            
class AnneauVitesse(Objet):
    def __init__(self, x, y):
        super().__init__("Anneau de vitesse", x, y)
    
    def use_object(self):
        if self.is_owned:
            self.owner.speed += 2

    def draw(self, screen):
        screen.blit(speed_ring, (self.x*CELL_SIZE, self.y*CELL_SIZE))
        
class PotionVie(Objet):
    def __init__(self, x, y):
        super().__init__("Potion de vie", x, y)
    
    def use_object(self):
        if self.is_owned:
            self.owner.health += 50
            
    def draw(self, screen):
        screen.blit(hp_pot, (self.x*CELL_SIZE, self.y*CELL_SIZE))
