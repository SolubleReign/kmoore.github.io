# Base Character class for Tiny Hero, Big Dungeon.

class Character:
    # Base class shared by Player and Enemy.

    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        # Returns True if the character is alive.

        return self.health > 0
    
    def take_damage(self, damage):
        #Reduces character health.
        self.health -= damage

        if self.health < 0:
            self.health = 0
