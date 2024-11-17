#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:57:44 2024

@author: seb
"""
from Unit import *

       
class Sorcier(Unit):
    def __init__(self, x, y, team):
        super().__init__(self, x = x, y = x, health = 75, attack_power = 100, 
                         defense_power = 75, speed = 75, team = team)
        self.type = "Ranged"
        self.skills = [{"Skill name": "Boule de feu", "Power": 25, "Range": 5, "Effect": "Burn"},
                       {"Skill name": "Gèle", "Power": 0, "Range": 0, "Effect": "Freeze"}
                       ]