import pygame
import random
import csv
from Unit1 import *
from constantes import *

class Game:
    def __init__(self, screen, mapfile):
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
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display(selected_unit)
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:  # Move skill (only needs dx, dy)
                            self.activate_skill(selected_unit, 0, 1, 0)  # Move right (dx=1, dy=0)
                        elif event.key == pygame.K_2:  # Attack
                            target = self.enemy_units[0] if self.enemy_units else None
                            self.activate_skill(selected_unit, 1, target)  # Attack
                        elif event.key == pygame.K_3:  # Defend
                            self.activate_skill(selected_unit, 2)  # Defend
                        elif event.key == pygame.K_LEFT:
                            selected_unit.move(-1, 0)  # Move left
                        elif event.key == pygame.K_RIGHT:
                            selected_unit.move(1, 0)  # Move right
                        elif event.key == pygame.K_UP:
                            selected_unit.move(0, -1)  # Move up
                        elif event.key == pygame.K_DOWN:
                            selected_unit.move(0, 1)  # Move down

                        self.flip_display(selected_unit)

                        # End the turn after attack
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
        with open(map_file, "r") as file:
            reader = csv.reader(file)
            return [list(row) for row in reader]

    def flip_display(self, selected_unit):
        """Met à jour l'affichage du jeu."""
        # Dessiner la carte (map)
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                image = self.tile_images.get(tile)
                if image:
                    self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Dessiner les compétences
        self.draw_skills(selected_unit)

        # Rafraîchir l'écran
        pygame.display.flip()

    def draw_skills(self, selected_unit):
        """Affiche les compétences disponibles pour l'unité sélectionnée"""
        font = pygame.font.Font(None, 36)
        for i, skill in enumerate(selected_unit.skills):
            text = font.render(f"{i+1}: {skill.name}", True, (255, 255, 255))
            self.screen.blit(text, (WIDTH + 20, 100 + i * 40))

    def activate_skill(self, unit, skill_index, *args):
        """Active une compétence de l'unité."""
        if 0 <= skill_index < len(unit.skills):
            skill = unit.skills[skill_index]
            skill.use(unit, *args)
