import pygame
from inventory import Item, Ectoplasm, Scales, Inventory, Player
from items import Item, Ectoplasm, Scales, Inventory
from indicators import draw_indicators

# Initialize Pygame and set up the game window
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Adventure Game")

# Initialize game variables
running = True
clock = pygame.time.Clock()

# Create the player character
player = Player(400, 300, 30, 30)

# Create the player's inventory
player_inventory = Inventory()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player controls and update player position
    player.x, player.y = handle_controls(player.x, player.y, 2000, 2000)

    # Update the camera to follow the player
    camera.update(player.x, player.y)

    # Update the time of day and day-night cycle
    world.advance_time_of_day()
    world.update_day_night_cycle()

    # Update enemy positions and behavior
    enemy_manager.update(world.get_part_of_day(), player.x, player.y, 200)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the world background based on the time of day
    world.draw_background(screen)

    # Draw structures and terrain
    for obj in objects:
        obj.draw(screen)

    # Draw enemies
    for enemy in enemy_manager.enemies:
        screen.blit(enemy.image, camera.apply(enemy))

    # Draw the player character
    screen.blit(player.image, camera.apply(player))

    # Draw game indicators
    draw_indicators(screen, len(enemy_manager.enemies), world.get_part_of_day(), True)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

pygame.quit()
