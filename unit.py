import pygame
from constants import GRID_SIZE, CELL_SIZE

# Classe qui gère le déplacement des unités
class Movement:
    def __init__(self, unit, obstacles, water_zones, units):
        self.unit = unit
        self.obstacles = obstacles
        self.water_zones = water_zones
        self.units = units

    def move(self, dx, dy):
        """Déplace l'unité selon sa vitesse."""
        if not self.unit.is_alive:
            return False

        for _ in range(self.unit.speed):  # Se déplace selon la vitesse de l'unité
            new_x = self.unit.x + dx
            new_y = self.unit.y + dy

            if isinstance(self.unit, Mage):
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    self.unit.x = new_x
                    self.unit.y = new_y
                else:
                    return False
            else:
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in self.obstacles:
                    self.unit.x = new_x
                    self.unit.y = new_y

                    if (self.unit.x, self.unit.y) in self.water_zones:
                        print(f"L'unité de l'équipe {self.unit.team} est tombée dans l'eau à ({self.unit.x}, {self.unit.y}) et est morte !")
                        self.unit.health = 0
                        self.unit.is_alive = False
                        return True
                else:
                    return False

        return False

class Unit:
    def __init__(self, x, y, health, attack_power, defense, speed, team, unit_type, image_path):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.team = team
        self.unit_type = unit_type
        self.is_selected = False
        self.is_alive = True
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

        self.movement = Movement(self, set(), set(), set())

    def attack(self, target):
        if not self.is_alive:
            return
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = max(self.attack_power - target.defense, 0)
            target.health -= damage
            if target.health <= 0:
                target.is_alive = False

    def draw(self, screen):
        if not self.is_alive:
            return

        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

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

class Knight(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_knight.png"
        else:
            image_path = "images/enemy_knight.png"
        super().__init__(x, y, 10, 2, 1, 2, team, "Knight", image_path)

class Archer(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_archer.png"
        else:
            image_path = "images/enemy_archer.png"
        super().__init__(x, y, 8, 3, 1, 1, team, "Archer", image_path)

class Mage(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_mage.png"
        else:
            image_path = "images/enemy_mage.png"
        super().__init__(x, y, 6, 4, 0, 3, team, "Mage", image_path)
