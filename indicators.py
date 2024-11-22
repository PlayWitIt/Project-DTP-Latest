# indicators.py
import pygame
from inventory import total_score

# Initialize the font module
pygame.font.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 32)  # Default font size

# Variable to keep track of the total score
# total_score = 0

# Dictionary to track scales collected for each scale object
scales_collected_dict = {}

# List of indicators with their properties
indicators = [
    {
        "name": "Enemies",
        "text": "Enemies: {}",
        "value": 0,
        "color": white,
        "position": (20, 20),
        "bg_color": blue,
        "visible": True,  # Toggle to control visibility
    },
    {
        "name": "Time",
        "text": "Time: {}",
        "value": "",
        "color": white,
        "position": (20, 60),
        "bg_color": blue,
        "visible": False,  # Toggle to control visibility
    },
    {
        "name": "Health",
        "text": "Health: {}",
        "value": 100,
        "color": (0, 255, 0),
        "position": (20, 100),
        "bg_color": blue,  # Initialize background color as blue
        "visible": True,  # Toggle to control visibility
    },
    {
        "name": "Armor",
        "text": "Armor: {}",
        "value": 0,
        "color": white,
        "position": (20, 140),
        "bg_color": blue,
        "visible": True,  # Toggle to control visibility
    },
    {
        "name": "Position",
        "text": "Position: {}",
        "value": (0, 0),
        "color": white,
        "position": (20, 180),
        "bg_color": blue,
        "visible": False,  # Toggle to control visibility
    },
    {
        "name": "Corrupted Pixels",
        "text": "Corrupted Pixels: {}",
        "value": 0,
        "color": white,
        "position": (20, 220),
        "bg_color": blue,
        "visible": False,  # Toggle to control visibility
    },
    {
        "name": "Score",
        "text": "Score: {}",
        "value": 0,
        "color": white,
        "position": (20, 260),
        "bg_color": blue,
        "visible": True,  # Toggle to control visibility
    },
    {
        "name": "Ectoplasm",
        "text": "Ectoplasm: {}",
        "value": 0,
        "color": white,
        "position": (20, 300),
        "bg_color": blue,
        "visible": True,  # Toggle to control visibility
    },
    {
        "name": "Scales",
        "text": "Scales: {}",
        "value": 0,
        "color": white,
        "position": (20, 340),
        "bg_color": blue,
        "visible": True,  # Toggle to control visibility
    },
    {
        "name": "TopCenter",
        "text": "Time: {} | Position: {}",
        "value": ("", (0, 0)),
        "color": white,
        "position": (600, 20),  # Top center position
        "bg_color": blue,
        "visible": True,  # Toggle to control visibility
        "font_size": 42,  # Increase the font size for HUD
    },
]

# Function to draw indicators
def draw_indicators(screen, enemy_count, part_of_day, player_alive, player_health, player_position, corrupted_pixels, inventory, ectoplasm_collected, scales_collected):
    global total_score, font  # Access the total_score and font variables

    # Initialize the y-position for the first visible indicator
    y_position = 20

    for indicator in indicators:
        if indicator["visible"]:
            if indicator["name"] == "TopCenter":
                # Calculate the time and position text for the top center indicator
                top_center_text = indicator["text"].format(part_of_day, player_position)
                font_size = indicator.get("font_size", 36)  # Get font size or default to 36
                font = pygame.font.Font(None, font_size)  # Use the specified font size
                text = font.render(top_center_text, True, indicator["color"])
                text_rect = text.get_rect(center=indicator["position"])
                pygame.draw.rect(screen, indicator["bg_color"], text_rect)
                screen.blit(text, text_rect)
            else:
                if indicator["name"] == "Health" and not player_alive:
                    # Player has respawned, reset the background color to blue
                    indicator["bg_color"] = blue

                # Handle Health and Armor indicators
                if indicator["name"] == "Health":
                    # Display the health, but limit it to 100
                    player_health_displayed = min(player_health, 100)
                    indicator["value"] = player_health_displayed
                    text = font.render(indicator["text"].format(player_health_displayed), True, indicator["color"])
                    # Determine health indicator background color based on health percentage
                    if player_health_displayed <= 50:
                        indicator["bg_color"] = red  # Change background color to red
                    else:
                        indicator["bg_color"] = blue  # Change background color back to blue
                elif indicator["name"] == "Armor":
                    # Calculate and display the armor
                    armor_value = max(player_health - 100, 0)
                    indicator["value"] = armor_value
                    text = font.render(indicator["text"].format(armor_value), True, indicator["color"])
                else:
                    # Update other indicators as before
                    indicator["value"] = enemy_count if indicator["name"] == "Enemies" else \
                                        part_of_day if indicator["name"] == "Time" else \
                                        player_position if indicator["name"] == "Position" else \
                                        corrupted_pixels if indicator["name"] == "Corrupted Pixels" else \
                                        total_score if indicator["name"] == "Score" else \
                                        ectoplasm_collected if indicator["name"] == "Ectoplasm" else \
                                        scales_collected

                    # Draw text using the global font variable
                    text = font.render(indicator["text"].format(indicator["value"]), True, indicator["color"])
                # Draw background rectangle
                pygame.draw.rect(screen, indicator["bg_color"], (10, y_position - 5, 200, 35))
                screen.blit(text, (20, y_position))

            # Increment y-position for the next visible indicator
            y_position += 40  # Adjust this value as needed for spacing
