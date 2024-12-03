import pygame
import sys
import random

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

            # Si l'unité est un Mage, ignore les obstacles
            if isinstance(self.unit, Mage):
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    self.unit.x = new_x
                    self.unit.y = new_y
                else:
                    return False  # Si la position est hors limites
            else:
                # Vérifie si la nouvelle position est valide pour les autres unités
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in self.obstacles:
                    self.unit.x = new_x
                    self.unit.y = new_y

                    # Vérifie si l'unité tombe dans une zone d'eau
                    if (self.unit.x, self.unit.y) in self.water_zones:
                        print(f"L'unité de l'équipe {self.unit.team} est tombée dans l'eau à ({self.unit.x}, {self.unit.y}) et est morte !")
                        self.unit.health = 0
                        self.unit.is_alive = False
                        return True
                else:
                    return False  # Si une case est bloquée, l'unité ne se déplace pas

        return False

# Classe générique pour représenter une unité
class Unit:
    def __init__(self, x, y, health, attack_power, defense, speed, team, unit_type, image_path):
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

        # Créer un objet de déplacement pour cette unité
        self.movement = Movement(self, set(), set(), set())  # Pas encore d'obstacles, zones d'eau ou autres unités

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
        super().__init__(x, y, 10, 2, 1, 2, team, "Knight", image_path)  # Vitesse = 2


class Archer(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_archer.png"
        else:
            image_path = "images/enemy_archer.png"
        super().__init__(x, y, 8, 3, 1, 1, team, "Archer", image_path)  # Vitesse = 1


class Mage(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_mage.png"
        else:
            image_path = "images/enemy_mage.png"
        super().__init__(x, y, 6, 4, 0, 3, team, "Mage", image_path)  # Vitesse = 3


# Classe principale du jeu
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.reset_game()  # Initialiser le jeu dès le début

    def reset_game(self):
        """Réinitialise le jeu avec de nouvelles unités et obstacles."""
        self.player_units = [
            Knight(0, 0, 'player'),
            Archer(1, 0, 'player'),
            Mage(2, 0, 'player')
        ]

        self.enemy_units = [
            Knight(6, 6, 'enemy'),
            Archer(7, 6, 'enemy'),
            Mage(5, 6, 'enemy')
        ]

        self.obstacles = {(3, 3), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}

        # Lier les obstacles, zones d'eau et unités au mouvement
        self.link_movement()

    def link_movement(self):
        # Associer obstacles, zones d'eau et unités aux objets de déplacement
        for unit in self.player_units + self.enemy_units:
            unit.movement.obstacles = self.obstacles
            unit.movement.water_zones = self.water_zones
            unit.movement.units = self.player_units + self.enemy_units

    def check_game_over(self):
        """Vérifie si une équipe a perdu toutes ses unités."""
        if not self.player_units:
            print("L'équipe du joueur a perdu !")
            self.display_game_over('enemy')
            return True
        if not self.enemy_units:
            print("L'équipe ennemie a perdu !")
            self.display_game_over('player')
            return True
        return False

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

            if self.check_game_over():
                return

    def handle_enemy_turn(self):
        for enemy in list(self.enemy_units):
            if not enemy.is_alive:
                self.enemy_units.remove(enemy)
                continue

            enemy.is_selected = True
            self.flip_display()

            has_acted = False
            while not has_acted:
                # Déplacement et attaque de l'ennemi
                direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                if enemy.movement.move(*direction):
                    has_acted = True

                # Attaquer une unité si à portée
                for player in self.player_units:
                    if abs(enemy.x - player.x) <= 1 and abs(enemy.y - player.y) <= 1:
                        enemy.attack(player)
                        if not player.is_alive:
                            print(f"Un joueur à ({player.x}, {player.y}) a été tué !")
                            self.player_units.remove(player)
                        has_acted = True

            if self.check_game_over():
                return

    def flip_display(self):
        self.screen.fill(BLACK)

        # Affichage des obstacles
        for x, y in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Affichage des zones d'eau
        for x, y in self.water_zones:
            pygame.draw.rect(self.screen, WATER_BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()

    def display_game_over(self, winner):
        font = pygame.font.Font(None, 50)
        if winner == 'player':
            message = "Vous avez gagné !"
        else:
            message = "Vous avez perdu !"

        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Afficher le message pendant 2 secondes

        self.reset_game()  # Réinitialiser le jeu après le message de fin

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Stratégie")
clock = pygame.time.Clock()

# Création du jeu
game = Game(screen)

# Boucle principale du jeu
while True:
    game.handle_player_turn()
    game.handle_enemy_turn()
    clock.tick(FPS)
