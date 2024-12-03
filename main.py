import pygame
from game import Game
from constants import WIDTH, HEIGHT, FPS

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strategic Battle Game")
clock = pygame.time.Clock()

# Création du jeu
game = Game(screen)

# Boucle de jeu
while True:
    game.handle_player_turn()
    game.handle_enemy_turn()
    game.check_game_over()

    clock.tick(FPS)
 