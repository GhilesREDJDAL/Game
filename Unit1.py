import pygame

class Skill:
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def use(self, unit, *args):
        self.action(unit, *args)


class Unit:
    def __init__(self, x, y, health, attack, role):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack
        self.role = role
        self.is_selected = False

        # Initialize skills
        self.skills = [
            Skill("Move", self.move),  # Move skill
            Skill("Attack", self.attack),  # Attack skill
            Skill("Defend", self.defend)  # Defend skill
        ]

    def draw(self, screen):
        # Draw the unit (this will depend on your unit's graphical representation)
        pygame.draw.rect(screen, (255, 0, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy):
        """Move the unit by dx and dy."""
        self.x += dx
        self.y += dy

    def attack(self, target):
        """Attack the target."""
        if target:
            target.health -= self.attack_power
            print(f"{self.role} unit attacks {target.role} unit. {target.role}'s health is now {target.health}.")

    def defend(self):
        """Defend and increase health."""
        self.health += 5
        print(f"{self.role} unit defends. Health increased to {self.health}.")
