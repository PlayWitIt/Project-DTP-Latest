import pygame
import os

class HouseInterior:
    def __init__(self):
        # You can define attributes for the house interior here
        # For example, you might have descriptions, objects, or interactions
        self.description = "You are inside a cozy home."
        self.objects = []
        self.interior_surface = None  # Surface to render the interior
        self.in_interior = False  # Flag to track if the player is inside the house

    def enter(self):
        # Implement what happens when the player enters the house
        self.in_interior = True  # Set the flag to True when entering
        print(self.description)
        self.show_objects()
        # You can add more interactions or actions here

    def show_objects(self):
        if self.objects:
            print("You see the following objects in the house:")
            for obj in self.objects:
                print(f"- {obj}")
        else:
            print("The house is empty.")

    def exit(self):
        # Implement what happens when the player exits the house
        self.in_interior = False  # Set the flag to False when exiting

    def render_interior(self):
        # Create a surface for rendering the interior
        interior_width = 800  # Adjust to your interior dimensions
        interior_height = 600  # Adjust to your interior dimensions
        self.interior_surface = pygame.Surface((interior_width, interior_height))
        self.interior_surface.fill((200, 200, 200))  # Set interior background color

        # Placeholder for rendering objects in the house
        for obj in self.objects:
            obj.render(self.interior_surface)  # Call the rendering method for each object

        # You can add more rendering elements as needed

    def render(self, screen, character_x, character_y):
        if self.in_interior:
            # Render interior when inside the house
            if self.interior_surface is None:
                self.render_interior()  # Create the interior surface if it doesn't exist

            # Render the interior surface onto the main screen
            screen.blit(self.interior_surface, (0, 0))

        else:
            # Clear the screen when not in the house
            screen.fill((255, 255, 255))

            # Render player (as a red rectangle) in the outside world
            pygame.draw.rect(screen, (255, 0, 0), (character_x, character_y, 50, 50))  # Red rectangle for the player

            # Load and render the controls image (D-pad)
            controls_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'dpad.png'))
            # Adjust the Y-coordinate to position the D-pad image higher up
            screen.blit(controls_image, (10, 10))  # Adjust position as needed

        # Don't forget to update the display
        pygame.display.flip()
