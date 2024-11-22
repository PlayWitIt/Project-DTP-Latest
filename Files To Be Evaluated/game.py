import pygame
import controls
import enemies
import structures
import random
from world import World

# Colors
white = (255, 255, 255)

# Character properties
character_width = 50
character_height = 50

# Function to run the game
def run(screen, world_width, world_height, num_enemies, num_structures, num_terrain):
    # Character position in the world
    character_x = screen.get_width() // 2 - character_width // 2
    character_y = screen.get_height() // 2 - character_height // 2

    # Camera position and dimensions
    camera_x = character_x - screen.get_width() // 2
    camera_y = character_y - screen.get_height() // 2
    camera_width = screen.get_width()
    camera_height = screen.get_height()

    # Generate random enemies
    existing_enemy_rects = []
    enemies_list = []

    # Generate random structures and terrain
    objects_list = structures.generate_structures_and_terrain(num_structures, num_terrain, world_width, world_height)

    # Create the world instance
    world = World(screen)

    # Game loop
    running = True
    clock = pygame.time.Clock()

    # Indicators
    font = pygame.font.Font(None, 24)
    enemy_spawning = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle control events
        character_x, character_y = controls.handle_controls(character_x, character_y, world_width, world_height)

        # Update enemy positions and set random targets
        if enemy_spawning and world.get_part_of_day() == "Night":
            if not enemies_list:
                # Only generate enemies if the list is empty (prevent repeated generation)
                enemies_list = enemies.generate_enemies(num_enemies, world_width, world_height, existing_enemy_rects, character_x, character_y, True)

            for enemy in enemies_list:
                enemy.move()
                if random.randint(0, 100) < 5:
                    enemy.set_random_target(world_width, world_height)
        else:
            # Clear the enemies list during daytime or when spawning is disabled
            enemies_list = []

        # Update camera position based on character position
        camera_x = character_x - screen.get_width() // 2
        camera_y = character_y - screen.get_height() // 2

        # Cap the camera position to ensure it stays within world bounds
        camera_x = max(0, min(camera_x, world_width - camera_width))
        camera_y = max(0, min(camera_y, world_height - camera_height))

        # Clear the screen
        screen.fill(white)

        # Update the day-night cycle
        world.update_day_night_cycle()

        # Draw on-screen touch controls
        pygame.draw.rect(screen, (200, 200, 200), controls.left_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), controls.right_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), controls.up_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), controls.down_button_rect)

        # Draw structures and terrain with camera position applied
        for obj in objects_list:
            obj_rect_screen = pygame.Rect(obj.x - camera_x, obj.y - camera_y, obj.width, obj.height)
            pygame.draw.rect(screen, obj.color, obj_rect_screen)

        # Draw enemies with camera position applied
        for enemy in enemies_list:
            enemy_rect_screen = pygame.Rect(enemy.x - camera_x, enemy.y - camera_y, enemy.width, enemy.height)
            pygame.draw.rect(screen, enemy.color, enemy_rect_screen)

        # Draw the character in the viewport with camera position applied
        character_rect = pygame.Rect(character_x - camera_x, character_y - camera_y, character_width, character_height)
        pygame.draw.rect(screen, (255, 0, 0), character_rect)

        # Display indicators
        enemy_count_text = font.render(f"Enemies: {len(enemies_list)}", True, (255, 255, 255))
        time_of_day_text = font.render(f"Time of Day: {world.get_part_of_day()}", True, (255, 255, 255))
        enemy_spawning_text = font.render(f"Enemy Spawning: {'Yes' if enemy_spawning else 'No'}", True, (255, 255, 255))

        screen.blit(enemy_count_text, (10, 10))
        screen.blit(time_of_day_text, (10, 40))
        screen.blit(enemy_spawning_text, (10, 70))

        # Update the display
        pygame.display.update()

        # Cap the frame rate to 60 frames per second
        clock.tick(60)

        # Advance the time of day
        world.advance_time_of_day()

    # Quit Pygame
    pygame.quit()

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D RPG Game")

# World dimensions
world_width = 10000
world_height = 10000

# Increased number of enemies, structures, and terrain
num_enemies = 200
num_structures = 100
num_terrain = 100

# Start the game
run(screen, world_width, world_height, num_enemies, num_structures, num_terrain)