import pygame
import math

# Day-night cycle colors
daytime_color = (135, 206, 235)  # Light blue
nighttime_color = (0, 0, 0)       # Black

# Class to manage the world and day-night cycle
class World:
    def __init__(self, screen):
        self.screen = screen
        self.time_of_day = 0  # 0 to 3600 (0 is sunrise, 1800 is sunset)

    # Function to update the day-night cycle
    def update_day_night_cycle(self):
        # Calculate the day-night cycle color based on a smooth gradient
        cycle_ratio = (self.time_of_day % 3600) / 1800  # Normalize time of day to [0, 2]

        # Smooth transition using cosine function (changed from sine)
        transition_ratio = (1 + math.cos(cycle_ratio * math.pi)) / 2

        # Blend the colors using the transition_ratio
        r = int((1 - transition_ratio) * daytime_color[0] + transition_ratio * nighttime_color[0])
        g = int((1 - transition_ratio) * daytime_color[1] + transition_ratio * nighttime_color[1])
        b = int((1 - transition_ratio) * daytime_color[2] + transition_ratio * nighttime_color[2])
        background_color = (r, g, b)

        # Fill the entire screen with the day-night cycle color
        self.screen.fill(background_color)

    # Function to advance the time of day
    def advance_time_of_day(self):
        self.time_of_day = (self.time_of_day + 1) % 3600

# Function to get the part of the day (morning, afternoon, evening, night)
    def get_part_of_day(self):
        if 0 <= self.time_of_day < 900:
            return "Night"
        elif 900 <= self.time_of_day < 1800:
            return "Morning"
        elif 1800 <= self.time_of_day < 2700:
            return "Afternoon"
        else:
            return "Evening"

