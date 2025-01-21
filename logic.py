import sqlite3


def insert_roll_data(game_id, die1, die2, score, is_match):
    """
    Insert a new roll data entry into the 'roll_data' table.

    Parameters:
        game_id (int): The ID of the game the roll belongs to.
        die1 (int): The value of the first die.
        die2 (int): The value of the second die.
        score (int): The total score for the roll.
        is_match (bool): Whether this roll matches certain criteria (e.g., point match).
    """
    try:
        conn = sqlite3.connect('Main.db')  # Connect to the Main.db database
        cursor = conn.cursor()

        # Insert the new roll data into the 'roll_data' table
        cursor.execute(
            "INSERT INTO roll_data (game_id, die1, die2, score, is_match) VALUES (?, ?, ?, ?,?)",
            (game_id, die1, die2, score, is_match)
        )

        conn.commit()  # Commit the transaction
        print("Roll data inserted successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()  # Ensure the connection is closed

def insert_into_payout(game_id, wager_amount,  payout_amount):
    conn = sqlite3.connect('game_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS payout (
        game_id INTEGER PRIMARY KEY,
        wager_amount INTEGER,
        payout_amount INTEGER
    );''')
    conn.commit()
    conn.close()
    print("Table 'payout' created successfully.")

def clear_wager_data():
    conn = sqlite3.connect('game_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payouts")
    conn.commit()
    conn.close()

def delete_roll_data():
    conn = sqlite3.connect('Main.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM roll_data")
    conn.commit()
    conn.close()

#delete_roll_data()

#clear_wager_data()