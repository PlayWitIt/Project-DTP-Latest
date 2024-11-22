import pygame
import random
import math
import sys
import os

# Import relevant modules from your project
from enemies import Ectoplasm, Scales, Bone
import controls
import enemies
import structures
from world import World
from camera import Camera
from enemies import BasicEnemy, StrongEnemy, Ghost, Ghoul
from black_mass import BlackMass
from inventory import Inventory
import indicators
import menu

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)

# Character properties
player_image_width = 300  # Width of the player image
player_image_height = 300  # Height of the player image
player_hitbox_width = 50  # Width of the player hitbox (collision rect)
player_hitbox_height = 100  # Height of the player hitbox (collision rect)

# Offset for aligning the player image with the hitbox
player_image_offset_x = (player_hitbox_width - player_image_width) // -50 + 115
player_image_offset_y = (player_hitbox_height - player_image_height) // -50 + 140

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Your New Window Title")

# World dimensions
world_width = 10000
world_height = 10000

# Game parameters
num_enemies = 100
num_structures = 100
num_terrain = 100

# Add the following function to get the current screen dimensions based on device orientation:
def get_screen_dimensions():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.quit()  # Close the fullscreen window
    return screen_width, screen_height

# Function to run the game
def run(screen, world_width, world_height, num_enemies, num_structures, num_terrain):
    # Initialize player's health and damage taken
    player_health = 100
    player_damage_taken = 0

    # Character position
    character_x = screen.get_width() // 2 - player_hitbox_width // 2
    character_y = screen.get_height() // 2 - player_hitbox_height // 2

    # Variables to store the previous character position
    previous_character_x = character_x
    previous_character_y = character_y

    # Camera properties
    camera_x = character_x - screen.get_width() // 2
    camera_y = character_y - screen.get_height() // 2
    camera_width = screen.get_width()
    camera_height = screen.get_height()

    # Create camera and world
    camera = Camera(world_width, world_height, camera_width, camera_height)
    world = World(screen)

    # Generate structures
    objects_list = structures.generate_structures_and_terrain(num_structures, num_terrain, world_width, world_height)

    # Create enemy manager
    enemy_manager = enemies.EnemyManager(world_width, world_height)

    # Dropped items list
    dropped_items = []

    # Initialize the BlackMass
    black_mass = BlackMass(world_width, world_height)

    # Initialize the player's inventory
    inventory = Inventory(10)  # Set the inventory capacity

    # Cooldown for enemy attacks
    last_enemy_attack_time = pygame.time.get_ticks()
    enemy_attack_cooldown = 2500

    # Aggro radius for enemies
    agro_radius = 200

    # Respawn parameters
    respawn_flag = False
    respawn_delay = 1500
    respawn_timer = 1500

    # Item despawn time (in milliseconds)
    item_despawn_time = 30000

    # Ectoplasm and Scales collected count
    ectoplasm_collected = 0  # Starting with 0 Ectoplasm
    scales_collected = 0  # Starting with 0 Scales

    # Water speed reduction flag
    in_water = False
    water_speed_reduction = 0.3  # 30% speed reduction in water

    # Load the player sprite image
    player_image = pygame.image.load("Player.png")  # Replace with the actual file path
    # Resize the player image to the desired width and height
    player_image = pygame.transform.scale(player_image, (player_image_width, player_image_height))

    # Add the following variables
    show_hitbox = True  # Variable to toggle player hitbox visibility
    show_enemy_hitboxes = True  # Variable to toggle enemy hitbox visibility

    # Main loop
    running = True
    paused = False  # Flag for pause state
    clock = pygame.time.Clock()

    # Initialize pause timer
    paused_start_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle pause when 'P' key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if not paused:
                    # Pause the game
                    paused = True  # Set paused to True
                    paused_start_time = pygame.time.get_ticks()  # Record the time when the game was paused
                else:
                    # Resume the game
                    paused = False  # Set paused to False
                    # Calculate the time elapsed during pause and subtract it from respawn_timer
                    if respawn_flag:
                        respawn_timer += pygame.time.get_ticks() - paused_start_time

        if paused:
            continue  # Skip game logic when paused

        # Store the previous character position before updating it
        previous_character_x = character_x
        previous_character_y = character_y

        # Define character_rect here
        character_rect = pygame.Rect(character_x - camera.camera.x, character_y - camera.camera.y, player_hitbox_width, player_hitbox_height)

        # Check if the player is in water
        in_water = False
        for obj in objects_list:
            if isinstance(obj, structures.River) or isinstance(obj, structures.Ocean) or isinstance(obj, structures.Lake):
                obj_rect = pygame.Rect(obj.x - camera.camera.x, obj.y - camera.camera.y, obj.width, obj.height)
                if character_rect.colliderect(obj_rect):
                    in_water = True
                    break  # No need to check further

        # Handle controls
        if not in_water:  # Check if the player is not in water for normal speed
            new_character_x, new_character_y = controls.handle_controls(character_x, character_y, world_width, world_height)
        else:
            # Adjust controls for reduced speed in water
            new_character_x, new_character_y = controls.handle_controls(character_x, character_y, world_width, world_height, in_water=True)

        # Check for collisions with mountains
        character_rect = pygame.Rect(new_character_x - camera.camera.x, new_character_y - camera.camera.y, player_hitbox_width, player_hitbox_height)
        mountain_collision = False

        for obj in objects_list:
            if isinstance(obj, structures.Mountain):
                obj_rect = pygame.Rect(obj.x - camera.camera.x, obj.y - camera.camera.y, obj.width, obj.height)
                if character_rect.colliderect(obj_rect):
                    mountain_collision = True
                    break  # No need to check further

        # Only update character position if there's no mountain collision
        if not mountain_collision:
            character_x, character_y = new_character_x, new_character_y

        # Update enemies and check for collisions
        enemy_manager.update(world.get_part_of_day(), character_x, character_y, agro_radius, objects_list, camera)

        # Update camera
        camera.update(character_x, character_y)

        # Clear screen
        if respawn_flag:
            screen.fill(red)
        else:
            screen.fill(white)

        # Update day/night cycle
        world.update_day_night_cycle()

        # Update player's health based on damage taken
        player_health -= player_damage_taken
        player_damage_taken = 0

        # Player death condition
        if player_health <= 0:
            player_health = 0
            if not respawn_flag:
                respawn_flag = True
                respawn_timer = pygame.time.get_ticks()
                screen.fill(red)
            else:
                if pygame.time.get_ticks() - respawn_timer >= respawn_delay:
                    player_health = 100
                    character_x = world_width // 2 - player_hitbox_width // 2
                    character_y = world_height // 2 - player_hitbox_height // 2
                    respawn_flag = False

        # Determine health text color based on health percentage
        health_color = (0, 255, 0)  # Green by default
        if player_health <= 50:
            health_color = (255, 0, 0)  # Red if health is 50 or less

        # Draw structures (excluding forests)
        for obj in objects_list:
            if not isinstance(obj, structures.Forest):
                obj_rect = pygame.Rect(obj.x - camera.camera.x, obj.y - camera.camera.y, obj.width, obj.height)
                pygame.draw.rect(screen, obj.color, obj_rect)

                # Check for collision with mountains
                if isinstance(obj, structures.Mountain):
                    if character_rect.colliderect(obj_rect):
                        # Handle the collision here, e.g., prevent character movement in that direction
                        character_x = previous_character_x
                        character_y = previous_character_y

        # Update Ghoul enemies
        for enemy in enemy_manager.enemies:
            if isinstance(enemy, Ghoul):
                enemy.update_health()  # Gradually decrease health and change appearance

        # Draw the resized player sprite image with the offset
        if show_hitbox:
            # Draw the hitbox rect for the player
            pygame.draw.rect(screen, (255, 0, 0), character_rect, 2)  # Red rect with a border
        screen.blit(player_image, (character_x - camera.camera.x - player_image_offset_x, character_y - camera.camera.y - player_image_offset_y))

        # Draw enemies and handle collisions
        for enemy in enemy_manager.enemies:
            enemy_rect = pygame.Rect(enemy.x - camera.camera.x, enemy.y - camera.camera.y, enemy.width, enemy.height)
            if show_enemy_hitboxes:
                # Draw the hitbox rect for enemies if show_enemy_hitboxes is True
                pygame.draw.rect(screen, (255, 0, 0), enemy_rect, 2)  # Red rect with a border
            pygame.draw.rect(screen, enemy.color, enemy_rect)

            # Check for collision with mountains
            for obj in objects_list:
                if isinstance(obj, structures.Mountain):
                    obj_rect = pygame.Rect(obj.x - camera.camera.x, obj.y - camera.camera.y, obj.width, obj.height)
                    if enemy_rect.colliderect(obj_rect):
                        # Handle the collision here, e.g., prevent enemy movement in that direction
                        enemy.x = enemy.prev_x
                        enemy.y = enemy.prev_y

            if character_rect.colliderect(enemy_rect) and pygame.time.get_ticks() - last_enemy_attack_time >= enemy_attack_cooldown:
                player_damage_taken += enemy.damage
                last_enemy_attack_time = pygame.time.get_ticks()
                enemy.health -= 10  # Adjust the amount of damage as needed

            # Randomly try to drop items
            dropped_item = enemy.try_drop_item()
            if dropped_item:
                dropped_items.append(dropped_item)

            # Update enemy health bars
            enemy.update_health_bar(screen, camera)

        # Draw forests on top of everything else
        for obj in objects_list:
            if isinstance(obj, structures.Forest):
                obj_rect = pygame.Rect(obj.x - camera.camera.x, obj.y - camera.camera.y, obj.width, obj.height)
                pygame.draw.rect(screen, obj.color, obj_rect)

        # Check for item pickup
        items_to_remove = []
        for item in dropped_items:
            item_rect = pygame.Rect(item.x - camera.camera.x, item.y - camera.camera.y, item.width, item.height)

            if character_rect.colliderect(item_rect):
                if isinstance(item, Ectoplasm):
                    ectoplasm_collected += 1
                    items_to_remove.append(item)
                elif isinstance(item, Scales):
                    # Check if the player has Ectoplasm to pick up the scale
                    if ectoplasm_collected > 0:
                        inventory.add_item(item)
                        scales_collected += 1

                        # Check if the player has collected 10 scales, and increase health if needed
                        if scales_collected % 1 == 0:
                            player_health += 100

                        items_to_remove.append(item)
                        ectoplasm_collected -= 1  # Consume one Ectoplasm per scale pickup

        # Remove picked up items from the list
        for item in items_to_remove:
            if item in dropped_items:
                dropped_items.remove(item)

        # Draw dropped items and handle despawning
        items_to_remove = []
        for item in dropped_items:
            item_rect = pygame.Rect(item.x - camera.camera.x, item.y - camera.camera.y, item.width, item.height)
            if isinstance(item, Ectoplasm):
                pygame.draw.rect(screen, item.color, item_rect)
            elif isinstance(item, Scales):
                pygame.draw.rect(screen, item.color, item_rect)
            elif isinstance(item, Bone):
                pygame.draw.rect(screen, item.color, item_rect)

            # Check if it's time to despawn the item
            if pygame.time.get_ticks() - item.spawn_time >= item_despawn_time:
                items_to_remove.append(item)

        # Remove despawned items from the list
        for item in items_to_remove:
            if item in dropped_items:
                dropped_items.remove(item)

        # Update the BlackMass
        # black_mass.update()

        # Draw the BlackMass
        for x, y in black_mass.get_black_mass_positions():
            black_mass_rect = pygame.Rect(x - camera.camera.x, y - camera.camera.y, BlackMass.BLACK_MASS_SIZE, BlackMass.BLACK_MASS_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), black_mass_rect)

        # Calculate the number of corrupted pixels/units
        corrupted_pixels = len(black_mass.get_black_mass_positions())

        # Draw indicators with corrupted pixels/units
        indicators.draw_indicators(
            screen,
            len(enemy_manager.enemies),
            world.get_part_of_day(),
            True,
            player_health,
            (character_x, character_y),
            corrupted_pixels,
            inventory,
            ectoplasm_collected,
            scales_collected  # Add scales_collected here
        )

        # Draw the D-pad image on the screen
        controls.draw_controls(screen)

        # Display indicators
        pygame.display.update()

        # Limit frame rate
        clock.tick(60)

        # Advance time
        world.advance_time_of_day()

    pygame.quit()

if __name__ == "__main__":
    menu.main_menu()
    run(screen, world_width, world_height, num_enemies, num_structures, num_terrain)