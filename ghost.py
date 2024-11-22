# ghost.py
import pygame
import random
import math

# Define dropped item class
class Ectoplasm:
    def __init__(self, x, y, spawn_time):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (192, 192, 192)  # Silver color
        self.spawn_time = spawn_time
        self.name = "Ectoplasm"  # Add the name attribute

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Adjustable variables for Ghost enemy behaviors
ghost_spawn_enabled = True
ghost_speed = 5
ghost_size = (25, 60)
ghost_health = 100
ghost_damage = 2

# Define Ghost class
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ghost_size[0]
        self.height = ghost_size[1]
        self.speed = ghost_speed
        self.target_x = x
        self.target_y = y
        self.damage = ghost_damage
        self.color = (192, 192, 192)
        self.health = ghost_health

        # Timer for drops
        self.ectoplasm_drop_timer = pygame.time.get_ticks()
        self.ectoplasm_drop_interval = 15000  # Ectoplasm drop every 15 seconds

    def move(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance != 0:
            dx /= distance
            dy /= distance
        
        self.x += dx * self.speed
        self.y += dy * self.speed

    def set_random_target(self, world_width, world_height):
        self.target_x = random.randint(0, world_width - self.width)
        self.target_y = random.randint(0, world_height - self.height)

    def agro(self, player_x, player_y, agro_radius):
        distance_to_player = math.sqrt((player_x - self.x)**2 + (player_y - self.y)**2)
        if distance_to_player <= agro_radius:
            self.target_x = player_x
            self.target_y = player_y

    def try_drop_item(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.ectoplasm_drop_timer >= self.ectoplasm_drop_interval:
            self.ectoplasm_drop_timer = current_time
            return Ectoplasm(self.x, self.y, current_time)

    def update(self):
        self.move()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update_health_bar(self, screen, camera):
        health_bar_width = 30
        health_bar_height = 5
        health_bar_x = self.x - camera.camera.x
        health_bar_y = self.y - camera.camera.y - 10

        health_percentage = self.health / 100.0
        current_health_width = int(health_bar_width * health_percentage)

        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

        font = pygame.font.Font(None, 34)
        text = font.render(f"{int(health_percentage * 100)}%", True, (255, 255, 255))
        text_rect = text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y - 15))
        screen.blit(text, text_rect)
