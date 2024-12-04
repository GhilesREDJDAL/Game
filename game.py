import pygame
import random

from unit import *
from Constantes import GRID_SIZE, CELL_SIZE, WIDTH, HEIGHT, BLACK, WHITE, GRAY, WATER_BLUE, MARGIN_BOTTOM

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
        self.player_units = [Sorcier(0, 0, 'player'),
                             Archer(1, 0, 'player'), Healer(3,1, 'player')]

        self.enemy_units = [Sorcier(6, 6, 'enemy'),
                            Sorcier(7, 6, 'enemy')]

        self.mode_de_jeu = None
        self.obstacles = {(3, 3), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}
        self.current_effects = []
        # Load images for grass, water, and obstacles
        self.grass_image = pygame.image.load('grass.png')
        self.water_image = pygame.image.load('water.png')
        self.obstacle_image = pygame.image.load('stone.png')

        # Scale images to match the grid cell size
        self.grass_image = pygame.transform.scale(self.grass_image, (CELL_SIZE, CELL_SIZE))
        self.water_image = pygame.transform.scale(self.water_image, (CELL_SIZE, CELL_SIZE))
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (CELL_SIZE, CELL_SIZE))

        
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
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
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
    
                        selected_unit.move(dx, dy, self.obstacles, self.water_zones)
                        if selected_unit in self.player_units and selected_unit.health <= 0:
                            self.player_units.remove(selected_unit)
                            has_acted = True
                            selected_unit.is_selected = False
                        self.flip_display()
    
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            has_acted = True
                            selected_unit.is_selected = False
    
                        elif event.key == pygame.K_s:
                            self.flip_display()
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
    
                                                self.flip_display()
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
                                                                    if chosen_skill.effet is not None:
                                                                        print(f"Applying {chosen_skill.effet.name} effect to enemy at ({enemy.x}, {enemy.y})")
                                                                        self.apply_effect(enemy, chosen_skill)
                                                                    cible_choisie = True
                                                                    break
                                                has_acted = True
                                                selected_unit.is_selected = False
    
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
                        self.player_units.remove(target)
                if enemy.health <= 0:
                    self.enemy_units.remove(enemy)

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
        
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                self.screen.blit(self.grass_image, (x, y))

        # Draw the grid (optional, if you want the grid to be visible over the grass)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.rect(self.screen, WHITE, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Affiche les zones d'eau avec l'image de l'eau
        for x, y in self.water_zones:
            self.screen.blit(self.water_image, (x * CELL_SIZE, y * CELL_SIZE))

        # Affiche les obstacles avec l'image de la pierre
        for x, y in self.obstacles:
            self.screen.blit(self.obstacle_image, (x * CELL_SIZE, y * CELL_SIZE))

        # Draw the effects on the screen
        self.draw_effects(self.screen)

        # Affiche les messages en bas (bottom margin)
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(0, HEIGHT, WIDTH, MARGIN_BOTTOM))

        # Rafraîchit l'écran
        pygame.display.flip()
    
      
    
  

    def draw_effects(self, screen):
        """Draw all current effects on the screen."""
        for (x, y), effect in self.current_effects:
            # Example: Draw a semi-transparent overlay for effects
            if effect.name == "Feu":
                color = (255, 69, 0, 128)  # Orange with transparency
            elif effect.name == "Poison":
                color = (128, 0, 128, 128)  # Purple with transparency
            elif effect.name == "Soin":
                color = (0, 255, 0, 128)  # Green with transparency
            else:
                continue
    
            # Create a surface with the specified color
            overlay = pygame.Surface((CELL_SIZE, CELL_SIZE))
            overlay.set_alpha(128)  # Set transparency level
            overlay.fill(color)
    
            # Draw the overlay on the specified cell
            screen.blit(overlay, (x * CELL_SIZE, y * CELL_SIZE))


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
        game.update_effects()
        game.check_end_game()
        game.flip_display()

if __name__ == "__main__": 
    main()