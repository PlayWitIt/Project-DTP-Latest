# dark_fairy.py
import pygame
import random
import math

# Define dropped item class for Dark Pixie Dust
class DarkPixieDust:
    def __init__(self, x, y, spawn_time):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (64, 64, 64)  # Dark gray color
        self.spawn_time = spawn_time
        self.name = "Dark Pixie Dust"  # Add the name attribute

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Adjustable variables for Dark Fairy enemy behaviors
dark_fairy_spawn_enabled = True
dark_fairy_speed = 6
dark_fairy_size = (20, 20)
dark_fairy_health = 100
dark_fairy_damage = 15

# Define DarkFairy class
class DarkFairy:
    def __init__(self, x, y, health=100, width=20, height=20, speed=6, damage=15, color=(64, 64, 64)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.target_x = x
        self.target_y = y
        self.damage = damage
        self.color = color
        self.health = health
        self.name = "Dark Fairy"

        # Timer for drops
        self.dark_pixie_dust_drop_timer = pygame.time.get_ticks()
        self.dark_pixie_dust_drop_interval = 20000  # Dark Pixie Dust drop every 20 seconds

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

        if current_time - self.dark_pixie_dust_drop_timer >= self.dark_pixie_dust_drop_interval:
            self.dark_pixie_dust_drop_timer = current_time
            return DarkPixieDust(self.x, self.y, current_time)

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