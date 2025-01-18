from tkinter import *
import sqlite3
import random
import logic
from tkinter import messagebox

# Background color for the GUI
bg_clr = "lightblue"

# Set up the Tkinter root window
root = Tk()
root.title("Craps 3.4")
root.geometry("400x400")
root.config(background=bg_clr)

# Load dice images into a list
dice_images = [
    PhotoImage(file=f"images/dice-{i}.png") for i in range(1, 7)
]

# Labels to display the dice images
dice1_label = Label(root, bg=bg_clr)
dice1_label.place(x=75, y=250)

dice2_label = Label(root, bg=bg_clr)
dice2_label.place(x=200, y=250)


# Casino Class
class Casino:
    def __init__(self):
        self.game_id = 0
        self.die1 = 0
        self.die2 = 0
        self.score = 0
        self.game_point = 0
        self.comeout = True
        self.wager_amount = 0
        self.payout_amount = 0
        self.initialize_database()

    def initialize_database(self):
        """Initialize the database and ensure the Game_ID table exists."""
        conn = sqlite3.connect('game_database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Game_ID (
            GameID INTEGER PRIMARY KEY
        )''')
        conn.commit()
        conn.close()

    def get_game_id(self):
        """Get a new game ID from the database."""
        conn = sqlite3.connect('game_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(GameID) FROM Game_ID")
        result = cursor.fetchone()
        self.game_id = 1 if result[0] is None else result[0] + 1
        cursor.execute('INSERT INTO Game_ID (GameID) VALUES (?)', (self.game_id,))
        conn.commit()
        conn.close()
        return self.game_id

    def roll_dice(self):
        """Roll the dice and calculate the score."""
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.score = self.die1 + self.die2
        return self.score, self.die1, self.die2

    def is_craps(self):
        """Check if the roll is craps."""
        craps = [2, 3, 12]
        return self.score in craps

    def is_winner(self):
        """Check if the roll is a natural winner."""
        return self.score in [7, 11]

    def is_match(self):
        """Check if the dice match (doubles)."""
        return self.die1 == self.die2

    def play_game(self):
        """Play the craps game logic."""
        self.roll_dice()
        gameID = self.get_game_id()
        is_match = self.is_match()

        if self.comeout:  # Comeout Roll
            if self.is_craps():
                logic.insert_roll_data(gameID, self.die1, self.die2, self.score, is_match)
                status_label.config(text="Craps! You lose.")
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            elif self.is_winner():
                logic.insert_roll_data(gameID, self.die1, self.die2, self.score, is_match)
                status_label.config(text="You win on the Comeout Roll!")
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            else:
                self.game_point = self.score
                status_label.config(text=f"Point established: {self.game_point}")
                logic.insert_roll_data(gameID, self.die1, self.die2, self.score, is_match)
                game_point_label.config(text=f"Game Point: {self.game_point}")
                self.comeout = False
        else:  # Subsequent rolls
            if self.score == self.game_point:
                status_label.config(text="You hit the point! You win!")
                logic.insert_roll_data(gameID, self.die1, self.die2, self.score, is_match)
                self.set_payout()
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            elif self.score == 7:
                status_label.config(text="Seven out! You lose.")
                logic.insert_roll_data(gameID, self.die1, self.die2, self.score, is_match)
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            else:
                status_label.config(text="Roll again!")
                logic.insert_roll_data(gameID, self.die1, self.die2, self.score, is_match)

    def set_wager(self, amount):
        """Set the wager amount."""
        self.wager_amount = amount
        wager_label.config(text=f"Wager: ${self.wager_amount}")

    def set_payout(self):
        """Set the payout amount."""
        self.payout_amount = self.wager_amount * 2
        payout_label.config(text=f"Payout: ${self.payout_amount}")


# Initialize the Casino object
casino = Casino()


# GUI Functionality
def roll_dice_gui():
    """Handle the roll dice button click."""
    score, die1, die2 = casino.roll_dice()
    dice_label.config(text=f"Dice: {die1}, {die2} (Total: {score})")
    casino.play_game()

    # Update dice images
    dice1_label.config(image=dice_images[die1 - 1])
    dice2_label.config(image=dice_images[die2 - 1])


# Wager selection
wager_label = Label(root, text="Wager: $0", bg=bg_clr)
wager_label.pack(pady=10)

wager_var = IntVar(value=5)

for amount in [5, 10, 25]:
    Radiobutton(
        root, text=f"${amount}", variable=wager_var, value=amount,
        command=lambda: casino.set_wager(wager_var.get()), bg=bg_clr
    ).pack()

# GUI Labels and Buttons
dice_label = Label(root, text="Dice: ", bg=bg_clr)
dice_label.pack(pady=10)

status_label = Label(root, text="Welcome to Craps!", bg=bg_clr)
status_label.pack(pady=10)

roll_button = Button(root, text="Roll Dice", command=roll_dice_gui, bg="white")
roll_button.pack(pady=10)

game_point_label = Label(root, text="Game Point:", bg=bg_clr)
game_point_label.place(x=25, y=10)

payout_label = Label(root, text="Payout: $0", bg=bg_clr)
payout_label.place(x=25, y=35)

# Run the Tkinter main loop
if __name__ == "__main__":
    root.mainloop()
