import pygame
from constants import CELL_SIZE, GRID_SIZE, WHITE

# Classe générique pour représenter une unité
class Unit:
    def __init__(self, x, y, health, attack_power, defense, speed, team, unit_type, image_path, crit=0.1, dodge=0.1):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed  # La vitesse détermine combien de cases une unité peut se déplacer
        self.team = team
        self.unit_type = unit_type
        self.is_selected = False
        self.is_alive = True
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.crit = crit
        self.dodge = dodge
        self.competences = []
        self.effect_status = None

        # Créer un objet de déplacement pour cette unité
        self.movement = self.get_movement_class()(self, set(), set(), set(), set())  # Pas encore d'obstacles, zones d'eau, autres unités ou bonus

    def attack(self, target):
        if not self.is_alive:
            return

        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = max(self.attack_power - target.defense, 0)
            target.health -= damage
            if target.health <= 0:
                target.is_alive = False

    def use_competence(self, competence, target, screen):
        competence.use(self, target, screen)

    def draw(self, screen):
        if not self.is_alive:
            return

        # Dessiner l'image de l'unité
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Afficher une bordure verte si l'unité est sélectionnée
        if self.is_selected:
            pygame.draw.rect(screen, (0, 255, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if not self.is_alive:
            return

        bar_width = CELL_SIZE - 10
        bar_height = 5
        health_ratio = max(self.health / 10, 0)
        x = self.x * CELL_SIZE + 5
        y = self.y * CELL_SIZE - 10
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width * health_ratio, bar_height))

    def get_movement_class(self):
        from movement import Movement
        return Movement

# Classes spécifiques pour chaque type d'unité
class Knight(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_knight.png"
        else:
            image_path = "images/enemy_knight.png"
        super().__init__(x, y, 10, 2, 1, 2, team, "Knight", image_path)  # Vitesse = 2
        self.competences = [self.get_competence_class("CoupDEpee")(), self.get_competence_class("CoupDeBouclier")()]

    def get_competence_class(self, competence_name):
        from competences import CoupDEpee, CoupDeBouclier
        competence_classes = {
            "CoupDEpee": CoupDEpee,
            "CoupDeBouclier": CoupDeBouclier
        }
        return competence_classes[competence_name]

class Archer(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_archer.png"
        else:
            image_path = "images/enemy_archer.png"
        super().__init__(x, y, 8, 3, 1, 1, team, "Archer", image_path)  # Vitesse = 1
        self.competences = [self.get_competence_class("TirArc")(), self.get_competence_class("FlecheEmpoisonnee")()]

    def get_competence_class(self, competence_name):
        from competences import TirArc, FlecheEmpoisonnee
        competence_classes = {
            "TirArc": TirArc,
            "FlecheEmpoisonnee": FlecheEmpoisonnee
        }
        return competence_classes[competence_name]

class Mage(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_mage.png"
        else:
            image_path = "images/enemy_mage.png"
        super().__init__(x, y, 6, 4, 0, 3, team, "Mage", image_path)  # Vitesse = 3
        self.competences = [self.get_competence_class("BouleDeFeu")()]

    def get_competence_class(self, competence_name):
        from competences import BouleDeFeu
        competence_classes = {
            "BouleDeFeu": BouleDeFeu
        }
        return competence_classes[competence_name]
