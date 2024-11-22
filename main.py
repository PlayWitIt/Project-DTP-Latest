import os
import pygame
import game_logic
import sys
import menu  # Import the menu module

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Your New Window Title")

# Load background image and resize it to match the screen's dimensions
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the D-pad image
dpad_image = pygame.image.load("Dpad.png")

# Font settings
font = pygame.font.Font(None, 32)

# Game state
class GameState:
    MainMenu, InGame, Paused = range(3)

game_state = GameState.MainMenu

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check the game state and run the appropriate logic
    if game_state == GameState.MainMenu:
        menu.main_menu()  # Run the main menu logic from the menu module
        game_state = GameState.InGame  # Start the game after main menu
    elif game_state == GameState.Paused:
        # Handle paused state here if needed
        pass
    elif game_state == GameState.InGame:
        game_logic.run(
            screen,
            game_logic.world_width,
            game_logic.world_height,
            game_logic.num_enemies,
            game_logic.num_structures,
            game_logic.num_terrain
        )
        game_state = GameState.Paused  # Set to Paused to pause the game

    # Draw the background image stretched across the entire screen
    screen.blit(background_image, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()