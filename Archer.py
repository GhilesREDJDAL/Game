#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:57:44 2024

@author: seb
"""
from Unit import *

class Archer(Unit):
    def __init__(self, x, y, team):
        super().__init__(self, x = x, y = x, health = 100, attack_power = 100, 
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