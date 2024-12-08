import pygame

# Définition des couleurs et des dimensions
GRID_SIZE = 8  # Augmentation de la taille de la grille à 15x15
CELL_SIZE = 60  # Taille des cases en pixels (reste inchangée)
WIDTH = GRID_SIZE * CELL_SIZE  # Largeur de la fenêtre, ajustée à la nouvelle taille de la grille
HEIGHT = GRID_SIZE * CELL_SIZE  # Hauteur de la fenêtre, ajustée à la nouvelle taille de la grille
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WATER_BLUE = (0, 191, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Charger les images pour les cases spéciales
STONE_IMAGE = pygame.image.load("images/stone.png")
WATER_IMAGE = pygame.image.load("images/water.png")
BONUS_IMAGE = pygame.image.load("images/bonus.png")
FOREST_BACKGROUND_IMAGE = pygame.image.load("images/forest_background.png")

# Redimensionner les images pour correspondre à la taille des cellules
STONE_IMAGE = pygame.transform.scale(STONE_IMAGE, (CELL_SIZE, CELL_SIZE))
WATER_IMAGE = pygame.transform.scale(WATER_IMAGE, (CELL_SIZE, CELL_SIZE))
BONUS_IMAGE = pygame.transform.scale(BONUS_IMAGE, (CELL_SIZE, CELL_SIZE))
FOREST_BACKGROUND_IMAGE = pygame.transform.scale(FOREST_BACKGROUND_IMAGE, (WIDTH, HEIGHT))
