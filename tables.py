import sqlite3

def create_table():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('game_database.db')
    cursor = conn.cursor()

    # SQL command to create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Game_ID (
        game_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        GameID INTEGER
    );
    """

    # Execute the query
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Table 'Game_ID' created successfully.")

# Call the function to create the table
#create_table()

import sqlite3


def create_roll_data_table():
    """Create the 'roll_data' table in the Main.db database."""
    conn = sqlite3.connect('Main.db')  # Connect to Main.db
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS roll_data (
        game_id INTEGER,
        die1 INTEGER,
        die2 INTEGER,
        score INTEGER,
        is_match BOOLEAN
    );
    """

    cursor.execute(create_table_query)  # Execute the query
    conn.commit()  # Commit the changes
    conn.close()  # Close the connection

create_roll_data_table()