# controls.py
import pygame

# Initialize Pygame for the controls module
pygame.init()

# Control variables
left_button_pressed = False
right_button_pressed = False
up_button_pressed = False
down_button_pressed = False

# Define the on-screen control buttons
left_button_rect = pygame.Rect(20, 600 - 120, 100, 100)
right_button_rect = pygame.Rect(140, 600 - 120, 100, 100)
up_button_rect = pygame.Rect(80, 600 - 180, 100, 100)
down_button_rect = pygame.Rect(80, 600 - 60, 100, 100)

# Define the 'b_button_rect'
b_button_rect = pygame.Rect(220, 600 - 120, 100, 100)

# Character speed
default_speed = 5
water_speed_reduction = 0.5  # Adjust this value to control speed reduction in water

# Transparent colors with an alpha value for transparency
transparent_red = (255, 0, 0, 128)  # The last value (128) controls transparency
transparent_blue = (0, 0, 255, 128)  # The last value (128) controls transparency

# Load the Dpad image and resize it
dpad_image = pygame.image.load("Dpad.png")
dpad_image = pygame.transform.scale(dpad_image, (250, 250))

# Calculate the position to center the D-pad image over the control buttons
dpad_x = left_button_rect.centerx - dpad_image.get_width() // 3.75
dpad_y = left_button_rect.centery - dpad_image.get_height() // 1.95

# Function to handle control events and update player position
def handle_controls(player_x, player_y, world_width, world_height, in_water=False):
    global left_button_pressed, right_button_pressed, up_button_pressed, down_button_pressed

    # Check for control button events
    touch_pos = pygame.mouse.get_pos()

    # Check for left button press
    left_button_pressed = is_point_inside_rect(touch_pos, left_button_rect)

    # Check for right button press
    right_button_pressed = is_point_inside_rect(touch_pos, right_button_rect)

    # Check for up button press
    up_button_pressed = is_point_inside_rect(touch_pos, up_button_rect)

    # Check for down button press
    down_button_pressed = is_point_inside_rect(touch_pos, down_button_rect)

    # Calculate speed based on the environment (in water or not)
    speed = default_speed if not in_water else default_speed * water_speed_reduction

    # Update player's position based on touch input and speed
    if left_button_pressed:
        player_x -= speed
    if right_button_pressed:
        player_x += speed
    if up_button_pressed:
        player_y -= speed
    if down_button_pressed:
        player_y += speed

    # Ensure the player stays within world boundaries
    player_x = max(0, min(player_x, world_width - 1))
    player_y = max(0, min(player_y, world_height - 1))

    # Return updated player position
    return player_x, player_y

# Function to check if a point is inside a rectangle
def is_point_inside_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

# Function to draw control buttons and the D-pad on top of everything else
def draw_controls(screen):
    # Draw transparent control buttons using the correct alpha value
    pygame.draw.rect(screen, transparent_red, left_button_rect)
    pygame.draw.rect(screen, transparent_red, right_button_rect)
    pygame.draw.rect(screen, transparent_red, up_button_rect)
    pygame.draw.rect(screen, transparent_red, down_button_rect)
    pygame.draw.rect(screen, transparent_blue, b_button_rect)  # Draw the 'b' button

    # Blit the D-pad image onto the screen at the specified position
    screen.blit(dpad_image, (dpad_x, dpad_y))

# Set the screen dimensions
screen_width, screen_height = 400, 600

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Your game loop would go here

# Make sure to update the screen to display the changes in the game loop
pygame.display.update()