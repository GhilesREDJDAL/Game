#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
Created on Thu Dec 5 16:32:40 2024

@author: seb 
"""

import pygame
from Constantes import WATER_BLUE, WHITE ,GRAY, BLACK, WIDTH, HEIGHT, CELL_SIZE, GRID_SIZE, MARGIN_BOTTOM

# On charge les images utilisées pour l'environnement (herbe, eau et obstacles)
grass_image = pygame.image.load('images/textures/grass.png')
water_image = pygame.image.load('images/textures/water_mc.png')
water_image_up = pygame.image.load('images/textures/water_tc.png')
water_image_uleft = pygame.image.load('images/textures/water_tl.png')
water_image_uright = pygame.image.load('images/textures/water_tr.png')
water_image_down = pygame.image.load('images/textures/water_bc.png')
water_image_dleft = pygame.image.load('images/textures/water_bl.png')
water_image_dright = pygame.image.load('images/textures/water_br.png')
water_image_left = pygame.image.load('images/textures/water_ml.png')
water_image_right = pygame.image.load('images/textures/water_mr.png')
obstacle_image = pygame.image.load('images/textures/rock_1.png')

# On met les images à la bonne échelle.
grass_image = pygame.transform.scale(grass_image, (CELL_SIZE, CELL_SIZE))
water_image = pygame.transform.scale(water_image, (CELL_SIZE, CELL_SIZE))
water_image_up = pygame.transform.scale(water_image_up, (CELL_SIZE, CELL_SIZE))
water_image_down = pygame.transform.scale(water_image_down, (CELL_SIZE, CELL_SIZE))
water_image_left = pygame.transform.scale(water_image_left, (CELL_SIZE, CELL_SIZE))
water_image_right = pygame.transform.scale(water_image_right, (CELL_SIZE, CELL_SIZE))

water_image_uleft = pygame.transform.scale(water_image_uleft, (CELL_SIZE, CELL_SIZE))
water_image_uright = pygame.transform.scale(water_image_uright, (CELL_SIZE, CELL_SIZE))
water_image_dleft = pygame.transform.scale(water_image_dleft, (CELL_SIZE, CELL_SIZE))
water_image_dright = pygame.transform.scale(water_image_dright, (CELL_SIZE, CELL_SIZE))
obstacle_image = pygame.transform.scale(obstacle_image, (CELL_SIZE, CELL_SIZE))
        

# On charge les images composant l'animation de l'effet Feu
feu_frames = [pygame.image.load(f"images/effects/Feu/feu_{i}.png") for i in range(1, 17)]  # Adjust based on your actual frame files
feu_frames = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in feu_frames]
img_frame_index = 0  # On initialise l'indice de l'image
frame_rate = 100  # Durée par image
last_update_time = pygame.time.get_ticks()  # On récupère le temps du jeu

# On fait pareil pour l'effet Poison
poison_frames = [pygame.image.load(f"images/effects/Poison/poison_{i}.png") for i in range(1, 17)]
poison_frames = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in poison_frames]

# Et pour le Soin:
healing_frames = [pygame.image.load(f"images/effects/Soin/soin_{i}.png") for i in range(1, 17)]
healing_frames = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in healing_frames]

def draw_text(screen, text, position, size=30, color=(255, 255, 255)):
    """Affiche du texte sur l'écran."""
    font = pygame.font.Font(None, size)
    lines = text.split('\n')
    x, y = position
    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += size  # Se déplace vers le bas de la hauteur de la police pour la ligne suivante

