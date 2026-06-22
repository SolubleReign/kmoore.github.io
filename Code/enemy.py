# Enemy class for Tiny Hero, Big Dungeon.

import random
from character import Character


class Enemy(Character):
    
    # Represents a random enemy
    
    def __init__(self, boss=False):

        if boss:
            super().__init__("Dungeon Boss", 120, 25)

        else:
            enemy_types = [
                ("Goblin", 30, 10),
                ("Skeleton", 40, 12),
                ("Orc", 50, 15)
            ]

            name, health, attack = random.choice(enemy_types)

            super().__init__(name, health, attack)
