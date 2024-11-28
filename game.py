import pygame
import random
import sys

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
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
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


class Game:
    """
    Classe pour représenter le jeu.
    """
    def __init__(self, screen):
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            selected_unit.is_selected = True
            self.flip_display()

            has_acted = False
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        # Déplacement
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

                        # Attaque
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            target = min(self.player_units, key=lambda p: abs(p.x - enemy.x) + abs(p.y - enemy.y))
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu."""
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()


def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        pygame.time.Clock().tick(FPS)


if __name__ == "__main__":
    main()
