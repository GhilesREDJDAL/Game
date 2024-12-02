
import pygame
import sys
from unit import Knight, Archer, Mage
from constants import WIDTH, HEIGHT, CELL_SIZE, WHITE, BLACK, WATER_BLUE, GRAY, FPS
from movement import Movement

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Création des unités du joueur
        self.player_units = [
            Knight(0, 0, 'player'),
            Archer(1, 0, 'player'),
            Mage(2, 0, 'player')
        ]

        # Création des unités ennemies
        self.enemy_units = [
            Knight(6, 6, 'enemy'),
            Archer(7, 6, 'enemy'),
            Mage(5, 6, 'enemy')
        ]

        self.obstacles = {(3, 3), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}

        # Lier les obstacles, les zones d'eau et les unités au mouvement
        self.link_movement()

    def link_movement(self):
        # Associer obstacles, zones d'eau et unités aux objets de déplacement
        for unit in self.player_units + self.enemy_units:
            unit.movement.obstacles = self.obstacles
            unit.movement.water_zones = self.water_zones
            unit.movement.units = self.player_units + self.enemy_units

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

                        # L'unité se déplace selon sa vitesse
                        if selected_unit.movement.move(dx, dy):
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

            if enemy.movement.move(dx, dy):
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
            print("Game Over - Les ennemis ont gagné !")
            pygame.quit()
            sys.exit()
        elif len(self.enemy_units) == 0:
            print("Game Over - Le joueur a gagné !")
            pygame.quit()
            sys.exit()
