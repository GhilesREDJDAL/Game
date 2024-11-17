#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:57:45 2024

@author: seb
"""
from unit import *
import numpy as np

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
