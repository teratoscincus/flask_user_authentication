"""
Contains a class to handle database operations.

Run as a script to create the database and tables.
"""

import sqlite3


class Database:
    """Handle database operations."""

    def __init__(self, database):
        """
        Init connection and cursor attributes.

        If the database file doesn't yet exist, one will be created.

        The database parameter takes a string argument, specifying the path to the
        database for the connection.
        """
        # Establish connection and create cursor.
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def create_tables(self, schema):
        """
        The schema parameter takes a string argument, specifying the path to an .sql
        file expected to contain a schema for the database.
        """
        # Make sure tables exist.
        with open(schema) as f:
            self.connection.executescript(f.read())


if __name__ == "__main__":
    # Imports necessary to create the database and tables.
    import members_only.config as config

    # Create database and tables.
    db = Database(config.DATABASE_PATH)
    # db = Database("./demo.sqlite3")
    print(f"Database successfully created")

    db.create_tables(config.SCHEMA_PATH)
    print(f"Tables successfully created from schema")
