<<<<<<< HEAD
import pygame
import random

# Constantes
GRID_SIZE = 8  # Taille de la grille (8x8)
CELL_SIZE = 60  # Taille de chaque cellule (en pixels)
WIDTH = GRID_SIZE * CELL_SIZE  # Largeur de la fenêtre
HEIGHT = GRID_SIZE * CELL_SIZE  # Hauteur de la fenêtre
FPS = 30  # Images par seconde 

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    """
    Classe pour représenter une unité.
    """
    def __init__(self, x, y, health, attack_power, team):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy dans les limites de la grille."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible adjacente."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen, font):
        """Affiche l'unité et ses points de vie sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        health_text = font.render(str(self.health), True, WHITE)
        screen.blit(health_text, (self.x * CELL_SIZE + 5, self.y * CELL_SIZE - 10))

class Game:
    """Classe principale pour gérer le jeu."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.player_units = [Unit(0, 0, 10, 2, 'player'), Unit(1, 0, 10, 2, 'player')]
        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'), Unit(7, 6, 8, 1, 'enemy')]

    def handle_player_turn(self):
        """Gestion du tour du joueur."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        selected_unit.move(dx, dy)
                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA simple pour le tour des ennemis."""
        for enemy in self.enemy_units:
            if len(self.player_units) == 0:
                return
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def check_game_over(self):
        """Vérifie si le jeu est terminé."""
        if len(self.player_units) == 0:
            print("Les ennemis ont gagné !")
            pygame.quit()
            exit()
        elif len(self.enemy_units) == 0:
            print("Le joueur a gagné !")
            pygame.quit()
            exit()

    def flip_display(self):
        """Met à jour l'affichage."""
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen, self.font)

        pygame.display.flip()

def main():
    """Lance le jeu."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.check_game_over()
        game.handle_enemy_turn()
        game.check_game_over()
        game.flip_display()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
=======
import pygame
import sys
from unit import Unit
from constants import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]
        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]
        self.obstacles = {(3, 3), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}

    def handle_player_turn(self):
        for selected_unit in list(self.player_units):
            if not selected_unit.is_alive:
                self.player_units.remove(selected_unit)
                continue

            selected_unit.is_selected = True
            self.flip_display()

            has_acted = False
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        if selected_unit.move(dx, dy, self.obstacles, self.water_zones, self.player_units + self.enemy_units):
                            self.player_units.remove(selected_unit)
                            has_acted = True
                            break

                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in list(self.enemy_units):
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy, self.obstacles)
                                    if not enemy.is_alive:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        for enemy in list(self.enemy_units):
            if not enemy.is_alive:
                self.enemy_units.remove(enemy)
                continue

            if len(self.player_units) == 0:
                break

            target = min(self.player_units, key=lambda p: abs(p.x - enemy.x) + abs(p.y - enemy.y))
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

            if not enemy.move(dx, dy, self.obstacles, self.water_zones, self.enemy_units + self.player_units):
                print(f"Ennemi bloqué à ({enemy.x}, {enemy.y}), cherche une autre action.")

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target, self.obstacles)
                if not target.is_alive:
                    self.player_units.remove(target)

    def flip_display(self):
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for x, y in self.water_zones:
            pygame.draw.rect(self.screen, WATER_BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for x, y in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()

    def check_game_over(self):
        if len(self.player_units) == 0:
            print("Les ennemis ont gagné !")
            pygame.quit()
            sys.exit()
        elif len(self.enemy_units) == 0:
            print("Le joueur a gagné !")
            pygame.quit()
            sys.exit()
>>>>>>> 2e34b69 (Jeux modifiée)
