import pygame

# Initialize Pygame for the start menu module
pygame.init()

# Start menu variables
start_button_rect = pygame.Rect(300, 250, 200, 80)
return_button_rect = pygame.Rect(300, 350, 200, 80)

# Start menu font size
font_size = 48  # Adjust the font size as needed

# Define the font for the start menu
font = pygame.font.Font(None, font_size)

# Function to handle start menu events
def handle_start_menu(screen):
    global game_started

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check for start button press
    if is_point_inside_rect(mouse_pos, start_button_rect):
        pygame.draw.rect(screen, (150, 150, 150), start_button_rect)
        if pygame.mouse.get_pressed()[0]:
            game_started = True

    # Check for return button press
    if is_point_inside_rect(mouse_pos, return_button_rect):
        pygame.draw.rect(screen, (150, 150, 150), return_button_rect)
        if pygame.mouse.get_pressed()[0]:
            game_started = False

    # Draw buttons
    pygame.draw.rect(screen, (200, 200, 200), start_button_rect)
    pygame.draw.rect(screen, (200, 200, 200), return_button_rect)

    # Render button texts
    start_text = font.render("Start Game", True, (0, 0, 0))
    return_text = font.render("Return to Menu", True, (0, 0, 0))

    # Blit button texts onto the screen
    screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 20))
    screen.blit(return_text, (return_button_rect.x + 20, return_button_rect.y + 20))

# Function to check if a point is inside a rectangle
def is_point_inside_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh
