import pygame
from constants import BLACK, CELL_SIZE, FOREST_BACKGROUND_IMAGE, STONE_IMAGE, WATER_IMAGE, BONUS_IMAGE, RED

# Classe pour gérer les animations
class AnimationManager:
    def __init__(self, screen):
        self.screen = screen

    def animate_movement(self, unit, dx, dy, obstacles, water_zones, bonuses, units):
        """Anime le déplacement de l'unité."""
        start_x = unit.x * CELL_SIZE
        start_y = unit.y * CELL_SIZE
        end_x = (unit.x + dx) * CELL_SIZE
        end_y = (unit.y + dy) * CELL_SIZE
        steps = 10
        for step in range(steps):
            x = start_x + (end_x - start_x) * step / steps
            y = start_y + (end_y - start_y) * step / steps
            self.screen.fill(BLACK)
            self.draw_background()
            self.draw_grid(obstacles, water_zones, bonuses)
            self.draw_units(units)
            self.screen.blit(unit.image, (x, y))
            pygame.display.flip()
            pygame.time.wait(50)

    def animate_attack(self, attacker, defender, obstacles, water_zones, bonuses, units):
        """Anime l'attaque de l'unité."""
        self.screen.fill(BLACK)
        self.draw_background()
        self.draw_grid(obstacles, water_zones, bonuses)
        self.draw_units(units)
        pygame.draw.line(self.screen, RED,
                         (attacker.x * CELL_SIZE + CELL_SIZE // 2, attacker.y * CELL_SIZE + CELL_SIZE // 2),
                         (defender.x * CELL_SIZE + CELL_SIZE // 2, defender.y * CELL_SIZE + CELL_SIZE // 2),
                         5)
        pygame.display.flip()
        pygame.time.wait(200)

    def animate_death(self, unit, obstacles, water_zones, bonuses, units):
        """Anime la mort de l'unité."""
        for alpha in range(255, 0, -10):
            self.screen.fill(BLACK)
            self.draw_background()
            self.draw_grid(obstacles, water_zones, bonuses)
            self.draw_units(units)
            unit.image.set_alpha(alpha)
            self.screen.blit(unit.image, (unit.x * CELL_SIZE, unit.y * CELL_SIZE))
            pygame.display.flip()
            pygame.time.wait(50)

    def animate_bonus(self, unit, obstacles, water_zones, bonuses, units):
        """Anime le bonus de l'unité."""
        for alpha in range(0, 255, 10):
            self.screen.fill(BLACK)
            self.draw_background()
            self.draw_grid(obstacles, water_zones, bonuses)
            self.draw_units(units)
            bonus_image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            bonus_image.fill((0, 255, 0, alpha))
            self.screen.blit(bonus_image, (unit.x * CELL_SIZE, unit.y * CELL_SIZE))
            pygame.display.flip()
            pygame.time.wait(50)

    def draw_background(self):
        self.screen.blit(FOREST_BACKGROUND_IMAGE, (0, 0))

    def draw_grid(self, obstacles, water_zones, bonuses):
        # Affichage des obstacles
        for x, y in obstacles:
            self.screen.blit(STONE_IMAGE, (x * CELL_SIZE, y * CELL_SIZE))

        # Affichage des zones d'eau
        for x, y in water_zones:
            self.screen.blit(WATER_IMAGE, (x * CELL_SIZE, y * CELL_SIZE))

        # Affichage des bonus
        for x, y in bonuses:
            self.screen.blit(BONUS_IMAGE, (x * CELL_SIZE, y * CELL_SIZE))

    def draw_units(self, units):
        for unit in units:
            unit.draw(self.screen)
