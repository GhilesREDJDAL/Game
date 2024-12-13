from abc import ABC, abstractmethod
import numpy as np
from Effects import *
from utils import draw_text
from Constantes import HEIGHT, GRID_SIZE, CELL_SIZE, WIDTH
import pygame

class Competence(ABC):
    """ Classe abstraite mère pour les compétences.
    ...
    Attributs
    ---------
    nom: str
        Le nom de la compétence
    puissance : int
        La puissance (dégats infligés) de la compétence
    portee : int
        La portée de la compétence
    aoe_radius : int
        La rayon d'effet de la compétence (si applicable)
    effet : Effect
        Effet associé à la compétence (si applicable)
    
    Méthodes
    --------
    use(utilisateur, cible, screen)
        Utilisation de la compétence et affichage selon les résultats de crit- et dodge_ check.
    crit_check(utilisateur)
        Determine si le cout critique a lieu
    dodge_check(cible)
        Determine si l'esquive a lieu
    display_message(screen, text)
        Affiche un message
    """
    
    def __init__(self, nom, puissance, portee, aoe_radius, effet=None):
        self.nom = nom
        self.puissance = puissance
        self.portee = portee
        self.aoe_radius = aoe_radius  # Area of effect radius
        self.effet = effet
        self.type = None

    def use(self, utilisateur, cible, screen, extra_aoelist=None):
        """ Utilisation de la compétence """
        if abs(utilisateur.x - cible.x) <= self.portee and abs(utilisateur.y - cible.y) <= self.portee:
            if self.dodge_check(cible):
                self.display_message(screen, "L'attaque a été esquivée!")
                return False

            if self.crit_check(utilisateur):
                crit_dmg = (utilisateur.attack_power + self.puissance) * 2
                dmg = max(0, crit_dmg - cible.defense_power)
                self.display_message(screen, f"Coup critique! Dégâts infligés: {dmg}")
            else:
                dmg = max(0, (utilisateur.attack_power + self.puissance) - cible.defense_power)
                self.display_message(screen, f"Dégâts infligés: {dmg}")
                cible.take_damage(utilisateur, dmg)
            if self.effet:
                cible.effect_status = self.effet
            return True
    
    def crit_check(self, utilisateur):
        """ Calcul aléatoire du coup critique, retourne True ou False selon le 
            taux critique de l'unité qui utilise la compétence"""
        return np.random.choice([True, False], p=[utilisateur.crit, 1-utilisateur.crit])

    def dodge_check(self, cible):
        """ Calcul aléatoire de l'evasion, retourne True ou False selon le 
            taux d'évasion de la cible """
        return np.random.choice([True, False], p=[cible.dodge, 1-cible.dodge])

    def display_message(self, screen, text):
        """ Affichage du message coup critique/evasion. """
        draw_text(screen, text, (10, HEIGHT + 10)) 
        pygame.display.flip()

    def draw_skill_effect(self, screen):
    	pass

fleche_frame = pygame.image.load("images/skills/Barrage/target_1.png")
fleche_frame = pygame.transform.scale(fleche_frame, (CELL_SIZE, CELL_SIZE))
class TirArc(Competence):
    """ Sous fille TirArc de Compétence """
    def __init__(self):
        super().__init__("Tir à l'arc", 20, 99, 1)
        self.type = "Attack"
        
    def use(self, utilisateur, cible, screen, extra_aoelist=None):
        super().use(utilisateur, cible, screen)
        self.draw_skill_effect(screen, [(cible.x, cible.y)])
        
    def draw_skill_effect(self, screen, positions):
        x, y = positions[0][0], positions[0][1]
        screen.blit(fleche_frame, (x * CELL_SIZE, y * CELL_SIZE))
        pygame.display.flip()
        pygame.time.wait(30)

class FlecheEmpoisonnee(Competence):
    def __init__(self):
        super().__init__("Flèche empoisonnée", 10, 5, 1, Poison())
        self.type = "Attack"

class BarrageDeFleches(Competence):
    def __init__(self):
        super().__init__("Barrage de Fleches", 15, 80, 1)
        self.type = "AoE"

    def use(self, utilisateur, cible, screen, extra_aoelist):
        x, y = cible.x, cible.y
        for enemy in extra_aoelist:
            if enemy.y == y:
                super().use(utilisateur, enemy, screen)
                self.draw_skill_effect(screen, [(enemy.x, enemy.y)])
                
    def draw_skill_effect(self, screen, positions):
        x, y = positions[0][0], positions[0][1]
        screen.blit(fleche_frame, (x * CELL_SIZE, y * CELL_SIZE))
        pygame.display.flip()
        pygame.time.wait(30)
            
