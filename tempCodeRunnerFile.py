import pygame
import random
import csv
from unit import *
from constantes import *

# Nouvelles dimensions
GRID_SIZE = 10  # Taille de la grille
CELL_SIZE = 60  # Taille des cases en pixels
WIDTH = GRID_SIZE * CELL_SIZE  # Largeur de la fenêtre
HEIGHT = GRID_SIZE * CELL_SIZE  # Hauteur de la fenêtre
FPS = 30  # Taux de rafraîchissement
class Unit:
    """
    Classe pour représenter une unité.
    """

    def __init__(self, x, y, health, attack_power, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy, game):
        """Déplace l'unité de dx, dy."""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Vérifie si la nouvelle position est dans les limites de la grille et n'est pas une "stone" (121)
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if game.map[new_y][new_x] != "121":  # Ne déplace pas sur une pierre
                self.x += dx
                self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen, unit_images):
        """Affiche l'unité sur l'écran en utilisant une image."""
        unit_image = unit_images[self.team]  # Sélectionner l'image en fonction de l'équipe
        image_rect = unit_image.get_rect(center=(self.x * CELL_SIZE + CELL_SIZE // 2, 
                                                 self.y * CELL_SIZE + CELL_SIZE // 2))
        screen.blit(unit_image, image_rect)
        
        # Si l'unité est sélectionnée, dessiner un contour autour de l'image
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, image_rect, 3)


class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, screen, mapfile):
        """
        Construit le jeu avec la surface de la fenêtre.
        """
        self.screen = screen
        self.map = self.load_map(mapfile)
        self.tile_images = {
            "11": pygame.image.load("grass.png"),
            "9": pygame.image.load("prize.png"),
            "121": pygame.image.load("stone.png"),
            "8": pygame.image.load("water.png"),
        }
        # Charger les images des unités
        self.unit_images = {
            'player': pygame.image.load("g.png"),  # Remplacer par votre image
            'enemy': pygame.image.load("g.png"),    # Remplacer par votre image
        }
        
        # Redimensionner les images des unités
        self.unit_images['player'] = pygame.transform.scale(self.unit_images['player'], (CELL_SIZE, CELL_SIZE))
        self.unit_images['enemy'] = pygame.transform.scale(self.unit_images['enemy'], (CELL_SIZE, CELL_SIZE))

        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]

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
            unit.draw(self.screen, self.unit_images)

        pygame.display.flip()

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy, self)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

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
