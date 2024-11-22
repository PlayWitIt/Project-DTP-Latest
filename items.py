class Item:
    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.collected = False
        self.name = name

    def collides_with_player(self, player_x, player_y, player_width, player_height):
        return (
            player_x < self.x + self.width and
            player_x + player_width > self.x and
            player_y < self.y + self.height and
            player_y + player_height > self.y
        )

class Scales(Item):
    def __init__(self, x, y):
        super().__init__(x, y, width=40, height=40, color=(0, 255, 0), name="Scales")

class Ectoplasm(Item):
    def __init__(self, x, y):
        super().__init__(x, y, width=40, height=40, color=(0, 0, 255), name="Ectoplasm")
