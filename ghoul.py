# ghoul.py
import pygame
import random
import math

# Define dropped item classes
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

class Scales:
    def __init__(self, x, y, spawn_time, height, color):
        self.x = x
        self.y = y
        self.width = 10
        self.height = height
        self.color = color  # Green color
        self.spawn_time = spawn_time
        self.name = "Scales"  # Add the name attribute

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Bone:
    def __init__(self, x, y, spawn_time):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.color = (255, 255, 255)  # White color
        self.spawn_time = spawn_time
        self.name = "Bone"  # Add the name attribute

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Adjustable variables for Ghoul enemy behaviors
ghoul_spawn_enabled = True
ghoul_speed = 3
ghoul_size = (45, 60)
ghoul_health = 100
ghoul_damage = 10

# Define Ghoul class
class Ghoul:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ghoul_size[0]
        self.height = ghoul_size[1]
        self.speed = ghoul_speed
        self.target_x = x
        self.target_y = y
        self.damage = ghoul_damage
        self.color = (0, 255, 0)
        self.health = ghoul_health
        self.skeleton_stage = False

        # Timers for drops
        self.scales_drop_timer = pygame.time.get_ticks()
        self.scales_drop_interval = 10000  # Scales drop every 10 seconds
        self.bone_drop_timer = pygame.time.get_ticks()
        self.bone_drop_interval = 20000  # Bones drop every 20 seconds

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

        if not self.skeleton_stage and current_time - self.scales_drop_timer >= self.scales_drop_interval:
            self.scales_drop_timer = current_time
            return Scales(self.x, self.y, current_time, 10, (0, 255, 0))
        elif self.skeleton_stage and current_time - self.bone_drop_timer >= self.bone_drop_interval:
            self.bone_drop_timer = current_time
            return Bone(self.x, self.y, current_time)

    def update_health(self):
        if not self.skeleton_stage:
            self.health -= 0.1

            if self.health <= ghoul_health * 0.5:
                self.skeleton_stage = True
                self.color = (255, 255, 255)
        else:
            self.health -= 0.01

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
