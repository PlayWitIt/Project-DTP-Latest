# game_logic2.py

import pygame
import game_manager  # Import the game_manager module

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Defeat The Purpose")

# World dimensions
world_width = 10000
world_height = 10000

# Game parameters
num_enemies = 20
num_structures = 50
num_terrain = 50

# Function to run the game
def run(screen, world_width, world_height, num_enemies, num_structures, num_terrain):

    # Initialize player's health and damage taken
    player_health = 100
    player_damage_taken = 0

    # Character properties
    character_width = 50
    character_height = 50

    # Character position 
    character_x = screen.get_width() // 2 - character_width // 2
    character_y = screen.get_height() // 2 - character_height // 2

    # Camera properties
    camera_x = character_x - screen.get_width() // 2
    camera_y = character_y - screen.get_height() // 2
    camera_width = screen.get_width()
    camera_height = screen.get_height()

    # Create camera and world
    camera = game_manager.Camera(world_width, world_height, camera_width, camera_height)
    world = game_manager.World(screen)

    # Generate structures
    objects_list = game_manager.structures.generate_structures_and_terrain(num_structures, num_terrain, world_width, world_height)

    # Create enemy manager
    enemy_manager = game_manager.enemies.EnemyManager(world_width, world_height)

    # Indicators
    font = pygame.font.Font(None, 50)

    # Cooldown for enemy attacks
    last_enemy_attack_time = pygame.time.get_ticks()
    enemy_attack_cooldown = 1000  # Set the desired cooldown duration in milliseconds

    # Aggro radius for enemies
    agro_radius = 200

    # Respawn parameters
    respawn_flag = False
    respawn_delay = 3000  # 3 seconds in milliseconds
    respawn_timer = 0

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle controls
        character_x, character_y = game_manager.controls.handle_controls(character_x, character_y, world_width, world_height)
        
        # Update enemies
        enemy_manager.update(world.get_part_of_day(), character_x, character_y, agro_radius)

        # Update camera
        camera.update(character_x, character_y)

        # Clear screen
        if respawn_flag:
            screen.fill(game_manager.red)  # Red screen during respawn
        else:
            screen.fill(game_manager.white)

        # Update day/night cycle
        world.update_day_night_cycle()

        # Update player's health based on damage taken
        player_health -= player_damage_taken
        player_damage_taken = 0

        # Player death condition
        if player_health <= 0:
            player_health = 0  # Ensure health doesn't go negative
            if not respawn_flag:
                respawn_flag = True
                respawn_timer = pygame.time.get_ticks()  # Start the respawn timer
                
                # Turn the screen red
                screen.fill(game_manager.red)
            else:
                # Check if respawn timer has reached the delay
                if pygame.time.get_ticks() - respawn_timer >= respawn_delay:
                    # Respawn the player with full health
                    player_health = 100
                    character_x = world_width // 2 - character_width // 2
                    character_y = world_height // 2 - character_height // 2
                    respawn_flag = False  # Reset the respawn flag

        # Determine health text color based on health percentage
        health_color = (0, 255, 0)  # Green by default
        if player_health <= 50:
            health_color = (255, 0, 0)  # Red if health is 50 or less

        # Draw touch controls
        pygame.draw.rect(screen, (200, 200, 200), game_manager.controls.left_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), game_manager.controls.right_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), game_manager.controls.up_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), game_manager.controls.down_button_rect)

        # Draw structures
        for obj in objects_list:
            obj_rect = pygame.Rect(obj.x - camera.camera.x, obj.y - camera.camera.y, obj.width, obj.height)
            pygame.draw.rect(screen, obj.color, obj_rect)

        # Draw enemies and handle collisions
        character_rect = pygame.Rect(character_x - camera.camera.x, character_y - camera.camera.y, character_width, character_height)
        for enemy in enemy_manager.enemies:
            enemy_rect = pygame.Rect(enemy.x - camera.camera.x, enemy.y - camera.camera.y, enemy.width, enemy.height)
            pygame.draw.rect(screen, enemy.color, enemy_rect)

            # Check for collision with the player and cooldown
            if character_rect.colliderect(enemy_rect) and pygame.time.get_ticks() - last_enemy_attack_time >= enemy_attack_cooldown:
                player_damage_taken += enemy.damage
                last_enemy_attack_time = pygame.time.get_ticks()  # Update last attack time
                enemy_manager.enemies.remove(enemy)

        # Draw character
        character_rect = pygame.Rect(character_x - camera.camera.x, character_y - camera.camera.y, character_width, character_height)
        pygame.draw.rect(screen, (255, 0, 0), character_rect)

        # Display indicators
        enemy_count_text = font.render(f"Enemies: {len(enemy_manager.enemies)}", True, (255, 255, 255))
        time_of_day_text = font.render(f"Time of Day: {world.get_part_of_day()}", True, (255, 255, 255))
        coords_text = font.render(f"X: {character_x}, Y: {character_y}", True, (255, 255, 255))
        
        # Use the determined health_color for the health text
        health_text = font.render(f"Health: {player_health}", True, health_color)

        screen.blit(enemy_count_text, (10, 10))
        screen.blit(time_of_day_text, (10, 40))
        screen.blit(coords_text, (10, 70))
        screen.blit(health_text, (10, 100))

        # Update display
        pygame.display.update()

        # Limit frame rate
        clock.tick(60)

        # Advance time
        world.advance_time_of_day()

    pygame.quit()

# Run game
game_manager.run(screen, world_width, world_height, num_enemies, num_structures, num_terrain)
