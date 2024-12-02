from constants import GRID_SIZE  # Importation de GRID_SIZE

class Movement:
    def __init__(self, unit, obstacles, water_zones, units):
        self.unit = unit
        self.obstacles = obstacles
        self.water_zones = water_zones
        self.units = units

    def move(self, dx, dy):
        """Déplace l'unité selon sa vitesse."""
        if not self.unit.is_alive:
            return False

        for _ in range(self.unit.speed):  # Se déplace selon la vitesse de l'unité
            new_x = self.unit.x + dx
            new_y = self.unit.y + dy

            # Vérifie si la nouvelle position est valide
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in self.obstacles:
                self.unit.x = new_x
                self.unit.y = new_y

                # Vérifie si l'unité tombe dans une zone d'eau
                if (self.unit.x, self.unit.y) in self.water_zones:
                    print(f"L'unité de l'équipe {self.unit.team} est tombée dans l'eau à ({self.unit.x}, {self.unit.y}) et est morte !")
                    self.unit.health = 0
                    self.unit.is_alive = False
                    return True
            else:
                return False  # Si une case est bloquée, l'unité ne se déplace pas

        return False
