import pygame
import sys
import os
import game_logic  # Import the game_logic module

# Colors
white = (255, 255, 255)

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

# Font settings
font = pygame.font.Font(None, 32)

# Game state
class GameState:
    MainMenu, InGame, Paused = range(3)

game_state = GameState.MainMenu

# Function to display the main menu
def main_menu():
    global game_state
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if game_state == GameState.MainMenu:
                    if 300 <= x <= 500 and 150 <= y <= 200:
                        # Start Game button clicked
                        game_logic.run(screen, game_logic.world_width, game_logic.world_height, game_logic.num_enemies, game_logic.num_structures, game_logic.num_terrain)
                    elif 300 <= x <= 500 and 550 <= y <= 600:
                        pygame.quit()
                        sys.exit()
                elif game_state == GameState.Paused:
                    if 300 <= x <= 500 and 150 <= y <= 200:
                        # Resume Game button clicked
                        game_state = GameState.InGame
                    elif 300 <= x <= 500 and 550 <= y <= 600:
                        pygame.quit()
                        sys.exit()

        # Draw the background image stretched across the entire screen
        screen.blit(background_image, (0, 0))

        # Create buttons
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(300, 150, 200, 50))
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(300, 550, 200, 50))

        # Add button labels based on game state
        if game_state == GameState.MainMenu:
            start_text = font.render("Start Game", True, (255, 255, 255))
        elif game_state == GameState.Paused:
            start_text = font.render("Resume Game", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        
        # Position button labels
        screen.blit(start_text, (350, 160))
        screen.blit(quit_text, (350, 560))

        pygame.display.update()
        clock.tick(60)

#if __name__ == "__main__":
    main_menu()
