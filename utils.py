#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:32:40 2024

@author: seb
"""
import pygame
from Constantes import WATER_BLUE, WHITE ,GRAY, BLACK, WIDTH, HEIGHT, CELL_SIZE, MARGIN_BOTTOM

def draw_text(screen, text, position, size=30, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    lines = text.split('\n')
    x, y = position
    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += size  # Move down by the font size for the next line

def flip_display(screen, player_units, enemy_units, water_zones, obstacles, current_effects):
    """Affiche le jeu."""
    # Affiche la grille
    screen.fill(BLACK)
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

    # Affiche les unités
    for unit in player_units + enemy_units:
        unit.draw(screen)

    # Affiche les zones d'eau
    for x, y in water_zones:
        pygame.draw.rect(screen, WATER_BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Affiche les obstacles
    for x, y in obstacles:
        pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the effects on the screen
    draw_effects(screen, current_effects)

    # Affiche les messages en bas
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, HEIGHT, WIDTH, MARGIN_BOTTOM))

    # Rafraîchit l'écran
    pygame.display.flip()
    
def draw_effects(screen, current_effects):
    """Draw all current effects on the screen."""
    for (x, y), effect in current_effects:
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