from constants import GRID_SIZE

# Classe qui gère le déplacement des unités
class Movement:
    def __init__(self, unit, obstacles, water_zones, units, bonuses):
        self.unit = unit
        self.obstacles = obstacles
        self.water_zones = water_zones
        self.units = units
        self.bonuses = bonuses

    def move(self, dx, dy):
        """Déplace l'unité selon sa vitesse."""
        if not self.unit.is_alive:
            return False

        for _ in range(self.unit.speed):  # Se déplace selon la vitesse de l'unité
            new_x = self.unit.x + dx
            new_y = self.unit.y + dy

            # Vérifie si la nouvelle position est occupée par une autre unité
            if any(u.x == new_x and u.y == new_y and u.is_alive for u in self.units if u != self.unit):
                return False  # Si la position est occupée, l'unité ne se déplace pas

            # Si l'unité est un Mage, ignore les obstacles
            if isinstance(self.unit, self.get_mage_class()):
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    self.unit.x = new_x
                    self.unit.y = new_y
                else:
                    return False  # Si la position est hors limites
            else:
                # Vérifie si la nouvelle position est valide pour les autres unités
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in self.obstacles:
                    self.unit.x = new_x
                    self.unit.y = new_y

                    # Vérifie si l'unité tombe dans une zone d'eau
                    if (self.unit.x, self.unit.y) in self.water_zones:
                        print(f"L'unité de l'équipe {self.unit.team} est tombée dans l'eau à ({self.unit.x}, {self.unit.y}) et est morte !")
                        self.unit.health = 0
                        self.unit.is_alive = False
                        return True

                    # Vérifie si l'unité passe par une case bonus
                    if (self.unit.x, self.unit.y) in self.bonuses:
                        print(f"L'unité de l'équipe {self.unit.team} a trouvé un bonus à ({self.unit.x}, {self.unit.y}) et a gagné de la vie !")
                        self.unit.health += 2  # Augmente la vie de l'unité
                        self.bonuses.remove((self.unit.x, self.unit.y))  # Retire le bonus de la liste

                else:
                    return False  # Si une case est bloquée, l'unité ne se déplace pas

        return False

    def get_mage_class(self):
        from units import Mage
        return Mage
