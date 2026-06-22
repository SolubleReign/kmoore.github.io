# Enemy Journal system for Tiny Hero, Big Dungeon.

class EnemyJournal:

    def __init__(self):

        # Stores enemy records
        self.enemies = {}

    def record_enemy(self, enemy):

        key = enemy.name.lower()

        if key not in self.enemies:

            self.enemies[key] = {
                "display_name": enemy.name,
                "health": enemy.health,
                "attack": enemy.attack,
                "defeated": 1
            }

        else:
            self.enemies[key]["defeated"] += 1

    def search_enemy(self, name):

        return self.enemies.get(name.lower())

    def sort_by_health(self):

        return sorted(
            self.enemies.values(),
            key=lambda enemy: enemy["health"],
            reverse=True
        )

    def sort_by_attack(self):

        return sorted(
           self.enemies.values(),
            key=lambda enemy: enemy["attack"],
            reverse=True
        )
    
    def sort_alphabetically(self):

        return sorted(
            self.enemies.values(),
            key=lambda enemy: enemy["display_name"]
        )
    
    def strongest_enemy(self):

        if not self.enemies:
            return None
        
        return max(
            self.enemies.values(),
            key=lambda enemy: enemy["attack"]
        )
    
    def total_defeated(self):

        return sum(
            enemy["defeated"]
            for enemy in self.enemies.values()
        )
    
    def total_discovered(self):

        return len(self.enemies)

    def show_journal(self):

        print("\n=== Enemy Journal ===")

        if not self.enemies:
            print("No enemies recorded.")
            return

        for enemy in self.sort_alphabetically():

            print(f"\n{enemy['display_name']}")
            print(f"Health: {enemy['health']}")
            print(f"Attack: {enemy['attack']}")
            print(f"Defeated: {enemy['defeated']}")

        print("\n=== Journal Statistics ===")

        print(
            f"Total Enemy Types Discovered: "
            f"{self.total_discovered()}"
        )

        print(
            f"Total Enemies Defeated: "
            f"{self.total_defeated()}"
        )

        strongest = self.strongest_enemy()

        if strongest:

            print(
                f"Strongest Enemy: "
                f"{strongest['display_name']}"
            )

            print(
                f"Attack Power: "
                f"{strongest['attack']}"
            )
