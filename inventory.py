total_score = 0

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = {}
        self.score = 0  # Add a score attribute

    def add_item(self, item):
        if item.name not in self.items:
            self.items[item.name] = 0

        if len(self.items) < self.capacity and self.has_required_items(item):
            self.items[item.name] += 1
            self.update_score(item)  # Update the score when adding an item
            return True

        return False

    def remove_item(self, item_name):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            return True

        return False

    def has_item(self, item_name):
        return item_name in self.items and self.items[item_name] > 0

    def has_required_items(self, item):
        if hasattr(item, 'required_items'):
            for required_item, count in item.required_items.items():
                if self.items.get(required_item, 0) < count:
                    return False
        return True

    def update_score(self, item):
        if hasattr(item, 'score_value'):
            if item.name == "Scales":
                self.score += 2  # Scales now give 2 points each
            else:
                self.score += item.score_value
