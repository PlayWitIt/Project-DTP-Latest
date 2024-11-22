# camera.py

import pygame

class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, entity):
        # Check if the entity is a pygame.Rect
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        # If it's not a Rect, it's assumed to be a tuple (x, y)
        x, y = entity
        return x - self.camera.x, y - self.camera.y

    def update(self, target_x, target_y):
        # Adjust camera movement to follow the player
        x = target_x - self.screen_width / 2
        y = target_y - self.screen_height / 2

        # Clamp the camera to stay within the world boundaries
        x = max(0, x)  # Left boundary
        y = max(0, y)  # Top boundary
        x = min(self.world_width - self.screen_width, x)  # Right boundary
        y = min(self.world_height - self.screen_height, y)  # Bottom boundary

        self.camera = pygame.Rect(x, y, self.screen_width, self.screen_height)