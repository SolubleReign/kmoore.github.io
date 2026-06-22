# Item system for Tiny Hero, Big Dungeon.

class Item:
    # Represents an item.

    def __init__(
            self, 
            name, 
            item_type, 
            value
    ):
        self.name = name
        self.item_type = item_type
        self.value = value
        

    def use(self, player):
        # Apply item effect.

        if self.item_type == "Potion":
            player.heal(self.value)
            print(f"{player.name} healed for {self.value} health!")

    def __str__(self): 
        return self.name
