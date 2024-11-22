import pygame
import random

class Corruption:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.corruption_map = [[False for _ in range(world_width)] for _ in range(world_height)]
        self.corruption_color = (0, 0, 0)  # Black color
        self.spread_chance = 0.01  # Probability of corruption spreading

    def update(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                if self.corruption_map[y][x]:
                    # Corruption already present at this location
                    continue
                
                # Check neighboring cells for corruption
                neighbors = self.get_neighbors(x, y)
                for nx, ny in neighbors:
                    if self.corruption_map[ny][nx] and random.random() < self.spread_chance:
                        # Spread corruption to this cell
                        self.corruption_map[y][x] = True
                        break

    def draw(self, screen):
        for y in range(self.world_height):
            for x in range(self.world_width):
                if self.corruption_map[y][x]:
                    # Draw a black square to represent corruption
                    pygame.draw.rect(screen, self.corruption_color, (x, y, 1, 1))

    def get_neighbors(self, x, y):
        # Returns a list of neighboring cell coordinates
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                # Check if the neighbor is within bounds
                if 0 <= nx < self.world_width and 0 <= ny < self.world_height:
                    neighbors.append((nx, ny))
        return neighbors

    def has_consumed_map(self):
        # Check if corruption has consumed a significant portion of the map
        total_cells = self.world_width * self.world_height
        corrupted_cells = sum(row.count(True) for row in self.corruption_map)
        corruption_ratio = corrupted_cells / total_cells
        return corruption_ratio >= 0.8  # Adjust this threshold as needed
