import pygame
import sys
import pickle
import subprocess  # Import the subprocess module for running external scripts

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D RPG Game - Main Menu")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font settings
font = pygame.font.Font(None, 100)
font_color = black

# Background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Main menu options
options = [
    "Start New Game",
    "Load Game",
    "Options",
    "Quit"
]

# Selected option
selected_option = 0

# Game state (you can add more game state variables here)
game_state = None

# Function to save game state
def save_game_state():
    with open("game_state.pkl", "wb") as file:
        pickle.dump(game_state, file)

# Function to load game state
def load_game_state():
    try:
        with open("game_state.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

# Main menu function
def main_menu():
    global selected_option  # Declare selected_option as a global variable

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the "Start New Game" button
                start_button_rect = pygame.Rect(screen_width / 2 - 150, 200, 300, 100)
                if start_button_rect.collidepoint(event.pos):
                    # Start New Game
                    game_state = None  # Initialize a new game state

                    # Launch game_logic.py using subprocess
                    subprocess.Popen(["python", "game_logic.py"])

        # Check for key presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            selected_option = (selected_option + 1) % len(options)
        elif keys[pygame.K_UP]:
            selected_option = (selected_option - 1) % len(options)
        elif keys[pygame.K_RETURN]:
            # Handle selected option
            if selected_option == 1:
                # Load Game
                game_state = load_game_state()
                if game_state is None:
                    print("No saved game found.")
            elif selected_option == 2:
                # Options (Replace with your game logic)
                pass
            elif selected_option == 3:
                # Save and Quit the game
                if game_state:
                    save_game_state()
                running = False

        # Clear the screen
        screen.fill(white)

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Draw menu options
        for i, option in enumerate(options):
            text = font.render(option, True, font_color)
            text_rect = text.get_rect(center=(screen_width / 2, 200 + i * 100))
            screen.blit(text, text_rect)

        # Highlight the selected option
        text = font.render(options[selected_option], True, white)
        text_rect = text.get_rect(center=(screen_width / 2, 200 + selected_option * 100))
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.update()

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
