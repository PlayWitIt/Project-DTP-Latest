#house_interior.py

import pygame
from structures import Structure

# Define the dimensions of the house interior
house_interior_width = 400
house_interior_height = 400

# Create a class for the house interior map
class HouseInteriorMap:
    def __init__(self):
        self.width = house_interior_width
        self.height = house_interior_height
        self.background_color = (255, 255, 255)  # White background color
        self.structures = []  # List to store structures in the house interior

    # Method to add structures to the house interior
    def add_structure(self, structure):
        self.structures.append(structure)

    # Method to render the house interior
    def render(self, screen):
        # Fill the interior with the background color
        screen.fill(self.background_color)

        # Draw structures in the interior
        for structure in self.structures:
            structure.draw(screen)
