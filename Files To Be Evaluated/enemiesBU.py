#enemies.py
import pygame
import random
import math

# Add variables for spawn chances
ghoul_spawn_chance = 5  # Adjust the percentage as needed
ghost_spawn_chance = 10  # Adjust the percentage as needed
dark_fairy_spawn_chance = 8  # Adjust the percentage as needed for Dark Fairy
parasite_spawn_chance = 12  # Adjust the percentage as needed for Parasite

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
        drop_probability = random.random()

        if drop_probability <= 0.001:
            return Ectoplasm(self.x, self.y, pygame.time.get_ticks())
        elif drop_probability <= 0.001:
            return Scales(self.x, self.y, pygame.time.get_ticks(), 10, (0, 255, 0))

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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Adjustable variables for Ghost enemy behaviors
ghost_spawn_enabled = True
ghost_speed = 5
ghost_size = (25, 60)
ghost_health = 100
ghost_damage = 2

# Adjustable variables for Ghoul enemy behaviors
ghoul_spawn_enabled = True
ghoul_speed = 3
ghoul_size = (45, 60)
ghoul_health = 100
ghoul_damage = 10

# Adjustable variables for Dark Fairy enemy behaviors
dark_fairy_spawn_enabled = True
dark_fairy_speed = 6
dark_fairy_size = (20, 20)
dark_fairy_health = 100
dark_fairy_damage = 15

# Adjustable variables for Parasite enemy behaviors
parasite_spawn_enabled = True
parasite_speed = 4
parasite_size = (10, 10)
parasite_health = 80
parasite_damage = 12
parasite_length = 10  # Number of body segments

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
        self.color = (255, 0, 0)
        self.health = 100

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
        drop_probability = random.random()

        if isinstance(self, Ghost) and drop_probability <= 0.001:
            return Ectoplasm(self.x, self.y, pygame.time.get_ticks())
        elif drop_probability <= 0.001:
            return Scales(self.x, self.y, pygame.time.get_ticks(), 10, (0, 255, 0))

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
    def __init__(self, x, y):
        super().__init__(x, y, ghost_size[0], ghost_size[1], ghost_speed, ghost_damage)
        self.color = (192, 192, 192)
        self.health = ghost_health

class Ghoul(StrongEnemy):
    def __init__(self, x, y):
        health = ghoul_health
        super().__init__(x, y, ghoul_size[0], ghoul_size[1], ghoul_speed, ghoul_damage, health)
        self.color = (0, 255, 0)
        self.skeleton_stage = False

        self.bone_drop_timer = pygame.time.get_ticks()
        self.bone_drop_interval = 5000

    def update_health(self):
        if not self.skeleton_stage:
            self.health -= 0.1

            if self.health <= ghoul_health * 0.5:
                self.skeleton_stage = True
                self.color = (255, 255, 255)
        else:
            self.health -= 0.01

    def try_drop_item(self):
        if self.skeleton_stage and pygame.time.get_ticks() - self.bone_drop_timer >= self.bone_drop_interval:
            self.bone_drop_timer = pygame.time.get_ticks()
            return Bone(self.x, self.y, pygame.time.get_ticks())
        elif not self.skeleton_stage:
            drop_probability = random.random()

            if drop_probability <= 0.005:
                return Ectoplasm(self.x, self.y, pygame.time.get_ticks())
            elif drop_probability <= 0.005:
                return Scales(self.x, self.y, pygame.time.get_ticks(), 10, (0, 255, 0))

        return None

    def update(self):
        super().update()

class Parasite(StrongEnemy):
    def __init__(self, x, y):
        health = parasite_health
        super().__init__(x, y, parasite_size[0], parasite_size[1], parasite_speed, parasite_damage, health)
        self.color = (0, 0, 0)  # Black color for the Parasite
        self.body = [(x, y)] * parasite_length
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Initial direction

    def move(self):
        # Move the Parasite's body segments
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        # Move the Parasite's head
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Update the head's position in the body list
        self.body[0] = (self.x, self.y)

        # Change direction randomly
        if random.randint(1, 100) <= 5:
            self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def draw(self, screen):
        # Draw the Parasite's body segments
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.width, self.height))

        # Draw the Parasite's head
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class EnemyManager:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.enemies = []

    def update(self, time_of_day, player_x, player_y, agro_radius):
        if time_of_day == "Night" and ghost_spawn_enabled:
            if random.randint(0, 100) < 5:
                new_enemies = generate_enemies(1, self.world_width, self.world_height, self.enemies, player_x, player_y, is_night=True)
                self.enemies.extend(new_enemies)
        else:
            self.enemies = [enemy for enemy in self.enemies if not (isinstance(enemy, Ghost) or (isinstance(enemy, Ghoul) and enemy.health <= 0))]

        for enemy in self.enemies:
            enemy.move()
            if random.randint(0, 100) < 5:
                enemy.set_random_target(self.world_width, self.world_height)
            enemy.agro(player_x, player_y, agro_radius)

    def try_drop_items(self):
        items_to_drop = []
        for enemy in self.enemies:
            dropped_item = enemy.try_drop_item()
            if dropped_item:
                items_to_drop.append(dropped_item)
        return items_to_drop

    def draw(self, screen, camera):
        for enemy in self.enemies:
            enemy.draw(screen)
            enemy.update_health_bar(screen, camera)

# Function to generate random enemies with improved spawning mechanics
# Function to generate random enemies with improved spawning mechanics
# Function to generate random enemies with adjustable spawning distances
def generate_enemies(num_enemies, world_width, world_height, existing_enemies, player_x, player_y, is_night=False):
    enemies = []
    min_spawn_distance = 300# Minimum spawning distance from the player
    max_spawn_distance = 1000  # Maximum spawning distance from the player

    for _ in range(num_enemies):
        while True:
            # Generate random coordinates within the specified range
            enemy_x = random.randint(0, world_width - 20)
            enemy_y = random.randint(0, world_height - 20)

            # Calculate the distance between the enemy and the player
            distance_to_player = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)

            # Check if the enemy is within the acceptable spawning range
            if min_spawn_distance <= distance_to_player <= max_spawn_distance:
                break

        # Create different enemy types based on probabilities
        enemy_type = random.choices(
            ["Ghost", "Ghoul", "DarkFairy", "Parasite"],
            weights=[ghost_spawn_chance, ghoul_spawn_chance, dark_fairy_spawn_chance, parasite_spawn_chance],
            k=1
        )[0]

        if enemy_type == "Ghost":
            enemies.append(Ghost(enemy_x, enemy_y))
        elif enemy_type == "Ghoul":
            enemies.append(Ghoul(enemy_x, enemy_y))
        elif enemy_type == "DarkFairy":
            enemies.append(DarkFairy(enemy_x, enemy_y))
        elif enemy_type == "Parasite":
            enemies.append(Parasite(enemy_x, enemy_y))

    return enemies
