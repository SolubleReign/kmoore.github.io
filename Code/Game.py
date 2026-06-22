# Game controller for Tiny Hero, Big Dungeon.

import logging

from player import Player
from room import Room
from item import Item
from enemy_journal import EnemyJournal
from database_manager import DatabaseManager


# Configure logging
logging.basicConfig(
    filename="game.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Game:

    def __init__(self):

        self.player = None
        self.current_room = 1
        self.max_rooms = 7

        self.journal = EnemyJournal()

        DatabaseManager.initialize_database()

    def get_player_name(self):

        while True:

            try:

                name = input(
                    "Enter your hero's name: "
                ).strip()

                if not name:
                    raise ValueError(
                        "Name cannot be empty."
                    )

                return name

            except ValueError as error:
                print(error)

    def start(self):

        print("Welcome to Tiny Hero, Big Dungeon!")

        choice = input(
            "Load saved game? (y/n): "
        ).lower()

        # Load save
        if choice == "y":

            save_data = DatabaseManager.load_player()

            if save_data:

                self.player = Player(
                    save_data[0]
                )

                self.player.health = save_data[1]
                self.player.attack = save_data[2]
                self.player.gold = save_data[3]

                self.current_room = save_data[4]

                # Load inventory
                inventory_data = (
                    DatabaseManager.load_inventory(
                        self.player.name
                    )
                )

                for item_data in inventory_data:

                    item = Item(
                        item_data[0],
                        item_data[1],
                        item_data[2]
                    )

                    self.player.add_item(item)

                print(
                    "Game loaded successfully!"
                )

                logging.info(
                    f"Loaded save for "
                    f"{self.player.name}"
                )

            else:
                print("No save file found.")

        # Create new character
        if self.player is None:

            player_name = self.get_player_name()

            self.player = Player(
                player_name
            )

            logging.info(
                f"Game started for "
                f"{player_name}"
            )

        # Main game loop
        while (
            self.player.is_alive()
            and self.current_room <= self.max_rooms
        ):

            print(
                f"\n--- Room "
                f"{self.current_room} ---"
            )

            room = Room(
                self.current_room,
                self.max_rooms
            )

            self.enter_room(room)

            if self.player.is_alive():

                choice = input(
                    "\nPress Enter to continue "
                    "or type SAVE or JOURNAL: "
                ).lower()

                if choice == "save":

                    DatabaseManager.save_player(
                        self.player,
                        self.current_room
                    )

                    DatabaseManager.save_inventory(
                        self.player
                    )

                    print(
                        "Game Saved!"
                    )

                    logging.info(
                        f"{self.player.name} "
                        f"saved the game."
                    )

                elif choice == "journal":

                    self.journal_menu()

                self.current_room += 1

        self.end_game()

    def enter_room(self, room):

        enemy = room.create_enemy()

        if enemy:

            print(
                f"\nA {enemy.name} appears!"
            )

            logging.info(
                f"Enemy encountered: "
                f"{enemy.name}"
            )

            input(
                "\nPress Enter to begin battle..."
            )

            self.battle(enemy)

        else:

            print(
                "\nThe room is empty."
            )

        # Treasure reward
        if self.player.is_alive():

            reward = room.get_reward()

            if reward:

                print(
                    f"\nYou found a "
                    f"{reward.name}!"
                )

                self.player.add_item(
                    reward
                )

                logging.info(
                    f"Player found item: "
                    f"{reward.name}"
                )

        self.player.show_stats()
        self.player.show_inventory()

    def battle(self, enemy):

        print(
            f"\nBattle Start! "
            f"You are fighting a "
            f"{enemy.name}."
        )

        while (
            self.player.is_alive()
            and enemy.is_alive()
        ):

            print("\n=== Battle Menu ===")
            print("1. Attack")
            print("2. Use Potion")

            choice = input(
                "\nChoose an action: "
            )

            # Player Attack
            if choice == "1":

                input(
                    "\nPress Enter to attack..."
                )

                print(
                    f"\nYou attack the "
                    f"{enemy.name} for "
                    f"{self.player.attack} damage."
                )

                enemy.take_damage(
                    self.player.attack
                )

                print(
                    f"{enemy.name} Health: "
                    f"{enemy.health}"
                )

            # Use Potion
            elif choice == "2":

                self.player.use_potion()

                input(
                    "\nPress Enter to continue..."
                )

            else:

                print(
                    "Invalid choice."
                )

                continue

            # Enemy defeated
            if not enemy.is_alive():

                self.journal.record_enemy(
                    enemy
                )

                logging.info(
                    f"{enemy.name} defeated"
                )

                break

            # Enemy turn
            input(
                "\nPress Enter for enemy turn..."
            )

            print(
                f"\nThe {enemy.name} attacks "
                f"you for {enemy.attack} damage."
            )

            self.player.take_damage(
                enemy.attack
            )

            print(
                f"{self.player.name} Health: "
                f"{self.player.health}"
            )

            logging.info(
                f"{enemy.name} attacked "
                f"{self.player.name}"
            )

            if (
                self.player.is_alive()
                and enemy.is_alive()
            ):

                input(
                    "\nPress Enter for next round..."
                )

        if self.player.is_alive():

            print(
                f"\nYou defeated "
                f"the {enemy.name}!"
            )

            input(
                "\nPress Enter to continue..."
            )

        else:

            print(
                "\nYou were defeated!"
            )

            logging.info(
                "Player defeated"
            )

    def journal_menu(self):

        while True:

            print(
                "\n=== Enemy Journal Menu ==="
            )
            print("1. View Journal")
            print("2. Search Enemy")
            print("3. Sort by Health")
            print("4. Sort by Attack")
            print("5. Exit Journal")

            choice = input(
                "\nChoose an option: "
            )

            if choice == "1":

                self.journal.show_journal()

            elif choice == "2":

                name = input(
                    "Enter enemy name: "
                )

                enemy = (
                    self.journal.search_enemy(
                        name
                    )
                )

                if enemy:

                    print(
                        f"\n{enemy['display_name']}"
                    )
                    print(
                        f"Health: "
                        f"{enemy['health']}"
                    )
                    print(
                        f"Attack: "
                        f"{enemy['attack']}"
                    )
                    print(
                        f"Defeated: "
                        f"{enemy['defeated']}"
                    )

                else:

                    print(
                        "Enemy not found."
                    )

            elif choice == "3":

                print(
                    "\n=== Sorted by Health ==="
                )

                enemies = (
                    self.journal.sort_by_health()
                )

                for enemy in enemies:

                    print(
                        f"{enemy['display_name']} "
                        f"- "
                        f"{enemy['health']} Health"
                    )

            elif choice == "4":

                print(
                    "\n=== Sorted by Attack ==="
                )

                enemies = (
                    self.journal.sort_by_attack()
                )

                for enemy in enemies:

                    print(
                        f"{enemy['display_name']} "
                        f"- "
                        f"{enemy['attack']} Attack"
                    )

            elif choice == "5":

                break

            else:

                print(
                    "Invalid choice."
                )

    def end_game(self):

        print("\n=== Game Over ===")

        if self.player.is_alive():

            print(
                "Congratulations! "
                "You cleared the dungeon!"
            )

        else:

            print(
                "Your adventure has "
                "come to an end."
            )

        self.player.show_stats()

        print(
            "\nOpening Enemy Journal..."
        )

        self.journal_menu()

        logging.info(
            "Game ended"
        )
