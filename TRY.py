import pygame
import sys

# Définition des couleurs et des dimensions
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WATER_BLUE = (0, 191, 255)
GRAY = (128, 128, 128)

# Classe générique pour représenter une unité
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

    def move(self, dx, dy, obstacles, water_zones, units):
        if not self.is_alive:
            return False

        new_x = self.x + dx
        new_y = self.y + dy

        if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in obstacles):
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
            damage = max(self.attack_power - target.defense, 0)
            target.health -= damage
            if target.health <= 0:
                target.is_alive = False

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

# Classes spécifiques pour chaque type d'unité
class Knight(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_knight.png"
        else:
            image_path = "images/enemy_knight.png"
        super().__init__(x, y, 10, 2, 1, 1, team, "Knight", image_path)


class Archer(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_archer.png"
        else:
            image_path = "images/enemy_archer.png"
        super().__init__(x, y, 8, 3, 1, 2, team, "Archer", image_path)


class Mage(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_mage.png"
        else:
            image_path = "images/enemy_mage.png"
        super().__init__(x, y, 6, 4, 0, 3, team, "Mage", image_path)


# Classe principale du jeu
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
            sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu avec obstacles et zones d'eau")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.check_game_over()
        game.handle_enemy_turn()
        game.check_game_over()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main()
