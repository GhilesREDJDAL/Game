import pygame
import random
from unit import Knight, Archer, Mage
from constants import WIDTH, HEIGHT, BLACK, GRAY, WATER_BLUE, FPS, CELL_SIZE  # Add CELL_SIZE import

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.reset_game()

    def reset_game(self):
        self.player_units = [
            Knight(0, 0, 'player'),
            Archer(1, 0, 'player'),
            Mage(2, 0, 'player')
        ]
        self.enemy_units = [
            Knight(6, 6, 'enemy'),
            Archer(7, 6, 'enemy'),
            Mage(5, 6, 'enemy')
        ]
        self.obstacles = {(3, 3), (3, 4), (4, 3), (5, 4), (4, 5), (4, 4), (5, 5)}
        self.water_zones = {(2, 2), (6, 2)}

        self.link_movement()

    def link_movement(self):
        for unit in self.player_units + self.enemy_units:
            unit.movement.obstacles = self.obstacles
            unit.movement.water_zones = self.water_zones
            unit.movement.units = self.player_units + self.enemy_units

    def check_game_over(self):
        if not self.player_units:
            print("L'équipe du joueur a perdu !")
            self.display_game_over('enemy')
            return True
        if not self.enemy_units:
            print("L'équipe ennemie a perdu !")
            self.display_game_over('player')
            return True
        return False

    def handle_player_turn(self):
        for selected_unit in list(self.player_units):
            if not selected_unit.is_alive:
                self.player_units.remove(selected_unit)
                continue

            selected_unit.is_selected = True
            self.flip_display()

            has_acted = False
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

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

                        if selected_unit.movement.move(dx, dy):
                            has_acted = True
                            break

                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in list(self.enemy_units):
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if not enemy.is_alive:
                                        print(f"Un ennemi à ({enemy.x}, {enemy.y}) a été tué !")
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

            if self.check_game_over():
                return

    def handle_enemy_turn(self):
        for enemy in list(self.enemy_units):
            if not enemy.is_alive:
                self.enemy_units.remove(enemy)
                continue

            enemy.is_selected = True
            self.flip_display()

            has_acted = False
            while not has_acted:
                # Déplacement et attaque de l'ennemi
                direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                if enemy.movement.move(*direction):
                    has_acted = True

                # Attaquer une unité si à portée
                for player in self.player_units:
                    if abs(enemy.x - player.x) <= 1 and abs(enemy.y - player.y) <= 1:
                        enemy.attack(player)
                        if not player.is_alive:
                            print(f"Un joueur à ({player.x}, {player.y}) a été tué !")
                            self.player_units.remove(player)
                        has_acted = True

            if self.check_game_over():
                return

    def flip_display(self):
        self.screen.fill(BLACK)

        for x, y in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for x, y in self.water_zones:
            pygame.draw.rect(self.screen, WATER_BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()

    def display_game_over(self, winner):
        font = pygame.font.Font(None, 50)
        message = "Vous avez gagné !" if winner == 'player' else "Vous avez perdu !"
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        self.reset_game()
