import random
import pygame

class BlackMass:
    BLACK_MASS_SIZE = 1
    GROW_INTERVAL = 1
    CHUNK_SIZE = 1

    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.black_mass = set()
        self.grow_timer = 0
        self.growth_enabled = True  # A flag to enable/disable growth

        center_x = world_width // 2
        center_y = world_height // 2
        self.black_mass.add((center_x, center_y))

        self.render_surface = pygame.Surface((world_width, world_height), pygame.SRCALPHA)
        self.render_surface.fill((0, 0, 0, 0))  # Use transparent black

    def grow(self):
        if not self.growth_enabled:
            return  # Growth is disabled, so just return

        x, y = random.choice(list(self.black_mass))
        chunk_size_x = random.randint(1, self.CHUNK_SIZE)
        chunk_size_y = random.randint(1, self.CHUNK_SIZE)

        for i in range(chunk_size_x):
            for j in range(chunk_size_y):
                new_x, new_y = x + i, y + j

                if 0 <= new_x < self.world_width and 0 <= new_y < self.world_height:
                    self.black_mass.add((new_x, new_y))

    def update(self):
        self.grow_timer += 10
        if self.grow_timer >= self.GROW_INTERVAL:
            self.grow()
            self.grow_timer = 0

        self.render_surface.fill((0, 0, 0, 0))  # Use transparent black
        for x, y in self.black_mass:
            pygame.draw.circle(self.render_surface, (0, 0, 0), (x, y), self.BLACK_MASS_SIZE)

    def get_black_mass_positions(self):
        return self.black_mass

    def draw(self, screen, camera):
        screen.blit(self.render_surface, (-camera.camera.x, -camera.camera.y))

    def enable_growth(self):
        self.growth_enabled = True

    def disable_growth(self):
        self.growth_enabled = False