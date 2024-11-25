import pygame
import random

from unit import *

MARGIN_BOTTOM = 100  # Marge en bas pour les messages

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
    mode_de_jeu : str
        Mode de jeu choisi ('PvP' ou 'PvE').
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Archer(0, 0, 'player'),
                             Archer(1, 0, 'player')]

        self.enemy_units = [Sorcier(6, 6, 'enemy'),
                            Sorcier(7, 6, 'enemy')]

        self.mode_de_jeu = None

    def draw_text(self, text, position, size=30, color=(255, 255, 255)):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def afficher_menu(self):
        """Affiche le menu de sélection du mode de jeu."""
        self.screen.fill(BLACK)
        self.draw_text("Choisissez le mode de jeu :", (10, 10))
        self.draw_text("1. Joueur contre Joueur (PvP)", (10, 50))
        self.draw_text("2. Joueur contre la Machine (PvE)", (10, 90))
        pygame.display.flip()

        mode_choisi = False
        while not mode_choisi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.mode_de_jeu = 'PvP'
                        mode_choisi = True
                    elif event.key == pygame.K_2:
                        self.mode_de_jeu = 'PvE'
                        mode_choisi = True

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

                        # Utilisation de compétence
                        elif event.key == pygame.K_s:
                            self.flip_display()  # Afficher la grille et les unités
                            self.draw_text("Compétences disponibles :", (10, HEIGHT + 10))
                            for i, skill in enumerate(selected_unit.skills):
                                self.draw_text(f"{i + 1}. {skill.nom}", (10, HEIGHT + 50 + i * 30))
                            pygame.display.flip()
    
                            skill_selected = False
                            while not skill_selected:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if event.type == pygame.KEYDOWN:
                                        if pygame.K_1 <= event.key <= pygame.K_9:
                                            skill_index = event.key - pygame.K_1
                                            if 0 <= skill_index < len(selected_unit.skills):
                                                chosen_skill = selected_unit.skills[skill_index]
                                                skill_selected = True
    
                                                self.flip_display()  # Afficher la grille et les unités
                                                self.draw_text("Cliquez sur un ennemi pour choisir une cible.", (10, HEIGHT + 10))
                                                pygame.display.flip()
    
                                                cible_choisie = False
                                                while not cible_choisie:
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            exit()
                                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                            mx, my = pygame.mouse.get_pos()
                                                            grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                                                            for enemy in self.enemy_units:
                                                                if enemy.x == grid_x and enemy.y == grid_y:
                                                                    selected_unit.use_skill(enemy, chosen_skill)
                                                                    if enemy.health <= 0:
                                                                        self.enemy_units.remove(enemy)
                                                                    cible_choisie = True
                                                                    break
    
                                                has_acted = True
                                                selected_unit.is_selected = False
                        
                        # Information sur une unité
                        elif event.key == pygame.K_i:
                            self.flip_display()
                            self.draw_text("Cliquez sur une cible pour obtenir des informations", (10, HEIGHT + 10))
                            pygame.display.flip()
                            cible_choisie = False
                            while not cible_choisie:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                                        for target in (self.enemy_units + self.player_units):
                                            if target.x == grid_x and target.y == grid_y:
                                                self.flip_display()
                                                self.draw_text(f"L'unité choisie a {target.health} points de vie.", (10, HEIGHT + 10))
                                                pygame.display.flip()
                                                cible_choisie = True

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        if self.mode_de_jeu == 'PvE':
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

    def check_end_game(self):
        """Vérifie les conditions de fin de partie."""
        if not self.enemy_units:
            self.draw_text("Vous avez gagné!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(0, 255, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            exit()
        if not self.player_units:
            self.draw_text("Vous avez perdu!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(255, 0, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            exit()

    def flip_display(self):
        """Affiche le jeu."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Affiche les messages en bas
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(0, HEIGHT, WIDTH, MARGIN_BOTTOM))

        # Rafraîchit l'écran
        pygame.display.flip()


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT + MARGIN_BOTTOM))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Affichage du menu de sélection du mode de jeu
    game.afficher_menu()

    # Boucle principale du jeu
    while True:
        game.handle_player_turn() 
        game.handle_enemy_turn() 
        game.check_end_game() 
if __name__ == "__main__": 
    main()