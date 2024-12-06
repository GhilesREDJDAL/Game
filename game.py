import pygame
import random

from unit import *
from Constantes import GRID_SIZE, CELL_SIZE, WIDTH, HEIGHT, BLACK, WHITE, GRAY, WATER_BLUE, MARGIN_BOTTOM
from utils import draw_text, flip_display, draw_effects

GAME_CONTINUE = True

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
        self.enemy_units = []
        self.team1_units = []
        self.team2_units = []
        self.player_units = []
        self.up_coords = [(1, 1), (1, 2), (2, 1)]
        self.down_coords = [(GRID_SIZE-1, GRID_SIZE-1), (GRID_SIZE-1, GRID_SIZE-2), (GRID_SIZE-2, GRID_SIZE-1)]
        self.mode_de_jeu = None
        self.obstacles = {(3, 3), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}
        self.current_effects = []

    def afficher_menu(self):
        global GAME_CONTINUE
        """Affiche le menu de sélection du mode de jeu."""
        self.screen.fill(BLACK)
        draw_text(self.screen, "Choisissez le mode de jeu :", (10, 10))
        draw_text(self.screen, "1. Joueur contre Joueur (PvP)", (10, 50))
        draw_text(self.screen, "2. Joueur contre la Machine (PvE)", (10, 90))
        draw_text(self.screen, "3. Quittez le jeu", (10, 120))
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
                        self.team1_units = self.selectionner_unites("Equipe 1")
                        self.team2_units = self.selectionner_unites("Equipe 2")
                        mode_choisi = True
                    elif event.key == pygame.K_2:
                        self.mode_de_jeu = 'PvE'
                        self.team1_units = self.selectionner_unites("Joueur")
                        self.enemy_units = [random.choice([Sorcier, Guerrier, Archer])(x, y, 'Ennemi') for x, y in self.down_coords]
                        mode_choisi = True
                    elif event.key == pygame.K_3:
                        self.mode_de_jeu = 'Quit'
                        mode_choisi = True
                        GAME_CONTINUE = False
        self.player_units = self.team1_units + self.team2_units 
        self.current_effects = []
        
    def selectionner_unites(self, team):
        """Permet à un joueur de sélectionner 3 unités."""
        units = []
        for i in range(3):
            selection_made = False
            while not selection_made:
                self.screen.fill(BLACK)
                draw_text(self.screen, f"{team}, choisissez votre unité {i + 1} :", (10, 10))
                draw_text(self.screen, "1. Sorcier", (10, 50))
                draw_text(self.screen, "2. Guerrier", (10, 90))
                draw_text(self.screen, "3. Archer", (10, 130))
                pygame.display.flip()
    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if team == "Equipe 1" or team =="Joueur":
                            x, y = self.up_coords[i]
                        elif team == "Equipe 2" or team == "Ennemi":
                            x, y  = self.down_coords[i]
                        if event.key == pygame.K_1:
                            units.append(Sorcier(x, y, team))
                            selection_made = True
                        elif event.key == pygame.K_2:
                            units.append(Guerrier(x, y, team))
                            selection_made = True
                        elif event.key == pygame.K_3:
                            units.append(Archer(x, y, team))
                            selection_made = True
        return units



    def handle_player_turn(self, turn_units):
        """Tour du joueur"""
        for selected_unit in turn_units:
            has_acted = False
            selected_unit.is_selected = True
            mvmt_cpt = selected_unit.speed
            friend_loop_check = False
            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
            while not has_acted:
                if friend_loop_check:
                    friend_loop_check = False
                if not self.enemy_units and (not self.team1_units or not self.team2_units):
                    return
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
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
                        if mvmt_cpt >= 0:
                            selected_unit.move(dx, dy, self.obstacles, self.water_zones)
                            mvmt_cpt -= 1  # Reduce the movement counter
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                        if mvmt_cpt < 0:
                            draw_text(self.screen, "Vous ne pouvez plus vous déplacer.", (10, HEIGHT + 10))
                            pygame.display.flip()
                            pygame.time.wait(1000)
                            if selected_unit in turn_units and selected_unit.health <= 0:
                                turn_units.remove(selected_unit)
                                has_acted = True
                                selected_unit.is_selected = False
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            has_acted = True
                            selected_unit.is_selected = False
                     
                        elif event.key == pygame.K_s:
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                            draw_text(self.screen, "Compétences disponibles :", (10, HEIGHT + 10))
                            for i, skill in enumerate(selected_unit.skills):
                                draw_text(self.screen, f"{i + 1}. {skill.nom}", (10, HEIGHT + 50 + i * 30))
                            pygame.display.flip()

                            skill_selected = False
                            while not skill_selected:
                                if friend_loop_check:
                                    break
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

                                                flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                draw_text(self.screen, "Cliquez sur un ennemi pour choisir une cible.", (10, HEIGHT + 10))
                                                pygame.display.flip()

                                                cible_choisie = False
                                                while not cible_choisie:
                                                    if friend_loop_check:
                                                        break
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            exit()
                                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                            mx, my = pygame.mouse.get_pos()
                                                            grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                                                
                                                            # Check if the click is on a friendly unit (using turn_units)
                                                            for friendly in turn_units:
                                                                if friendly.x == grid_x and friendly.y == grid_y:
                                                                    flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                    draw_text(self.screen, "Vous ne pouvez pas attaquer votre propre unité!", (10, HEIGHT + 10))
                                                                    pygame.display.flip()
                                                                    pygame.time.wait(300)
                                                                    friend_loop_check = True
                                                                    break
                                                            # Check if the click is on an enemy unit (using all_player_units minus turn_units)
                                                            for unit in self.player_units:
                                                                if unit not in turn_units and unit.x == grid_x and unit.y == grid_y:
                                                                    flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                    if selected_unit.use_skill(unit, chosen_skill, self.screen):
                                                                        has_acted = True
                                                                    pygame.time.wait(300)
                                                                    if unit.health <= 0:
                                                                        if unit.team == "Equipe 1":
                                                                            self.team1_units.remove(unit)
                                                                        elif unit.team == "Equipe 2":
                                                                            self.team2_units.remove(unit)
                                                                        self.player_units.remove(unit)
                                                                    if chosen_skill.effet is not None:
                                                                        self.apply_effect(unit, chosen_skill)
                                                                    cible_choisie = True
                                                                    selected_unit.is_selected = False
                                                                    break
                                                
                                                            # Check if the click is on an enemy unit (PvE mode)
                                                            for enemy in self.enemy_units:
                                                                if enemy.x == grid_x and enemy.y == grid_y:
                                                                    flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                    if selected_unit.use_skill(unit, chosen_skill, self.screen):
                                                                        has_acted = True
                                                                    pygame.time.wait(300)
                                                                    if enemy.health <= 0:
                                                                        self.enemy_units.remove(enemy)
                                                                    if chosen_skill.effet is not None:
                                                                        self.apply_effect(enemy, chosen_skill)
                                                                    cible_choisie = True
                                                                    has_acted = True
                                                                    selected_unit.is_selected = False
                                                                    break       
                        elif event.key == pygame.K_i:
                            self.disp_info()

    def disp_info(self):
        flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
        draw_text(self.screen, "Cliquez sur une cible pour obtenir des informations", (10, HEIGHT + 10))
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
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                            info_text = (
                                f"L'unité choisie a {target.health} points de vie.\n"
                                f"Points d'attaque : {target.attack_power}\n"
                                f"Défense : {target.defense_power}\n"
                                f"Vitesse : {target.speed}"
                            )
                            draw_text(self.screen, info_text, (10, HEIGHT + 10))  # Adjusting starting position
                            pygame.display.flip()
                            cible_choisie = True

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        if self.mode_de_jeu == 'PvE':
            for enemy in self.enemy_units:
                if not self.player_units:
                    print("No player units available to target")
                    continue
                # Déplacement aléatoire
                target = random.choice(self.player_units)
                dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
                enemy.move(dx, dy, self.obstacles, self.water_zones)

                # Attaque si possible
                if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                    enemy.attack(target)
                    if target.health <= 0:
                        self.team1_units.remove(target)
                        self.player_units.remove(target)
                if enemy.health <= 0:
                    self.enemy_units.remove(enemy)

    def check_end_game(self):
        """Vérifie les conditions de fin de partie."""
        if self.mode_de_jeu == 'PvP':
            if not self.team1_units:
                draw_text(self.screen, "Equipe 2 a gagné!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(255, 0, 0))
                pygame.display.flip()
                pygame.time.wait(1500)
                return True
            if not self.team2_units:
                draw_text(self.screen, "Equipe 1 a gagné!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(0, 255, 0))
                pygame.display.flip()
                pygame.time.wait(1500)
                return True
        elif self.mode_de_jeu == 'PvE':
            if not self.enemy_units:
                draw_text(self.screen, "Vous avez gagné!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(0, 255, 0))
                pygame.display.flip()
                pygame.time.wait(1500)
                return True
            if not self.team1_units:
                draw_text(self.screen, "Vous avez perdu!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(255, 0, 0))
                pygame.display.flip()
                pygame.time.wait(1500)
                return True
        return False

    def apply_effect(self, target, skill):
        """Applies an effect to all cells within the area of effect range around the target."""

        affected_cells = []

        if skill.aoe_radius == 1:  # flecheempoisonée
            affected_cells.append((target.x, target.y))
        elif skill.aoe_radius == 3:  # boule de feu
            for dx in range(-2, 3):  # Cover 2 cells on each side
                for dy in range(-2, 3):
                    x = target.x + dx
                    y = target.y + dy
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        affected_cells.append((x, y))

        for x, y in affected_cells:
            new_effect = skill.effet.__class__()  # Create a new instance of the effect
            new_effect.effectTTL = skill.effet.effectTTL  # Copy the effectTTL value
            self.current_effects.append(((x, y), new_effect))
            for unit in self.player_units + self.enemy_units:
                if unit.x == x and unit.y == y:
                    new_effect.apply_effect(unit)

    def update_effects(self):
        """Apply effects to units in affected cells and reduce effect duration."""

        for (x, y), effect in self.current_effects[:]:
            for unit in self.player_units + self.enemy_units:
                if unit.x == x and unit.y == y:
                    effect.apply_effect(unit)

            # Reduce effect duration
            effect.effectTTL -= 1

        # Remove expired effects
        self.current_effects = [((x, y), effect) for (x, y), effect in self.current_effects if effect.effectTTL > 0]

    def handle_turns(self):
        if self.mode_de_jeu == "PvP":
            self.handle_player_turn(self.team1_units)
            self.handle_player_turn(self.team2_units)
        elif self.mode_de_jeu == "PvE":
            self.handle_player_turn(self.team1_units)
            self.handle_enemy_turn()

def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT + MARGIN_BOTTOM))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    while True:
        # Affichage du menu de sélection du mode de jeu
        game.afficher_menu()
        if not GAME_CONTINUE:
            pygame.quit()
            exit()
        # Boucle principale du jeu
        while not game.check_end_game():
            game.handle_turns()
            game.update_effects()
            flip_display(screen, game.player_units, game.enemy_units, game.water_zones, game.obstacles, game.current_effects)

if __name__ == "__main__":
    main()
