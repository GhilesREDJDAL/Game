import pygame
import random
import numpy as np

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
        La liste des unités de joueurs (2 équipes).
    team1_units : list[Unit]
        La liste des unités de l'équipe 1.
    team2_units : list[Unit]
        La liste des unités de l'équipe 2.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire IA.
    mode_de_jeu : str
        Mode de jeu choisi ('PvP' ou 'PvE' ou 'Quit' [pour quitter le jeu]).
        
    Méthodes
    --------
    afficher_menu
        Affiche le menu et gère la selection du mode de jeu
    selectionner_unites
        Gère la selection des unités selon le mode de jeu(PvP/PvE)
    handle_player_turn
        Gère le tour de l'équipe qui doit agir
    disp_info
        Affiche les information d'une unité sélectionnée
    handle_enemy_turn
        Gère le tour de l'IA
    check_end_game
        Verifie les conditions d'arret du jeu
    apply_effect
        Applique les effets selon les emplacements du grid
    update_effects
        Applique les effets sur les unités présentes sur les empplacements affectés
    handle_turns
        Gère le tour par tour selon le mode de jeu (PvP/PvE)
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
        #On affiche les modes de jeu disponnibles, ainsi que l'option de quitter le jeu:
        draw_text(self.screen, "Choisissez le mode de jeu :", (10, 10))
        draw_text(self.screen, "1. Joueur contre Joueur (PvP)", (10, 50))
        draw_text(self.screen, "2. Joueur contre la Machine (PvE)", (10, 90))
        draw_text(self.screen, "3. Quittez le jeu", (10, 120))
        pygame.display.flip()
    
        mode_choisi = False
        #Tant que le mode de jeu n'a pas été choisi:
        while not mode_choisi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                #L'utilisateur peut choisir entre 3 modes (PvP, PvE, et Quit pour quitter le jeu)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        #Si le mode PvP est séléctionner:
                        self.mode_de_jeu = 'PvP'
                        #Chaque équipe choisie ses unitées:
                        self.team1_units = self.selectionner_unites("Equipe 1")
                        self.team2_units = self.selectionner_unites("Equipe 2")
                        mode_choisi = True
                    elif event.key == pygame.K_2:
                        #Si le mode PvE est choisi:
                        self.mode_de_jeu = 'PvE'
                        #Le joueur sélectionne ses unités et les unités énnemies sont choisies aléatoirement:
                        self.team1_units = self.selectionner_unites("Joueur")
                        self.enemy_units = [random.choice([Sorcier, Guerrier, Archer])(x, y, 'Ennemi') for x, y in self.down_coords]
                        mode_choisi = True
                    elif event.key == pygame.K_3:
                        #Si l'utilisateur ne souhaite plus jouer:
                        self.mode_de_jeu = 'Quit'
                        mode_choisi = True
                        #La variable globale GAME_CONTINUE est placée à False et permettera au jeu de se fermé.
                        GAME_CONTINUE = False
        #On concatène les listes contenant les unités des joueurs (necessair pour des tests ultérieurs)
        self.player_units = self.team1_units + self.team2_units 
        #On redefinit la liste d'effets à une liste vide (pour ne plus avoir les effets de la partie précedente):
        self.current_effects = []
        
    def selectionner_unites(self, team):
        """Permet à un joueur de sélectionner 3 unités."""
        units = []
        #Pour chaque unité (parmis les 3 disponnibles):
        for i in range(3):
            selection_made = False
            while not selection_made:
                #L'utilisateur à le choix entre Socier, Archer et Guerrier:
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
                        #Il choisi l'unité qu'il souhaite intégrer à son équipe grâce au boution 1, 2, et 3.
                        #Selon l'équipe, des coordonnées sont attribuées aux unités:
                        if team == "Equipe 1" or team =="Joueur":
                            #En haut de l'écran pour l'équipe 1:
                            x, y = self.up_coords[i]
                        elif team == "Equipe 2" or team == "Ennemi":
                            #En bas pour l'équipe 2
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
        #Pour chaque unité dans l'équipe du joueur:
        for selected_unit in turn_units:
            has_acted = False #On remet l'indicateur d'action à False
            selected_unit.is_selected = True #Et l'indicateur de séléction à True
            mvmt_cpt = selected_unit.speed #Pour gérer les déplacements des unités selon leur vitesse.
            friend_loop_check = False #Indicateur de mauvaise séléction de cible (alliée), utile dans la gestion de ce cas.
            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
            while not has_acted:
                if friend_loop_check:
                    friend_loop_check = False #on remet cet indicateur à False pour que l'unité puisse essayer d'agir à nouveau
                #On verifie qu'il reste des unités dans les équipes, afin de bien sortir du jeu en cas de victoire/défaite.
                if not self.enemy_units and (not self.team1_units or not self.team2_units):
                    return
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    #L'utilisateur peut choisir de déplacer son unité en 4-connexité:
                    move_key = False
                    draw_text(self.screen, "Realisez une action!", (10, HEIGHT + 10))
                    pygame.display.flip()
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                            move_key = True
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                            move_key = True
                        elif event.key == pygame.K_UP:
                            dy = -1
                            move_key = True
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                            move_key = True
                        #Si l'unité peut encore de déplacer:
                        if mvmt_cpt >= 0 and move_key == True:
                            #Elle se déplace et le compteur est décremnté de 1:
                            selected_unit.move(dx, dy, self.obstacles, self.water_zones, self.screen)
                            mvmt_cpt -= 1  # Reduce the movement counter
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                        #Si elle ne peut plus se déplacer:
                        elif mvmt_cpt < 0:
                            #On affiche un message:
                            if (event.key != pygame.K_s) and (event.key != pygame.K_ESCAPE):
                                draw_text(self.screen, "Vous ne pouvez plus vous déplacer.", (10, HEIGHT + 10))
                                pygame.display.flip()
                                pygame.time.wait(500)
                            #On verifie que l'unité soit encore en vie (cas où l'unité serait tombée à l'eau)
                            if selected_unit in turn_units and selected_unit.health <= 0:
                                #Si c'est le cas, l'unité est enlevée d ela liste de l'équipe.
                                has_acted = True
                                selected_unit.is_selected = False #On remet l'indicateur de sélection à False
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                        #L'utilisateur peut choisir d'utiliser l'attaque basique et de terminer son tour:
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                #Si lun ennemi est à portée, l'unité attaque:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                            has_acted = True #L'indicateur d'action est placé à True
                            selected_unit.is_selected = False #Celui de séléction à False
                        #Si l'utilisateur choisi d'utiliser une compétence d'unité:
                        elif event.key == pygame.K_s:
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                            #Un menu contenant les compétences disponibles est afiché:
                            draw_text(self.screen, "Compétences disponibles :", (10, HEIGHT + 10))
                            for i, skill in enumerate(selected_unit.skills):
                                draw_text(self.screen, f"{i + 1}. {skill.nom}", (10, HEIGHT + 50 + i * 30))
                            pygame.display.flip()
                            skill_selected = False
                            #L'utilisateur peut alors choisir quelle compétence utiliser.
                            while not skill_selected:
                                #La verification de tentative d'attaque sur un allié est faite, afin de retourner plus haut dans la boucle:
                                if friend_loop_check:
                                    break
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:
                                            skill_selected = True
                                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                            draw_text(self.screen, "", (10, HEIGHT + 10))
                                            pygame.display.flip()
                                            pygame.time.wait(5)
                                            break
                                        #On prévoit 9 compétences maximums, en réalité seulement 2 sont actuellement disponnibles par type d'unité:
                                        if pygame.K_1 <= event.key <= pygame.K_9:
                                            skill_index = event.key - pygame.K_1
                                            if 0 <= skill_index < len(selected_unit.skills):
                                                #Lorsque la compétence à été choisie:
                                                chosen_skill = selected_unit.skills[skill_index]
                                                skill_selected = True #L'indicateur est placé a True
                                                #L'utilisateur doit maintenant choisir une cible:
                                                flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                draw_text(self.screen, "Cliquez sur un ennemi pour choisir une cible.", (10, HEIGHT + 10))
                                                pygame.display.flip()

                                                cible_choisie = False
                                                while not cible_choisie:
                                                    #Test sur l'attaque alliée, pour remonter plus haut
                                                    if friend_loop_check:
                                                        break
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            exit()
                                                        if event.type == pygame.KEYDOWN:    
                                                            if event.key == pygame.K_ESCAPE:
                                                                skill_selected = True
                                                                cible_choisie = True
                                                                flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                draw_text(self.screen, "", (10, HEIGHT + 10))
                                                                pygame.display.flip()
                                                                pygame.time.wait(5)
                                                                break
                                                        #L'utilisateur doit cliquer sur sa cible, les coordonnées sont alors récupérées:
                                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                            mx, my = pygame.mouse.get_pos()
                                                            grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                                                
                                                            #Si la cible est une unité alliée:
                                                            for friendly in turn_units:
                                                                if friendly.x == grid_x and friendly.y == grid_y:
                                                                    flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                    draw_text(self.screen, "Vous ne pouvez pas attaquer votre propre unité!", (10, HEIGHT + 10))
                                                                    pygame.display.flip()
                                                                    pygame.time.wait(300)
                                                                    friend_loop_check = True #L'indicateur est placé à True
                                                                    break
                                                            #Si la cible est une unité de joueur:
                                                            for unit in self.player_units:
                                                                #Et si elle n'est pas dans l'équipe:
                                                                if unit not in turn_units and unit.x == grid_x and unit.y == grid_y:
                                                                    flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                    #La compétence est utilisée:
                                                                    if selected_unit.use_skill(unit, chosen_skill, self.screen):
                                                                        has_acted = True
                                                                    pygame.time.wait(300)
                                                                    #Si la comptétence possède un effet, il est appliqué:
                                                                    if chosen_skill.effet is not None:
                                                                        self.apply_effect(unit, chosen_skill)
                                                                    cible_choisie = True
                                                                    selected_unit.is_selected = False
                                                                    break
                                                
                                                            #S la cible est une unité ennemie (PvE):
                                                            for enemy in self.enemy_units:
                                                                if enemy.x == grid_x and enemy.y == grid_y:
                                                                    flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                                                                    #La compétence est utilisée:
                                                                    if selected_unit.use_skill(unit, chosen_skill, self.screen):
                                                                        has_acted = True
                                                                    pygame.time.wait(300)
                                                                    #Et l'effet appliqué si besoin:
                                                                    if chosen_skill.effet is not None:
                                                                        self.apply_effect(enemy, chosen_skill)
                                                                    cible_choisie = True
                                                                    has_acted = True 
                                                                    selected_unit.is_selected = False #L'unité est déselectionnée
                                                                    break       
                        #L'utilisateur peut choisir d'afficher plus d'informations à propos d'une unité (en cliquant dessus):
                        elif event.key == pygame.K_i:
                            self.disp_info()
        self.check_death()
        flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
        
        
    def check_death(self):
        for unit in self.team1_units + self.team2_units + self.enemy_units:
            if unit.health <= 0:
                if unit in self.enemy_units:
                    self.enemy_units.remove(unit)
                elif unit in self.player_units:
                    if unit in self.team1_units:
                        self.team1_units.remove(unit)
                    if unit in self.team2_units:
                        self.team2_units.remove(unit)
                    self.player_units.remove(unit)
        
                         
    def disp_info(self):
        """"Affichage d'information d'une unité"""
        flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
        #Le message indiquant que l'utilisateur doit sélectionner une unité est affiché:
        draw_text(self.screen, "Cliquez sur une cible pour obtenir des informations", (10, HEIGHT + 10))
        pygame.display.flip()
        cible_choisie = False
        #Tant que la cible n'a pas été choisie:
        while not cible_choisie:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                #On récupère les coordonnées du clique:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                    #Si ces coordonnées correspondent à une unité:
                    for target in (self.enemy_units + self.player_units):
                        if target.x == grid_x and target.y == grid_y:            
                            flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
                            #L'information est affichée:
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
                enemy.move(dx, dy, self.obstacles, self.water_zones, self.screen)

                # Attaque si possible
                if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                    enemy.attack(target)
                    """if target.health <= 0:
                        self.team1_units.remove(target)
                        self.player_units.remove(target)
                if enemy.health <= 0:
                    self.enemy_units.remove(enemy)"""
        self.check_death()

    def check_end_game(self):
        """Vérifie les conditions de fin de partie."""
        #Selon les modes de jeu, la gestion est diférente:
        #Si le mode PvP a été sélectioné:
        if self.mode_de_jeu == 'PvP':
            #L'équipe gagnante est affiché:
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
        #si le mod ePvE a été sélectionné:
        elif self.mode_de_jeu == 'PvE':
            #Si le joueur à gagné:
            if not self.enemy_units:
                draw_text(self.screen, "Vous avez gagné!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(0, 255, 0))
                pygame.display.flip()
                pygame.time.wait(1500)
                return True
            #Si il a perdu:
            if not self.team1_units:
                draw_text(self.screen, "Vous avez perdu!", (WIDTH // 2 - 100, HEIGHT // 2), size=50, color=(255, 0, 0))
                pygame.display.flip()
                pygame.time.wait(1500)
                return True
        return False

    def apply_effect(self, target, skill):
        """Application des effets de compétence sur les emplacements du grid."""
        affected_cells = [] #La liste des emplacements afféctés
        if skill.aoe_radius == 1:  # Pour un rayon d'effet de 1 (ex: Fleche Empoisonée)
            affected_cells.append((target.x, target.y))
        elif skill.aoe_radius > 1:  # Pour un rayon plus grand que 1 (ex: 3 pour Boule de feu)
            # L'effet est appliqué selon son rayon autour de la cible.
            for dx in range(-skill.aoe_radius+1, skill.aoe_radius):
                for dy in range(-skill.aoe_radius+1, skill.aoe_radius):
                    x = target.x + dx
                    y = target.y + dy
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        affected_cells.append((x, y))
        #Si l'emplacement à déja été affecté par un effet:
        for x, y in affected_cells:
            new_effect = skill.effet.__class__()  # Une nouvelle instance de l'effet est créee
            new_effect.effectTTL = skill.effet.effectTTL  # On place sa durée de vie à celle de l'ancient effet
            #Cela permet de ne pas avoir plusieur effets superposés
            self.current_effects.append(((x, y), new_effect))
            #Deprec: l'effet est appliqué à l'unité; Gestion des effets par emplacement plutot que par unité affectée (plus facile ainsi)
            #Ask to remove:
            for unit in self.player_units + self.enemy_units:
                if unit.x == x and unit.y == y:
                    new_effect.apply_effect(unit)
        self.check_death()
        flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
        

    def update_effects(self):
        """Mise a jour des durée de vie des effets, et application des effets sur les unités."""
        #Pour chaque effet dans la liste d'effets actuels:
        for (x, y), effect in self.current_effects[:]:
            for unit in self.player_units + self.enemy_units:
                if unit.x == x and unit.y == y:
                    #L'effet est appliqué si l'unité est à un de ses emplacements
                    effect.apply_effect(unit)
            #Réduction de la durée de vie de l'effet
            effect.effectTTL -= 1

        #Si la durée de vie de l'effet a expiré, l'effet est enlevé de la liste:
        self.current_effects = [((x, y), effect) for (x, y), effect in self.current_effects if effect.effectTTL > 0]
        self.check_death()
        flip_display(self.screen, self.player_units, self.enemy_units, self.water_zones, self.obstacles, self.current_effects)
        
    def handle_turns(self):
        """Gestion des tours selon le mode de jeu """
        #Si le mode PvP est sélectionné:
        if self.mode_de_jeu == "PvP":
            #Chaque équipe joue son tour:
            self.handle_player_turn(self.team1_units)
            self.handle_player_turn(self.team2_units)
        #Si PvE est sélectionné:
        elif self.mode_de_jeu == "PvE":
            #Le jouer et l'IA jouent:
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
        # On test la valeur de GAME_CONTINUE (gestion du mode Quit)
        if not GAME_CONTINUE:
            #Si l'utilisateur ne désire plus jouer, pygame est fermé ainsi que le programme principal.
            pygame.quit()
            exit()
        # Boucle principale du jeu
        while not game.check_end_game():
            #On gère le tour par tour:
            game.handle_turns()
            #Et les effets:
            game.update_effects()
            flip_display(screen, game.player_units, game.enemy_units, game.water_zones, game.obstacles, game.current_effects)

if __name__ == "__main__":
    main()
