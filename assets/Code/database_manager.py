import sqlite3


class DatabaseManager:

    DATABASE_NAME = "game.db"

    @staticmethod
    def initialize_database():

        connection = sqlite3.connect(
            DatabaseManager.DATABASE_NAME
        )

        cursor = connection.cursor()

        # Player save data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                health INTEGER,
                attack INTEGER,
                gold INTEGER,
                current_room INTEGER
            )
        """)

        # Inventory data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                item_name TEXT,
                item_type TEXT,
                item_value INTEGER
            )
        """)

        connection.commit()
        connection.close()

    @staticmethod
    def save_player(player, current_room):

        connection = sqlite3.connect(
            DatabaseManager.DATABASE_NAME
        )

        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM players"
        )

        cursor.execute("""
            INSERT INTO players
            (
                name,
                health,
                attack,
                gold,
                current_room
            )
            VALUES (?,?,?,?,?)
        """,
        (
            player.name,
            player.health,
            player.attack,
            player.gold,
            current_room
        ))

        connection.commit()
        connection.close()

    @staticmethod
    def load_player():

        connection = sqlite3.connect(
            DatabaseManager.DATABASE_NAME
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                name,
                health,
                attack,
                gold,
                current_room
            FROM players
            LIMIT 1
        """)

        result = cursor.fetchone()

        connection.close()

        return result

    @staticmethod
    def save_inventory(player):

        connection = sqlite3.connect(
            DatabaseManager.DATABASE_NAME
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM inventory
            WHERE player_name = ?
            """,
            (player.name,)
        )

        for item in player.inventory:

            cursor.execute("""
                INSERT INTO inventory
                (
                    player_name,
                    item_name,
                    item_type,
                    item_value
                )
                VALUES (?,?,?,?)
            """,
            (
                player.name,
                item.name,
                item.item_type,
                item.value
            ))

        connection.commit()
        connection.close()

    @staticmethod
    def load_inventory(player_name):

        connection = sqlite3.connect(
            DatabaseManager.DATABASE_NAME
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                item_name,
                item_type,
                item_value
            FROM inventory
            WHERE player_name = ?
        """,
        (player_name,)
        )

        inventory = cursor.fetchall()

        connection.close()

        return inventory
