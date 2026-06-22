# Room class for Tiny Hero, Big Dungeon


import random
from enemy import Enemy
from item import Item


class Room:
    
    # Represents a room in the dungeon
    
    def __init__(self, room_number, max_rooms):

        # Boss room
        if room_number == max_rooms:
            self.room_type = "Boss"

        else:
            self.room_type = random.choice( 
                ["Combat", "Treasure", "Empty"]
            )

    def create_enemy(self):

        # Creates and returns an enemy if one exists in the room.

        if self.room_type == "Combat":
            return Enemy()
        
        elif self.room_type == "Boss":
            return Enemy(boss=True)
        
        return None
    
    def get_reward(self):

        # Returns a random amount of gold of treasure exsits.

        if self.room_type == "Treasure":

            treasure_rewards = [
                Item("Small Potion", "Potion", 30),
                Item("Large Potion", "Potion", 50)
            ]

            return random.choice(treasure_rewards)
        
        return None