bdf_frames = [pygame.image.load(f"images/skills/FB_hit/fb_hit_{i}.png") for i in range(1, 4)]  # Adjust based on your actual frame files
bdf_frames = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in bdf_frames] 
class BouleDeFeu(Competence):
    def __init__(self):
        super().__init__("Boule de feu", 25, 5, 3, Feu())
        self.type = "Attack"
        
    def use(self, utilisateur, cible, screen, extra_aoelist=None):
        super().use(utilisateur, cible, screen)
        self.draw_skill_effect(screen, [(cible.x, cible.y)])
        
    def draw_skill_effect(self, screen, positions):
        x, y = positions[0][0], positions[0][1]
        for frame in bdf_frames:
            screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))
            pygame.display.flip()
            pygame.time.wait(100)
            
class CoupDEpee(Competence):
    def __init__(self):
        super().__init__("Coup d'épée", 35, 1, 1)
        self.type = "Attack"

class CoupDeBouclier(Competence):
    def __init__(self):
        super().__init__("Coup de bouclier", 20, 1, 1)
        self.type = "Attack"

    def use(self, utilisateur, cible, screen, extra_aoelist=None):
        """ Surcharge de la méthode d'utilisation de la compétence, adaptée à celle-ci"""
        success = super().use(utilisateur, cible, screen)
        if not success:
            return False
        #Si l'attaque n'a pas été esquivé:
        dx = cible.x - utilisateur.x
        dy = cible.y - utilisateur.y
        #La cible est déplacée d'une case selon l'orientation de l'utilisateur:
        if dx > 0 and cible.x < GRID_SIZE - 1:
            cible.x += 1
        elif dx < 0 and cible.x > 0:
            cible.x -= 1
        if dy > 0 and cible.y < GRID_SIZE - 1:
            cible.y += 1
        elif dy < 0 and cible.y > 0:
            cible.y -= 1
        return True

class Teleportation(Competence):
    def __init__(self):
        super().__init__("Teleportation", 0, 99, 0)
        self.type = "Movement"
    def use(self, utilisateur, cible, screen, extra_aoelist=None):
        utilisateur.x = cible[0]
        utilisateur.y = cible[1]
        self.display_message(screen, f"Vous vous êtes téléportés à l'emplacement ({cible[0]}, {cible[1]})!")
        return True

class ZoneDeSoin(Competence):
    def __init__(self):
        super().__init__("Zone de Soin", 10, 99, 3, effet=Soin())
        self.type = "Zone"
    
    def use(self, utilsiateur, cible, screen, extra_aoelist=None):
        self.display_message(screen, f"Vous avez créé une zone de soin!")
        return True
  

sword_frames = [pygame.image.load(f"images/skills/Sword/sword_{i}.png") for i in range(1, 4)]  # Adjust based on your actual frame files
sword_frames = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE*1.5)) for img in sword_frames]      
sword_ground = pygame.image.load('images/skills/Sword/ground.png')
sword_ground = pygame.transform.scale(sword_ground, (CELL_SIZE, CELL_SIZE))


class EpeeDivine(Competence):
    def __init__(self):
        super().__init__("Epée Divine", 30, 99, 1)
        self.type = "AoE"

    def use(self, utilisateur, cible, screen, extra_aoelist):
        x, y = cible.x, cible.y
        positions = [
            (x, y),
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1),
            (x - 2, y), (x + 2, y),
            (x, y - 2), (x, y + 2)
        ]
        self.draw_skill_effect(screen, positions)
        for enemy in extra_aoelist:
            if (enemy.x, enemy.y) in positions:
                super().use(utilisateur, enemy, screen)

        return True
        
    def draw_skill_effect(self, screen, positions):
        x, y = positions[0][0], positions[0][1]
        # Play sword animation
        start_time = pygame.time.get_ticks()
        frame_duration = 100  # 0.1 second per frame

        for frame in sword_frames:
            screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE - CELL_SIZE/2))
            pygame.display.flip()
            pygame.time.wait(100)

        max_x = WIDTH // CELL_SIZE - 1
        max_y = HEIGHT // CELL_SIZE - 1

        # Play ground breaking animation in "+" pattern using a single frame
        for pos in positions:
            px, py = pos
            if 0 <= px <= max_x and 0 <= py <= max_y:  # Boundary check
                screen.blit(sword_ground, (px * CELL_SIZE, py * CELL_SIZE))
        pygame.display.flip()
        pygame.time.wait(frame_duration)  # Wait for the ground breaking effect to be visible

