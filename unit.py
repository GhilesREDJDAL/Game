# unit.py
import pygame
from constants import CELL_SIZE, RED, BLUE, GREEN

class Unit:
    def __init__(self, x, y, health, attack_power, team):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team
        self.is_selected = False
        self.is_alive = True

    def move(self, dx, dy, obstacles, water_zones, units):
        if not self.is_alive:
            return False

        new_x = self.x + dx
        new_y = self.y + dy

        if (0 <= new_x < 8 and 0 <= new_y < 8 and (new_x, new_y) not in obstacles):
            self.x = new_x
            self.y = new_y

            if (self.x, self.y) in water_zones:
                print(f"L'unité de l'équipe {self.team} est tombée dans l'eau à ({self.x}, {self.y}) et est morte !")
                self.health = 0
                self.is_alive = False
                return True

        return False

    def attack(self, target):
        if not self.is_alive:
            return

        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power
            if target.health <= 0:
                target.is_alive = False

    def draw(self, screen):
        if not self.is_alive:
            return

        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if not self.is_alive:
            return

        bar_width = CELL_SIZE - 10
        bar_height = 5
        health_ratio = max(self.health / 10, 0)
        x = self.x * CELL_SIZE + 5
        y = self.y * CELL_SIZE - 10
        pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_ratio, bar_height))
