import pygame
from constants import WIDTH, HEIGHT, FPS
from game import Game

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Stratégie")
clock = pygame.time.Clock()

# Création du jeu
game = Game(screen)

# Boucle principale du jeu
while True:
    game.handle_player_turn()
    game.handle_enemy_turn()
    clock.tick(FPS)

