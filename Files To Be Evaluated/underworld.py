# underworld.py

import pygame

# Dimensions
UNDERWORLD_WIDTH = 800
UNDERWORLD_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Underworld:
    def __init__(self):
        # Create an underworld surface
        self.surface = pygame.Surface((UNDERWORLD_WIDTH, UNDERWORLD_HEIGHT))
        self.surface.fill(BLACK)

    def update(self):
        # Update underworld-specific logic here (e.g., enemy movement, interactions, etc.)
        pass

    def render(self, screen, camera):
        # Render the underworld dimension
        screen.blit(self.surface, (0, 0))

    # You can add methods for handling underworld-specific features, enemies, etc.

# Test the underworld dimension
if __name__ == "__main__":
    pygame.init()

    # Screen settings
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Underworld Test")

    underworld = Underworld()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(RED)  # Fill the screen with a different color for the overworld

        underworld.update()
        underworld.render(screen, None)  # Pass None for camera (no camera movement)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
