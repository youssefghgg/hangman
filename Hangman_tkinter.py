import tkinter as tk
from random import choice

# List of words for the game
words = ["PYTHON", "HANGMAN", "COMPUTER", "PROGRAMMING", "SCIENCE"]


# Main Hangman Game class
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.word = choice(words)  # Randomly select a word
        self.guesses = 6  # Number of wrong guesses allowed
        self.correct_guesses = ["_"] * len(self.word)  # Placeholder for correct guesses

        # Display for current word status
        self.word_label = tk.Label(root, text=" ".join(self.correct_guesses), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        # Display for remaining guesses
        self.guess_label = tk.Label(root, text=f"Guesses left: {self.guesses}", font=("Helvetica", 14))
        self.guess_label.pack(pady=10)

        # Canvas for hangman drawing
        self.canvas = tk.Canvas(root, width=200, height=250, bg="white")
        self.canvas.pack(pady=20)
        self.draw_base()  # Draw initial base for hangman

        # QWERTY Keyboard Layout
        qwerty_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        # Frame for alphabet buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        # Create buttons according to QWERTY layout
        self.buttons = {}
        for row, keys in enumerate(qwerty_layout):
            row_frame = tk.Frame(self.buttons_frame)
            row_frame.pack(pady=5)
            for key in keys:
                button = tk.Button(row_frame, text=key, font=("Helvetica", 14), width=3,
                                   command=lambda l=key: self.guess_letter(l))
                button.pack(side="left", padx=3)
                self.buttons[key] = button

        # List to store drawing functions for each body part
        self.hangman_parts = [self.draw_head, self.draw_body, self.draw_left_arm,
                              self.draw_right_arm, self.draw_left_leg, self.draw_right_leg]

    def draw_base(self):
        # Draw the base structure of the hangman stand
        self.canvas.create_line(50, 230, 150, 230, width=2)  # Base
        self.canvas.create_line(100, 230, 100, 50, width=2)  # Pole
        self.canvas.create_line(100, 50, 150, 50, width=2)  # Top beam
        self.canvas.create_line(150, 50, 150, 70, width=2)  # Rope

    # Functions to draw each body part
    def draw_head(self):
        self.canvas.create_oval(140, 70, 160, 90, width=2)  # Head

    def draw_body(self):
        self.canvas.create_line(150, 90, 150, 150, width=2)  # Body

    def draw_left_arm(self):
        self.canvas.create_line(150, 100, 130, 120, width=2)  # Left arm

    def draw_right_arm(self):
        self.canvas.create_line(150, 100, 170, 120, width=2)  # Right arm

    def draw_left_leg(self):
        self.canvas.create_line(150, 150, 130, 180, width=2)  # Left leg

    def draw_right_leg(self):
        self.canvas.create_line(150, 150, 170, 180, width=2)  # Right leg

    def guess_letter(self, letter):
        if letter in self.word:
            # Correct guess: Update the word display
            for i, char in enumerate(self.word):
                if char == letter:
                    self.correct_guesses[i] = letter
            self.word_label.config(text=" ".join(self.correct_guesses))

            # Check if the word is fully guessed
            if "_" not in self.correct_guesses:
                self.end_game("Congratulations! You guessed the word!")
        else:
            # Wrong guess: Draw a body part and reduce guesses
            self.hangman_parts[6 - self.guesses]()  # Draw the next body part
            self.guesses -= 1
            self.guess_label.config(text=f"Guesses left: {self.guesses}")
            if self.guesses == 0:
                self.end_game(f"Game Over! The word was '{self.word}'")

        # Disable the button
        self.buttons[letter].config(state="disabled")

    def end_game(self, message):
        # Disable all buttons
        for button in self.buttons.values():
            button.config(state="disabled")

        # Display end game message
        self.guess_label.config(text=message)


# Create the main window
root = tk.Tk()
game = HangmanGame(root)
root.mainloop()