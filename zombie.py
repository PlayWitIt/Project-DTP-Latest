from enemies import BaseEnemy

class Zombie(BaseEnemy):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, 50, 50, target_x, target_y)
        self.color = (0, 128, 0)  # Green color for zombies
        self.damage = 30  # Higher damage for zombies

    def interact(self):
        print("A zombie is attacking!")
        super().interact()  # Call the base class interact method

    # Add any additional methods or attributes specific to zombies here