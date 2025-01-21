from tkinter import *
import sqlite3
import random
import logic  # Ensure logic.py is available and functional
from tkinter import messagebox

# Background color for the GUI
bg_clr = "lightblue"

# Set up the Tkinter root window
root = Tk()
root.title("Craps 3.4")
root.geometry("400x400")
root.config(background=bg_clr)

# Load dice images into a list
try:
    dice_images = [
        PhotoImage(file=f"images/dice-{i}.png") for i in range(1, 7)
    ]
except Exception as e:
    messagebox.showerror("Error", f"Error loading dice images: {e}")
    root.destroy()

# Labels to display the dice images
dice1_label = Label(root, bg=bg_clr)
dice1_label.place(x=75, y=250)

dice2_label = Label(root, bg=bg_clr)
dice2_label.place(x=200, y=250)

# GUI Labels and Buttons
dice_label = Label(root, text="Dice: ", bg=bg_clr)
dice_label.pack(pady=10)

status_label = Label(root, text="Welcome to Craps!", bg=bg_clr)
status_label.pack(pady=10)

roll_button = Button(root, text="Roll Dice", bg="white")
roll_button.pack(pady=10)

game_point_label = Label(root, text="Game Point:", bg=bg_clr)
game_point_label.place(x=25, y=10)

payout_label = Label(root, text="Payout: $0", bg=bg_clr)
payout_label.place(x=25, y=35)

wager_label = Label(root, text="Wager: $0", bg=bg_clr)
wager_label.pack(pady=10)

wager_var = IntVar(value=5)

for amount in [5, 10, 25]:
    Radiobutton(
        root, text=f"${amount}", variable=wager_var, value=amount,
        command=lambda: casino.set_wager(wager_var.get()), bg=bg_clr
    ).pack()


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
        self.is_win = False
        self.status_label = status_label
        self.payout_label = payout_label
        self.initialize_database()

    def initialize_database(self):
        """Initialize the database and ensure the Game_ID table exists."""
        conn = sqlite3.connect('game_database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Game_ID (
            GameID INTEGER PRIMARY KEY
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Payouts (
            GameID INTEGER,
            WagerAmount REAL,
            PayoutAmount REAL,
            Win BOOLEAN
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
        return self.score in [2, 3, 12]

    def is_winner(self):
        """Check if the roll is a natural winner."""
        return self.score in [7, 11]

    def is_match(self):
        """Check if the dice match (doubles)."""
        return self.die1 == self.die2

    def play_game(self):
        """Play the craps game logic."""
        self.roll_dice()
        game_id = self.get_game_id()
        is_match = self.is_match()

        if self.comeout:  # Comeout Roll
            if self.is_craps():
                logic.insert_roll_data(game_id, self.die1, self.die2, self.score, is_match)
                self.set_payout()
                self.status_label.config(text="Craps! You lose.")
                self.is_win = False
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            elif self.is_winner():
                logic.insert_roll_data(game_id, self.die1, self.die2, self.score, is_match)
                self.set_payout()
                self.is_win = True
                self.status_label.config(text="You win on the Comeout Roll!")
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            else:
                self.game_point = self.score
                self.status_label.config(text=f"Point established: {self.game_point}")
                logic.insert_roll_data(game_id, self.die1, self.die2, self.score, is_match)
                self.set_payout()
                game_point_label.config(text=f"Game Point: {self.game_point}")
                self.comeout = False
        else:  # Subsequent rolls
            if self.score == self.game_point:
                self.status_label.config(text="You hit the point! You win!")
                logic.insert_roll_data(game_id, self.die1, self.die2, self.score, is_match)
                self.is_win = True
                self.set_payout()
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            elif self.score == 7:
                self.status_label.config(text="Seven out! You lose.")
                logic.insert_roll_data(game_id, self.die1, self.die2, self.score, is_match)
                self.is_win = False
                self.comeout = True
                game_point_label.config(text="Game Point: None")
            else:
                self.status_label.config(text="Roll again!")
                logic.insert_roll_data(game_id, self.die1, self.die2, self.score, is_match)

    def set_wager(self, amount):
        """Set the wager amount."""
        self.wager_amount = amount
        wager_label.config(text=f"Wager: ${self.wager_amount}")

    def set_payout(self):
        """Calculate and set the payout."""
        if self.is_win:
            self.payout_amount = self.wager_amount * 2
        else:
            self.payout_amount = 0
        self.payout_label.config(text=f"Payout: ${self.payout_amount}")
        insert_into_payout(self.game_id, self.wager_amount, self.payout_amount, self.is_win)


def insert_into_payout(game_id, wager, payout, win):
    """Insert payout details into the database."""
    conn = sqlite3.connect('game_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Payouts (GameID, WagerAmount, PayoutAmount, Win) VALUES (?, ?, ?, ?)',
                   (game_id, wager, payout, win))
    conn.commit()
    conn.close()


# Initialize the Casino object
casino = Casino()

# GUI Functionality
def roll_dice_gui():
    """Handle the roll dice button click."""
    casino.play_game()

    # Update dice images
    dice1_label.config(image=dice_images[casino.die1 - 1])
    dice2_label.config(image=dice_images[casino.die2 - 1])

roll_button.config(command=roll_dice_gui)
# for i in range(500):
#     print(f'print i: {i}')
#     roll_dice_gui()

# Run the Tkinter main loop
if __name__ == "__main__":

    root.mainloop()
