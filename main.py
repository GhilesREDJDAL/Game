import pygame
from game import Game
from constants import WIDTH, HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu avec obstacles et zones d'eau")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.check_game_over()
        game.handle_enemy_turn()
        game.check_game_over()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main()
