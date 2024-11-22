# game_manager.py

import pygame
import random
import controls
import structures
import enemies
from world import World
from camera import Camera
from enemies import BasicEnemy, StrongEnemy, Ghost, Ghoul

# Define dropped item classes
class Ectoplasm:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (192, 192, 192)  # Silver color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Scales:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (0, 255, 0)  # Green color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Modify the Enemy class to include item dropping
class Enemy:

    def __init__(self, x, y, width, height, speed, damage):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.speed = speed
        self.target_x = x
        self.target_y = y
        self.damage = damage
        self.color = (255, 0, 0)  # Default color

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
        # Define the drop probabilities here
        drop_probability = random.random()

        if isinstance(self, Ghost) and drop_probability <= 0.05:
            return Ectoplasm(self.x, self.y)
        elif isinstance(self, Ghoul) and drop_probability <= 0.05:
            return Scales(self.x, self.y)
        else:
            return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class BasicEnemy(Enemy):

    def __init__(self, x, y, width, height, speed, damage):
        super().__init__(x, y, width, height, speed, damage)

class StrongEnemy(Enemy):

    def __init__(self, x, y, width, height, speed, damage, health):
        super().__init__(x, y, width, height, speed, damage)
        self.health = health

class Ghost(BasicEnemy):

    def __init__(self, x, y, width, height, speed, damage):
        super().__init__(x, y, width, height, speed, damage)
        self.color = (192, 192, 192)  # Silver color

class Ghoul(StrongEnemy):

    def __init__(self, x, y, width, height, speed, damage):
        health = 100
        super().__init__(x, y, width, height, speed, damage, health)
        self.color = (0, 255, 0)  # Green color

class EnemyManager:
    
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.enemies = []

    def update(self, time_of_day, player_x, player_y, agro_radius):
        if time_of_day == "Night":
            if random.randint(0, 100) < 5:
                new_enemies = generate_enemies(1, self.world_width, self.world_height, self.enemies, player_x, player_y, is_night=True)
                self.enemies.extend(new_enemies)
        else:
            self.enemies = [enemy for enemy in self.enemies if not (isinstance(enemy, Ghost) or (isinstance(enemy, Ghoul) and enemy.health <= 0))]

        for enemy in self.enemies:
            enemy.move()
            if random.randint(0, 100) < 5:
                enemy.set_random_target(self.world_width, self.world_height)

            enemy.agro(player_x, player_y, agro_radius)  # Set enemy to agro state

def generate_enemies(num_enemies, world_width, world_height, existing_enemies, player_x, player_y, is_night):

    enemies = []

    for _ in range(num_enemies):

        if is_night:
            visible_range = 300
            min_x = max(0, player_x - visible_range)
            max_x = min(world_width-50, player_x + visible_range)
            min_y = max(0, player_y - visible_range)
            max_y = min(world_height-50, player_y + visible_range)

            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
        else:
            x = random.randint(0, world_width-50)
            y = random.randint(0, world_height-50)
        
        width = 40
        height = 40
        speed = 2.0
        damage = random.randint(10, 30)

        if random.randint(0, 1) == 0:  # 50% chance of spawning a Ghoul
            enemy = Ghoul(x, y, width, height, speed, damage)
        else:
            enemy = Ghost(x, y, width, height, speed, damage)

        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

        overlap = any(enemy_rect.colliderect(pygame.Rect(e.x, e.y, e.width, e.height)) for e in existing_enemies)

        while overlap:
            x = random.randint(0, world_width-50)
            y = random.randint(0, world_height-50)
            if random.randint(0, 1) == 0:  # 50% chance of spawning a Ghoul
                enemy = Ghoul(x, y, width, height, speed, damage)
            else:
                enemy = Ghost(x, y, width, height, speed, damage)
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            overlap = any(enemy_rect.colliderect(pygame.Rect(e.x, e.y, e.width, e.height)) for e in existing_enemies)

        if is_night:
            enemy.set_random_target(world_width, world_height)

        enemies.append(enemy)

    return enemies
