
# Player class for Tiny Hero, Big Dungeon.

from character import Character

class Player(Character):
    
# Represents the player character.
   

    def __init__(self, name):
        super().__init__(name, 100, 20)

        self.gold = 0
        self.inventory = []

    def heal(self, amount):
        
    # Restores player health.
       
        self.health += amount

        if self.health > 100:
            self.health = 100
      
    def add_gold(self, amount):

    # Adds gold to player inventory.

        self.gold += amount

    def add_item(self, item):
        self.inventory.append(item)

    def show_inventory(self):
        print("\n=== Inventory ===") 

        if not self.inventory:
            print("Inventory is empty.")
            return
        
        for index, item in enumerate(
            self.inventory, 
            start=1
        ):
            print(
                f"{index}. " 
                f"{item.name}"
            )

    def use_potion(self):

        potions = [
            item for item in self.inventory
            if item.item_type == "Potion"
        ]

        if not potions:
            print("No potions available.")
            return
        
        potion = potions[0]

        potion.use(self)

        self.inventory.remove(potion)
   
    def show_stats(self):
        
    # Displays current player statistics.
        
        print(
            f"\n{self.name}'s Stats"
        )
        print(
            f"Health: {self.health}"
        )
        print(
            f"Attack: {self.attack}"
        )
        print(
            f"Gold: {self.gold}\n"
        )
        print(
            f"Inventory Items: "
            f"{len(self.inventory)}"
        )

        print()
