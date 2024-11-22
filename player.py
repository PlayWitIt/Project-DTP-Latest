import pygame
import controls

# Character properties
character_width = 50
character_height = 50
character_speed = 5

# Function to handle player movement
def handle_player_movement(player_x, player_y, world_width, world_height):
    # Handle control events and update player position
    player_x, player_y = controls.handle_controls(player_x, player_y, world_width, world_height)

    # Ensure the player stays within world boundaries
    player_x = max(0, min(player_x, world_width - character_width))
    player_y = max(0, min(player_y, world_height - character_height))

    # Return updated player position
    return player_x, player_y