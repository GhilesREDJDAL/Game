import pygame
import random
import csv
from constantes import *

# Nouvelles dimensions
GRID_SIZE = 10  # Taille de la grille
CELL_SIZE = 60  # Taille des cases en pixels
WIDTH = GRID_SIZE * CELL_SIZE  # Largeur de la fenêtre
HEIGHT = GRID_SIZE * CELL_SIZE  # Hauteur de la fenêtre
FPS = 30  # Taux de rafraîchissement
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    """
    Classe de base pour représenter une unité.
    """
    def __init__(self, x, y, health, attack_power, team, image=None):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.image = image  # Image spécifique pour l'unité

    def move(self, dx, dy, game):
        """Déplace l'unité de dx, dy."""
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if game.map[new_y][new_x] != "121":  # Ne déplace pas sur une pierre
                self.x += dx
                self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran en utilisant son image spécifique."""
        image_rect = self.image.get_rect(center=(self.x * CELL_SIZE + CELL_SIZE // 2, 
                                                 self.y * CELL_SIZE + CELL_SIZE // 2))
        screen.blit(self.image, image_rect)
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, image_rect, 3)

# Héritage pour créer des types spécifiques d'unités

class Healer(Unit):
    def __init__(self, x, y, team, image):
        super().__init__(x, y, health=10, attack_power=2, team=team, image=image)
        self.healing_power = 3  # Exemple de compétence spécifique

    def heal(self, target):
        """Soigne une unité alliée."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health += self.healing_power
            if target.health > 10:  # Limite de la santé
                target.health = 10
class Knight(Unit):
    def __init__(self, x, y, team):
        if team == 'player':
            image_path = "images/player_knight.png"
        else:
            image_path = "images/enemy_knight.png"
        super().__init__(x, y, 10, 2, 1, 2, team, "Knight", image_path)

class Mage(Unit):
    def __init__(self, x, y, team, image):
        super().__init__(x, y, health=8, attack_power=3, team=team, image=image)
        self.magic_power = 5  # Exemple de compétence magique

    def cast_spell(self, target):
        """Lance un sort sur une unité ennemie."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.magic_power

class Knight(Unit):
    def __init__(self, x, y, team, image):
        super().__init__(x, y, health=12, attack_power=4, team=team, image=image)
        self.shield = 2  # Défense supplémentaire

    def defend(self):
        """Renforce sa défense."""
        self.health += self.shield
        if self.health > 12:  # Limite de la santé
            self.health = 12

class EnemyMage(Unit):
    def __init__(self, x, y, team, image):
        super().__init__(x, y, health=8, attack_power=3, team=team, image=image)
        self.magic_power = 5  # Exemple de compétence magique

    def cast_spell(self, target):
        """Lance un sort sur une unité ennemie."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.magic_power

# Classe Game modifiée pour utiliser ces nouvelles unités

class Game:
    def __init__(self, screen, mapfile):
        self.screen = screen
        self.map = self.load_map(mapfile)
        self.tile_images = {
            "11": pygame.image.load("grass.png"),
            "9": pygame.image.load("prize.png"),
            "121": pygame.image.load("stone.png"),
            "8": pygame.image.load("water.png"),
        }

        self.unit_images = {
            'player_healer': pygame.image.load("prize.png"),
            'player_mage': pygame.image.load("g.png"),
            'enemy_knight': pygame.image.load("g.png"),
            'enemy_mage': pygame.image.load("g.png"),
            'enemy_mage': pygame.image.load("g.png"),
            'enemy_mage': pygame.image.load("g.png"),
        }

        for key in self.unit_images:
            self.unit_images[key] = pygame.transform.scale(self.unit_images[key], (CELL_SIZE, CELL_SIZE))

        # Créer des unités spécifiques en utilisant les sous-classes
        self.player_units = [
            Healer(0, 0, 'player', self.unit_images['player_healer']),
            Mage(1, 0, 'player', self.unit_images['player_mage']),
        ]
        self.enemy_units = [
            Knight(6, 6, 'enemy', self.unit_images['enemy_knight']),
            EnemyMage(7, 6, 'enemy', self.unit_images['enemy_mage']),
        ]

    # Le reste de la classe Game reste inchangé.

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # Fermeture de la fenêtre
                        exit()  # Fermeture de la boucle

                    if event.type == pygame.KEYDOWN:
                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        # Déplacer l'unité, en passant l'instance du jeu pour vérifier la carte
                        selected_unit.move(dx, dy, self)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def load_map(self, map_file):
        """Charge la carte depuis un fichier CSV."""
        with open(map_file, "r") as file:
            reader = csv.reader(file)
            return [list(row) for row in reader]  # Retourne la carte sous forme de liste de listes


    def flip_display(self):
        """Met à jour l'affichage du jeu."""
        # Dessiner la carte (map)
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                tile_value = row[x]
                image = self.tile_images.get(tile_value)
                if image:
                    self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

        # Dessiner les unités en utilisant leurs images
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)  # Appeler draw sans unit_images

        pygame.display.flip()


    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire 
            target = random.choice(self.enemy_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy, self)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.enemy_units.remove(target)

    def draw_skills(self, unit):
        """Dessine les compétences de l'unité sélectionnée."""
        font = pygame.font.Font(None, 36)
        x, y = 10, 10  # Position de départ pour dessiner les compétences

        for skill in unit.skills:
            skill_text = font.render(skill.name, True, (255, 255, 255))
            self.screen.blit(skill_text, (x, y))
            y += 40  # Espacement vertical entre les compétences

    def handle_skill_usage(self, unit, skill_name):
        """Gère l'utilisation des compétences."""
        for skill in unit.skills:
            if skill.name == skill_name:
                skill.use(unit)
                break

def main():
    pygame.init()  # Initialisation de Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Strategy Game with Map")
    clock = pygame.time.Clock()

    # Charger le jeu avec le fichier de carte
    game = Game(screen, "maptest2.csv")  # Remplacez par le chemin vers votre fichier de carte

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        clock.tick(FPS)  # Limite le nombre de frames par seconde

if __name__ == "__main__":
    main()
