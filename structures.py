# structures.py
import pygame
import random

# Seed for random generation (None for random seed)
seed = None

# Size settings for each structure and terrain type
house_size = 175
ruins_size = 257
forest_size = 500
mountain_size = 500
river_width = 130
river_length = 450
ocean_width = 1000  # Adjust as needed
ocean_length = 2000  # Adjust as needed
lake_width = 450    # Adjust as needed
lake_length = 850   # Adjust as needed
terrain_size = max(house_size, ruins_size, forest_size, mountain_size, river_width, ocean_width, ocean_length, lake_width, lake_length)

# Probability settings for each structure and terrain type (out of 100)
house_probability = 5
ruins_probability = 1
forest_probability = 30
mountain_probability = 30
river_probability = 10
ocean_probability = 1
lake_probability = 10

# True/False toggles for each structure and terrain type
generate_houses = True
generate_ruins = True
generate_forests = True
generate_mountains = True
generate_rivers = True
generate_oceans = True  # Enable ocean generation
generate_lakes = True    # Enable lake generation

# Base structure class definition
class Structure:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    # Method to draw the structure on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    # Method to define specific interaction for each structure
    def interact(self):
        print("This is a structure.")

# House structure class
class House(Structure):
    def __init__(self, x, y):
        width = house_size
        height = house_size
        color = (255, 200, 200)  # Light red color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for houses
    def interact(self):
        print("You've entered a cozy house!")

# Ruins structure class
class Ruins(Structure):
    def __init__(self, x, y):
        width = ruins_size
        height = ruins_size
        color = (150, 150, 150)  # Gray color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for ruins
    def interact(self):
        print("You've discovered ancient ruins!")

# Base terrain class definition
class Terrain:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    # Method to draw the terrain on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    # Method to define specific behavior for each terrain type
    def interact(self):
        print("This is terrain.")

# Forest terrain class
class Forest(Terrain):
    def __init__(self, x, y):
        width = forest_size
        height = forest_size
        color = (0, 100, 0)  # Dark green color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for forests
    def interact(self):
        print("You've entered a dense forest!")

# Mountain terrain class
class Mountain(Terrain):
    def __init__(self, x, y):
        width = mountain_size
        height = mountain_size
        color = (100, 100, 100)  # Gray color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for mountains
    def interact(self):
        print("You've reached the towering mountains!")

    # Method to check for collision with the player (added for impassable barrier)
    def is_collision(self, player_rect):
        mountain_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return mountain_rect.colliderect(player_rect)

# River terrain class
class River(Terrain):
    def __init__(self, x, y):
        width = river_width
        height = river_length
        color = (0, 0, 255)  # Blue color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for rivers
    def interact(self):
        print("You've encountered a flowing river!")

# Ocean terrain class
class Ocean(Terrain):
    def __init__(self, x, y):
        width = ocean_width
        height = ocean_length
        color = (0, 0, 128)  # Deep blue color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for oceans
    def interact(self):
        print("You've reached the vast ocean!")

# Lake terrain class
class Lake(Terrain):
    def __init__(self, x, y):
        width = lake_width
        height = lake_length
        color = (0, 0, 255)  # Blue color
        super().__init__(x, y, width, height, color)

    # Method to define specific behavior for lakes
    def interact(self):
        print("You've reached a calm lake!")

# Function to generate random structures and terrain
def generate_structures_and_terrain(num_structures, num_terrain, world_width, world_height):
    objects = []

    if seed is not None:
        random.seed(seed)  # Set the random seed if specified

    # Generate structures
    if generate_houses:
        for _ in range(num_structures):
            if random.randint(1, 100) <= house_probability:
                structure_type = House
                instance = structure_type(0, 0)  # Create an instance of the selected structure type
                width = instance.width  # Access the width from the instance
                height = instance.height  # Access the height from the instance
                x = random.randint(0, world_width - width)  # Random x position
                y = random.randint(0, world_height - height)  # Random y position
                structure = structure_type(x, y)
                objects.append(structure)

    if generate_ruins:
        for _ in range(num_structures):
            if random.randint(1, 100) <= ruins_probability:
                structure_type = Ruins
                instance = structure_type(0, 0)  # Create an instance of the selected structure type
                width = instance.width  # Access the width from the instance
                height = instance.height  # Access the height from the instance
                x = random.randint(0, world_width - width)  # Random x position
                y = random.randint(0, world_height - height)  # Random y position
                structure = structure_type(x, y)
                objects.append(structure)

    # Generate terrain
    if generate_forests or generate_mountains or generate_rivers or generate_oceans or generate_lakes:
        for _ in range(num_terrain):
            if generate_forests and random.randint(1, 100) <= forest_probability:
                terrain_type = Forest
            elif generate_mountains and random.randint(1, 100) <= mountain_probability:
                terrain_type = Mountain
            elif generate_rivers and random.randint(1, 100) <= river_probability:
                terrain_type = River
            elif generate_oceans and random.randint(1, 100) <= ocean_probability:
                terrain_type = Ocean
            elif generate_lakes and random.randint(1, 100) <= lake_probability:
                terrain_type = Lake
            else:
                continue  # Skip generating terrain if no type is selected
            instance = terrain_type(0, 0)  # Create an instance of the selected terrain type
            width = instance.width  # Access the width from the instance
            height = instance.height  # Access the height from the instance
            x = random.randint(0, world_width - width)  # Random x position
            y = random.randint(0, world_height - height)  # Random y position
            terrain = terrain_type(x, y)
            objects.append(terrain)

    return objects