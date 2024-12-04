import pygame
import random
import csv  # Ensure the csv module is imported at the top of your file
from unit import *


# Constantes pour le jeu
CELL_SIZE = 60
GRID_SIZE = 10
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
BLACK = (0, 0, 0)

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen, mapfile):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.map = self.load_map(mapfile)
        self.tile_images = {
            "11": pygame.image.load("grass.png"),
            "9": pygame.image.load("prize.png"),
            "121": pygame.image.load("stone.png"),
            "8" : pygame.image.load("water.png"),
        }
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

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
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

                        selected_unit.move(dx, dy)
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
        """Load the map from a CSV file."""
        with open(map_file, "r") as file:  # Use map_file instead of maptest
            reader = csv.reader(file)
            return [list(row) for row in reader]

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Met à jour l'affichage du jeu."""

        # Dessiner la carte (map)
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                image = self.tile_images.get(tile)  # On récupère l'image pour la tuile
                if image:
                    self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

       

        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Rafraîchir l'écran
        pygame.display.flip()

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
        if event.type==pygame.QUIT:
            pygame.quit() #closing window  
            exit() #closing the loop

if __name__ == "__main__":
    main()