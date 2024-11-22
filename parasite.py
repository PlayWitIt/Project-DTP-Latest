# parasite.py
import pygame
import random
import math

# Define dropped item class for Parasite Segment
class ParasiteSegment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (0, 0, 0)  # Black color
        self.name = "Parasite Segment"  # Add the name attribute

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Adjustable variables for Parasite enemy behaviors
parasite_spawn_enabled = True
parasite_speed = 4
parasite_size = (10, 10)
parasite_health = 80
parasite_damage = 12
parasite_length = 10  # Number of body segments

# Define Parasite class
class Parasite:
    def __init__(self, x, y):
        health = parasite_health
        self.x = x
        self.y = y
        self.width = parasite_size[0]
        self.height = parasite_size[1]
        self.speed = parasite_speed
        self.color = (0, 0, 0)  # Black color for the Parasite
        self.health = health
        self.name = "Parasite"

        # List to store Parasite segments (body)
        self.body = [(x, y)] * parasite_length

        # Direction for movement
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

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

    def try_drop_item(self):
        pass
        # Parasite does not drop items

    def update(self):
        self.move()

    def draw(self, screen):
        # Draw the Parasite's body segments
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.width, self.height))

        # Draw the Parasite's head
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
