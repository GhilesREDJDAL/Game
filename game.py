# game.py
import pygame
import sys
from constants import GRID_SIZE, CELL_SIZE, WIDTH, HEIGHT, BLACK, WHITE, GRAY, WATER_BLUE
from unit import Unit

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
                                    selected_unit.attack(enemy)
                                    if not enemy.is_alive:
                                        print(f"Un ennemi à ({enemy.x}, {enemy.y}) a été tué !")
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

            if enemy.move(dx, dy, self.obstacles, self.water_zones, self.enemy_units + self.player_units):
                self.enemy_units.remove(enemy)
                continue

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if not target.is_alive:
                    print(f"L'unité du joueur à ({target.x}, {target.y}) a été tuée !")
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
            sys.exit
