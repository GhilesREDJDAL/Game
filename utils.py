#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
Created on Thu Dec 5 16:32:40 2024

@author: seb 
"""

import pygame
from Constantes import WATER_BLUE, WHITE ,GRAY, BLACK, WIDTH, HEIGHT, CELL_SIZE, GRID_SIZE, MARGIN_BOTTOM

# On charge les images utilisées pour l'environnement (herbe, eau et obstacles)
grass_image = pygame.image.load('images/grass.png')
water_image = pygame.image.load('images/water.png')
obstacle_image = pygame.image.load('images/stone.png')

# On met les images à la bonne échelle.
grass_image = pygame.transform.scale(grass_image, (CELL_SIZE, CELL_SIZE))
water_image = pygame.transform.scale(water_image, (CELL_SIZE, CELL_SIZE))
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
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

    # Affiche les unités
    for unit in player_units + enemy_units:
        unit.draw(screen)

    # Affiche les zones d'eau
    for x, y in water_zones:
        screen.blit(water_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Affiche les obstacles
    for x, y in obstacles:
        screen.blit(obstacle_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Affiche les objets
    for obj in object_list:
        obj.draw(screen)
        
    # Affiche les effets à l'écran
    draw_effects(screen, current_effects)

    # Affiche les messages en bas
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, HEIGHT, WIDTH, MARGIN_BOTTOM))
    draw_text(screen, "Pour realisez une action:", (10, HEIGHT + MARGIN_BOTTOM - 90))
    draw_text(screen, " - Utilisez les touches directionnelles pour vous déplacer.", (10, HEIGHT + MARGIN_BOTTOM -60))
    draw_text(screen, " - Utilisez la touche 'S' utiliser une compétence", (10, HEIGHT + MARGIN_BOTTOM - 30))
    pygame.display.flip()
    # Rafraîchit l'écran
    pygame.display.flip()
    
def draw_effects(screen, current_effects):
    """Affiche tous les effets actuels à l'écran."""
    global img_frame_index, last_update_time # On récupère les variables globales 
    current_time = pygame.time.get_ticks()
    for (x, y), effect in current_effects:
        # Exemple : Affiche une animation selon les effets
        if effect.name == "Feu":
            if current_time - last_update_time > frame_rate: 
                last_update_time = current_time 
                img_frame_index = (img_frame_index + 1) % len(feu_frames) # On affiche la trame courante
            frame = feu_frames[img_frame_index] 
            screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))
            #color = (255, 69, 0, 128)  # Orange avec transparence
        elif effect.name == "Poison":
            if current_time - last_update_time > frame_rate: 
                last_update_time = current_time 
                img_frame_index = (img_frame_index + 1) % len(poison_frames) # On affiche la trame courante
            frame = poison_frames[img_frame_index] 
            screen.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))
            #color = (128, 0, 128, 128)  # Violet avec transparence
        elif effect.name == "Soin":
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
    

