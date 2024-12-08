import pygame
import sys
import random
from constants import GRID_SIZE, BLACK, HEIGHT, WIDTH, WHITE
from animation_manager import AnimationManager

# Classe principale du jeu
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.animation_manager = AnimationManager(screen)
        self.reset_game()  # Initialiser le jeu dès le début
        self.selected_competence = None

    def reset_game(self):
        """Réinitialise le jeu avec de nouvelles unités et obstacles."""
        self.player_units = [
            self.get_unit_class("Knight")(0, 0, 'player'),
            self.get_unit_class("Archer")(1, 0, 'player'),
            self.get_unit_class("Mage")(2, 0, 'player')
        ]

        self.enemy_units = [
            self.get_unit_class("Knight")(6, 6, 'enemy'),
            self.get_unit_class("Archer")(7, 6, 'enemy'),
            self.get_unit_class("Mage")(5, 6, 'enemy')
        ]
        self.obstacles = {(3, 3),(3,4),(4,3),(5,4),(6,6), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}
        self.bonuses = self.place_bonuses()

        # Lier les obstacles, zones d'eau, unités et bonus au mouvement
        self.link_movement()

    def get_unit_class(self, unit_type):
        from units import Knight, Archer, Mage
        unit_classes = {
            "Knight": Knight,
            "Archer": Archer,
            "Mage": Mage
        }
        return unit_classes[unit_type]

    def place_bonuses(self):
        """Place les bonus de manière aléatoire sur la grille."""
        bonuses = set()
        while len(bonuses) < 5:  # Place 5 bonus sur la grille
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in self.obstacles and (x, y) not in self.water_zones:
                bonuses.add((x, y))
        return bonuses

    def link_movement(self):
        # Associer obstacles, zones d'eau, unités et bonus aux objets de déplacement
        for unit in self.player_units + self.enemy_units:
            unit.movement.obstacles = self.obstacles
            unit.movement.water_zones = self.water_zones
            unit.movement.units = self.player_units + self.enemy_units
            unit.movement.bonuses = self.bonuses

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
                            self.animation_manager.animate_movement(selected_unit, dx, dy, self.obstacles, self.water_zones, self.bonuses, self.player_units + self.enemy_units)
                            has_acted = True
                            break

                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in list(self.enemy_units):
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    self.animation_manager.animate_attack(selected_unit, enemy, self.obstacles, self.water_zones, self.bonuses, self.player_units + self.enemy_units)
                                    selected_unit.attack(enemy)
                                    if not enemy.is_alive:
                                        print(f"Un ennemi à ({enemy.x}, {enemy.y}) a été tué !")
                                        self.animation_manager.animate_death(enemy, self.obstacles, self.water_zones, self.bonuses, self.player_units + self.enemy_units)
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

                        # Utiliser une compétence
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                            competence_index = event.key - pygame.K_1
                            if competence_index < len(selected_unit.competences):
                                self.selected_competence = selected_unit.competences[competence_index]
                                self.display_competence_selection()
                                has_acted = True
                                break

                        # Confirmer l'utilisation de la compétence sélectionnée
                        if event.key == pygame.K_RETURN and self.selected_competence:
                            for enemy in list(self.enemy_units):
                                if abs(selected_unit.x - enemy.x) <= self.selected_competence.portee and abs(selected_unit.y - enemy.y) <= self.selected_competence.portee:
                                    selected_unit.use_competence(self.selected_competence, enemy, self.screen)
                                    has_acted = True
                                    self.selected_competence = None
                                    break

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
                    self.animation_manager.animate_movement(enemy, *direction, self.obstacles, self.water_zones, self.bonuses, self.player_units + self.enemy_units)
                    has_acted = True

                # Attaquer une unité si à portée
                for player in self.player_units:
                    if abs(enemy.x - player.x) <= 1 and abs(enemy.y - player.y) <= 1:
                        self.animation_manager.animate_attack(enemy, player, self.obstacles, self.water_zones, self.bonuses, self.player_units + self.enemy_units)
                        enemy.attack(player)
                        if not player.is_alive:
                            print(f"Un joueur à ({player.x}, {player.y}) a été tué !")
                            self.animation_manager.animate_death(player, self.obstacles, self.water_zones, self.bonuses, self.player_units + self.enemy_units)
                            self.player_units.remove(player)
                        has_acted = True

                # Utiliser une compétence
                if not has_acted and enemy.competences:
                    competence = random.choice(enemy.competences)
                    for player in self.player_units:
                        if abs(enemy.x - player.x) <= competence.portee and abs(enemy.y - player.y) <= competence.portee:
                            enemy.use_competence(competence, player, self.screen)
                            has_acted = True
                            break

            if self.check_game_over():
                return

    def display_competence_selection(self):
        self.screen.fill(BLACK)
        self.animation_manager.draw_background()
        self.animation_manager.draw_grid(self.obstacles, self.water_zones, self.bonuses)
        self.animation_manager.draw_units(self.player_units + self.enemy_units)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Compétence sélectionnée: {self.selected_competence.nom}", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 50))
        self.screen.blit(text, text_rect)

        # Afficher les compétences disponibles
        for index, competence in enumerate(self.selected_unit.competences):
            competence_text = font.render(f"{index + 1}: {competence.nom}", True, WHITE)
            competence_rect = competence_text.get_rect(topleft=(10, HEIGHT + 80 + index * 40))
            self.screen.blit(competence_text, competence_rect)

        pygame.display.flip()
        pygame.time.wait(1000)

    def flip_display(self):
        self.screen.fill(BLACK)
        self.animation_manager.draw_background()
        self.animation_manager.draw_grid(self.obstacles, self.water_zones, self.bonuses)
        self.animation_manager.draw_units(self.player_units + self.enemy_units)
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

        pygame.quit()  # Ferme la fenêtre Pygame
        sys.exit()  # Quitte le programme
