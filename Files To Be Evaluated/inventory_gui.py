import pygame

# Initialize pygame and set up the screen
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Inventory System")

# Load background image
background_image = pygame.image.load("background.jpg")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
highlight_color = (200, 200, 200)
selected_color = (255, 255, 0)  # Color for selected items

# Create a list to represent the player's inventory
inventory_rows = 5
inventory_cols = 8
inventory = [["Item"] * inventory_cols for _ in range(inventory_rows)]

# Create empty slots by setting some items to None
inventory[2][3] = None
inventory[3][5] = None
inventory[4][1] = None

# Create a font for text display
font = pygame.font.Font(None, 36)

# Define grid cell size and padding (increased cell size)
cell_size = 120  # Adjust the cell size to make slots larger
cell_padding = 10

# Define variables for item dragging
dragging = False
dragged_item = None
dragged_item_index = None
offset_x, offset_y = 0, 0

# Define a variable to track the selected item
selected_item_index = None

# Define variables for the "Drop" button
drop_button_width = 100
drop_button_height = 40
drop_button_x = (screen_width - drop_button_width) // 2  # Centered horizontally
drop_button_y = screen_height - drop_button_height - 20  # Lowered the button position
drop_button_rect = pygame.Rect(drop_button_x, drop_button_y, drop_button_width, drop_button_height)
drop_button_text = font.render("Drop", True, white)

# Create a dictionary to store item descriptions and types
item_data = {
    "Item1": {"description": "This is the description for Item1.", "type": "Weapon"},
    "Item2": {"description": "Item2 is a special item with unique properties.", "type": "Potion"},
    # Add descriptions and types for other items here
}

# Create a dictionary to keep track of item stacks
item_stacks = {}

# Define a variable for the search bar
search_query = ""

# Create a dictionary to store item quantities (for testing)
item_quantities = {
    "Ectoplasm": 5,
    "Scales": 3,
    "Bone": 2,
    "Pixie Dust": 8,
    "Dark Slime": 4,
}

# Define variables for item information display
item_info_font = pygame.font.Font(None, 24)
item_info_background = pygame.Surface((screen_width, 50))
item_info_border_rect = pygame.Rect(0, 0, screen_width, 50)
item_info_background.fill(white)
pygame.draw.rect(item_info_background, black, item_info_border_rect, 2)
item_info_rect = item_info_background.get_rect()
item_info_rect.topleft = (0, screen_height - item_info_rect.height)
selected_item_info = None

# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse events for selecting items
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for i in range(len(inventory)):
                    for j in range(len(inventory[i])):
                        item = inventory[i][j]
                        slot_rect = pygame.Rect(
                            cell_padding + j * (cell_size + cell_padding),
                            cell_padding + i * (cell_size + cell_padding),
                            cell_size,
                            cell_size
                        )
                        if slot_rect.collidepoint(event.pos):
                            if selected_item_index == (i, j):
                                # If the same item is clicked again, deselect it
                                selected_item_index = None
                            else:
                                selected_item_index = (i, j)

        # Handle mouse events for dragging items
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for i in range(len(inventory)):
                    for j in range(len(inventory[i])):
                        item = inventory[i][j]
                        if item is not None:
                            slot_rect = pygame.Rect(
                                cell_padding + j * (cell_size + cell_padding),
                                cell_padding + i * (cell_size + cell_padding),
                                cell_size,
                                cell_size
                            )
                            if slot_rect.collidepoint(event.pos):
                                dragging = True
                                dragged_item = item
                                dragged_item_index = (i, j)
                                offset_x, offset_y = slot_rect.topleft[0] - event.pos[0], slot_rect.topleft[1] - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                # Check for item stacking
                i, j = dragged_item_index
                new_i = (event.pos[1] - cell_padding) // (cell_size + cell_padding)
                new_j = (event.pos[0] - cell_padding) // (cell_size + cell_padding)
                if 0 <= new_i < inventory_rows and 0 <= new_j < inventory_cols and (new_i, new_j) != dragged_item_index:
                    existing_item = inventory[new_i][new_j]
                    if existing_item == dragged_item:
                        # Increase the stack count if the same item is dropped onto an existing stack
                        stack_count = item_stacks.get((new_i, new_j), 1)
                        item_stacks[(new_i, new_j)] = stack_count + 1
                        inventory[i][j] = None
                    else:
                        inventory[i][j], inventory[new_i][new_j] = inventory[new_i][new_j], inventory[i][j]
                dragging = False

        # Handle mouse click on the "Drop" button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if drop_button_rect.collidepoint(event.pos):
                    # Remove the highlighted item (if any) from the inventory
                    if dragged_item is not None:
                        i, j = dragged_item_index
                        inventory[i][j] = None
                        dragged_item = None

        # Handle text input for the search bar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character from the search query
                search_query = search_query[:-1]
            elif event.key == pygame.K_RETURN:
                # Perform a search action (e.g., highlighting items)
                pass  # Add your search action here
            else:
                # Append the pressed key to the search query
                search_query += event.unicode

        # Handle using items from the inventory
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # Press 'u' key to use the selected item
                if selected_item_index:
                    i, j = selected_item_index
                    item_name = inventory[i][j]
                    if item_name in item_quantities and item_quantities[item_name] > 0:
                        # Perform the item's use action here (e.g., healing, equipping)
                        item_quantities[item_name] -= 1
                        # Add your item usage logic here

    # Clear the screen
    screen.fill(white)

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Display "Inventory" label
    label_text = font.render("Inventory", True, black)
    label_rect = label_text.get_rect(center=(screen_width // 2, cell_padding // 2))
    screen.blit(label_text, label_rect)

    # Display search bar
    search_bar_text = font.render("Search: " + search_query, True, black)
    search_bar_rect = search_bar_text.get_rect(topleft=(drop_button_x + drop_button_width + 10, drop_button_rect.centery - search_bar_text.get_height() // 2))

    pygame.draw.rect(screen, black, search_bar_rect, 2)  # Draw search bar border
    screen.blit(search_bar_text, search_bar_rect.topleft)

    # Display inventory items in a grid layout with highlight for selected item
    for i in range(inventory_rows):
        for j in range(inventory_cols):
            item = inventory[i][j]
            slot_rect = pygame.Rect(
                cell_padding + j * (cell_size + cell_padding),
                cell_padding + i * (cell_size + cell_padding),
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, black, slot_rect, 2)  # Draw slot borders
            if item is not None:
                item_info = item_data.get(item, {"description": "No description available", "type": "Unknown"})
                text = font.render(f"{item} x{item_quantities.get(item, 0)}", True, black)
                text_rect = text.get_rect(center=slot_rect.center)

                # Check if the item is selected
                if selected_item_index == (i, j):
                    pygame.draw.rect(screen, selected_color, slot_rect, 0)  # Use selected_color to fill the slot
                    pygame.draw.rect(screen, black, slot_rect, 2)  # Draw slot border for selected item
                else:
                    pygame.draw.rect(screen, white, slot_rect, 0)  # Use white to fill the slot for unselected items

                screen.blit(text, text_rect)

                # Display item type and color-code them
                item_type = item_info["type"]
                type_text = font.render(item_type, True, black)

                if item_type == "Weapon":
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(slot_rect.x, slot_rect.y - 30, cell_size, 25))
                elif item_type == "Potion":
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(slot_rect.x, slot_rect.y - 30, cell_size, 25))
                else:
                    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(slot_rect.x, slot_rect.y - 30, cell_size, 25))

                screen.blit(type_text, (slot_rect.x + 5, slot_rect.y - 30))

                # Highlight items that match the search query
                if search_query.lower() in item.lower():
                    pygame.draw.rect(screen, (255, 255, 0), slot_rect, 2)  # Yellow highlight

    # Draw the "Drop" button
    pygame.draw.rect(screen, red, drop_button_rect)
    pygame.draw.rect(screen, black, drop_button_rect, 2)
    screen.blit(drop_button_text, (drop_button_x + 10, drop_button_y + 10))

    # Draw the dragged item if dragging
    if dragging:
        text = font.render(dragged_item, True, black)
        screen.blit(text, (pygame.mouse.get_pos()[0] + offset_x, pygame.mouse.get_pos()[1] + offset_y))

    # Draw the item information background with a border
    screen.blit(item_info_background, item_info_rect.topleft)

    # Draw the selected item information
    if selected_item_info:
        screen.blit(selected_item_info, (cell_padding, screen_height - item_info_rect.height + 5))

    pygame.display.flip()

# Quit pygame
pygame.quit()