def flip_display(screen, player_units, enemy_units, water_zones, obstacles, current_effects, object_list):
    """Affiche le jeu."""
    # Affiche la grille
    screen.fill(BLACK)
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            screen.blit(grass_image, (x, y))

    # Affiche les zones d'eau et les images correspondantes
    for water_case in water_zones:
        wx, wy = water_case.x, water_case.y
        screen.blit(water_image, (wx * CELL_SIZE, wy * CELL_SIZE))
        water_case_pos_list = [(water.x, water.y) for water in water_zones]
	
        # Draw corresponding grass images around water
        if wx > 0 and (wx - 1, wy) not in water_case_pos_list:
            screen.blit(water_image_left, ((wx - 1) * CELL_SIZE, wy * CELL_SIZE))
        if wx < WIDTH // CELL_SIZE - 1 and (wx + 1, wy) not in water_case_pos_list:
            screen.blit(water_image_right, ((wx + 1) * CELL_SIZE, wy * CELL_SIZE))
        if wy > 0 and (wx, wy - 1) not in water_case_pos_list:
            screen.blit(water_image_up, (wx * CELL_SIZE, (wy - 1) * CELL_SIZE))
        if wy < HEIGHT // CELL_SIZE - 1 and (wx, wy + 1) not in water_case_pos_list:
            screen.blit(water_image_down, (wx * CELL_SIZE, (wy + 1) * CELL_SIZE))

        # Draw diagonal grass images
        if wx > 0 and wy > 0 and (wx - 1, wy - 1) not in water_case_pos_list:
            screen.blit(water_image_uleft, ((wx - 1) * CELL_SIZE, (wy - 1) * CELL_SIZE))
        if wx < WIDTH // CELL_SIZE - 1 and wy > 0 and (wx + 1, wy - 1) not in water_case_pos_list:
            screen.blit(water_image_uright, ((wx + 1) * CELL_SIZE, (wy - 1) * CELL_SIZE))
        if wx > 0 and wy < HEIGHT // CELL_SIZE - 1 and (wx - 1, wy + 1) not in water_case_pos_list:
            screen.blit(water_image_dleft, ((wx - 1) * CELL_SIZE, (wy + 1) * CELL_SIZE))
        if wx < WIDTH // CELL_SIZE - 1 and wy < HEIGHT // CELL_SIZE - 1 and (wx + 1, wy + 1) not in water_case_pos_list:
            screen.blit(water_image_dright, ((wx + 1) * CELL_SIZE, (wy + 1) * CELL_SIZE))

    # Affiche les obstacles
    for obst in obstacles:
        ox, oy = obst.x, obst.y
        screen.blit(obstacle_image, (ox * CELL_SIZE, oy * CELL_SIZE))

    # Affiche les objets
    for obj in object_list:
        obj.draw(screen)

    # Affiche les unités
    for unit in player_units + enemy_units:
        unit.draw(screen)
        
    # Affiche les effets à l'écran
    draw_effects(screen, current_effects)

    # Draw the grid lines last
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

    # Affiche les messages en bas
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, HEIGHT, WIDTH, MARGIN_BOTTOM))
    draw_text(screen, "Pour realisez une action:", (10, HEIGHT + MARGIN_BOTTOM - 90))
    draw_text(screen, " - Utilisez les touches directionnelles pour vous déplacer.", (10, HEIGHT + MARGIN_BOTTOM -60))
    draw_text(screen, " - Utilisez la touche 'S' utiliser une compétence", (10, HEIGHT + MARGIN_BOTTOM - 30))

    # Rafraîchit l'écran
    pygame.display.flip()


    
def draw_effects(screen, current_effects):
    """Affiche tous les effets actuels à l'écran."""
    global img_frame_index, last_update_time # On récupère les variables globales 
    current_time = pygame.time.get_ticks()
    for case in current_effects:
        if case.effect:
            x, y = case.x, case.y
            # Exemple : Affiche une animation selon les effets
            if case.effect.name == "Feu":
                if current_time - last_update_time > frame_rate: 
                    last_update_time = current_time 
                    img_frame_index = (img_frame_index + 1) % len(feu_frames) # On affiche la trame courante
                frame = feu_frames[img_frame_index] 
                screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))
                #color = (255, 69, 0, 128)  # Orange avec transparence
            elif case.effect.name == "Poison":
                if current_time - last_update_time > frame_rate: 
                    last_update_time = current_time 
                    img_frame_index = (img_frame_index + 1) % len(poison_frames) # On affiche la trame courante
                frame = poison_frames[img_frame_index] 
                screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))
                #color = (128, 0, 128, 128)  # Violet avec transparence
            elif case.effect.name == "Soin":
                if current_time - last_update_time > frame_rate: 
                    last_update_time = current_time 
                    img_frame_index = (img_frame_index + 1) % len(healing_frames) # On affiche la trame courante
                frame = healing_frames[img_frame_index] 
                screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))
                #color = (0, 255, 0, 128)  # Vert avec transparence
            else:
                continue
"""
        # Crée une surface avec la couleur spécifiée
        overlay = pygame.Surface((CELL_SIZE, CELL_SIZE))
        overlay.set_alpha(128)  # Définit le niveau de transparence
        overlay.fill(color)

        # Dessine la superposition sur la cellule spécifiée
        screen.blit(overlay, (x * CELL_SIZE, y * CELL_SIZE))
"""
def disp_move_range(screen, selected_unit, moves):
    """Affiche la portée de déplacement maximale de l'unité."""
    color = (0, 0, 255, 128)
    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE))
    overlay.set_alpha(128) 
    overlay.fill(color)

    # Calcule les coordonnées accessibles:
    x, y = selected_unit.x, selected_unit.y
    for dx in range(-moves, moves + 1):
        for dy in range(-moves, moves + 1):
            if abs(dx) + abs(dy) <= moves:  # Vérifie la distance de Manhattan
                new_x = x + dx
                new_y = y + dy
                # Vérifie que les nouvelles coordonnées sont dans les limites de la grille
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    if (new_x, new_y) != (x, y):
                        pygame.draw.rect(screen, color, (new_x * CELL_SIZE, new_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3) 
    pygame.display.flip()
    

