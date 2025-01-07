import tkinter as tk
from random import choice
from tkinter import messagebox
import json
import os
from datetime import datetime
# achievements
ACHIEVEMENTS = {
    "first_win": {"name": "First Victory", "description": "Win your first game", "icon": "🏆"},
    "perfect_game": {"name": "Perfect Game", "description": "Win without any wrong guesses", "icon": "⭐"},
    "winning_streak_5": {"name": "winning Streak", "description": "Win 5 games in a row", "icon": "🔥"},
    "category_master": {"name": "Category Master", "description": "Win in every category", "icon": "👑"},
    "quick_solver": {"name": "Quick Solver", "description": "Guess the word with 4 or more guesses left", "icon": "⚡"}
}
# Dictionary of word categories and their corresponding words
WORD_CATEGORIES = {
    "Movies": ["AVATAR", "TITANIC", "INCEPTION", "JAWS", "MATRIX"],
    "Animals": ["ELEPHANT", "GIRAFFE", "DOLPHIN", "PENGUIN", "LION"],
    "Countries": ["FRANCE", "JAPAN", "EGYPT", "BRAZIL", "INDIA"],
    "Sports": ["FOOTBALL", "TENNIS", "CRICKET", "BOXING", "RUGBY"],
    "Food": ["PIZZA", "BURGER", "SUSHI", "PASTA", "TACO"]
}


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("700x700")

        # Main menu container
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(expand=True, fill='both')

        # Title
        tk.Label(self.menu_frame,
                 text="HANGMAN GAME",
                 font=("Helvetica", 32, "bold")).pack(pady=30)

        # Start Game Button (Single Player)
        tk.Button(self.menu_frame,
                  text="Single Player",
                  font=("Helvetica", 16),
                  command=self.show_categories).pack(pady=20)

        # Add PvP Button
        tk.Button(self.menu_frame,
                  text="Player vs Player",
                  font=("Helvetica", 16),
                  command=self.start_pvp).pack(pady=20)

        tk.Button(self.menu_frame,
                  text="Game History",
                  font=("Helvetica", 16),
                  command=self.show_history).pack(pady=20)

        # Exit Button
        tk.Button(self.menu_frame,
                  text="Exit",
                  font=("Helvetica", 16),
                  command=root.quit).pack(pady=10)
    # history
    def show_history(self):
        self.menu_frame.pack_forget()
        GameHistoryWindow(self.root)
    # Add this method to MainMenu class
    def start_pvp(self):
        self.menu_frame.pack_forget()
        PvPHangmanGame(self.root)

    def show_categories(self):
        # Hide main menu
        self.menu_frame.pack_forget()

        # Create category selection frame
        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack(expand=True, fill='both')

        tk.Label(self.category_frame,
                 text="Select Category",
                 font=("Helvetica", 24, "bold")).pack(pady=20)

        # Create buttons for each category
        for category in WORD_CATEGORIES.keys():
            tk.Button(self.category_frame,
                      text=category,
                      font=("Helvetica", 14),
                      width=20,
                      command=lambda c=category: self.start_game(c)).pack(pady=10)

        # Back button
        tk.Button(self.category_frame,
                  text="Back to Main Menu",
                  font=("Helvetica", 12),
                  command=self.back_to_menu).pack(pady=20)

    def back_to_menu(self):
        self.category_frame.pack_forget()
        self.menu_frame.pack(expand=True, fill='both')

    def start_game(self, category):
        self.category_frame.pack_forget()
        HangmanGame(self.root, category)

class GameHistoryWindow:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill='both')

        # Title
        tk.Label(self.frame, text="Game History", font=("Helvetica", 24, "bold")).pack(pady=10)

        # Stats Frame
        stats_frame = tk.Frame(self.frame)
        stats_frame.pack(pady=10)

        # Load stats
        self.game_stats = GameStats()
        stats = self.game_stats.stats

        # Display overall stats
        tk.Label(stats_frame,
                 text=f"Total Games: {stats['total_games']}\n"
                      f"Wins: {stats['total_wins']}\n"
                      f"Current Streak: {stats['current_streak']}\n"
                      f"Best Streak: {stats['best_streak']}",
                 font=("Helvetica", 12)).pack()

        # Achievements Frame
        achievement_frame = tk.Frame(self.frame)
        achievement_frame.pack(pady=10)
        tk.Label(achievement_frame, text="Achievements", font=("Helvetica", 16, "bold")).pack()

        for achievement_id in stats['achievements']:
            achievement = ACHIEVEMENTS[achievement_id]
            tk.Label(achievement_frame,
                     text=f"{achievement['icon']} {achievement['name']}: {achievement['description']}",
                     font=("Helvetica", 10)).pack()

        # Game History List
        history_frame = tk.Frame(self.frame)
        history_frame.pack(pady=10, fill='both', expand=True)
        tk.Label(history_frame, text="Recent Games", font=("Helvetica", 16, "bold")).pack()

        for game in stats['game_history'][:10]:  # Show last 10 games
            tk.Label(history_frame,
                     text=f"{game['date']} - {game['category']}: {game['word']} "
                          f"({game['result']} - {game['guesses_left']} guesses left)",
                     font=("Helvetica", 10)).pack()

        # Back button
        tk.Button(self.frame,
                  text="Back to Main Menu",
                  command=self.return_to_menu).pack(pady=10)

    def return_to_menu(self):
        self.frame.destroy()
        MainMenu(self.root)

class GameStats:
    def __init__(self):
        self.stats_file = "hangman_stats.json"
        self.load_stats()

    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                "game_history": [],
                "achievements": [],
                "total_games": 0,
                "total_wins": 0,
                "current_streak": 0,
                "best_streak": 0,
                "category_wins": {}
            }

    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)

    def add_game(self, word, category, guesses_left, is_win):
        game_record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word": word,
            "category": category,
            "guesses_left": guesses_left,
            "result": "Win" if is_win else "Loss"
        }
        self.stats["game_history"].insert(0, game_record)  # Add at beginning
        self.stats["total_games"] += 1

        if is_win:
            self.stats["total_wins"] += 1
            self.stats["current_streak"] += 1
            self.stats["best_streak"] = max(self.stats["best_streak"], self.stats["current_streak"])

            # Update category wins
            if category not in self.stats["category_wins"]:
                self.stats["category_wins"][category] = 0
            self.stats["category_wins"][category] += 1

            # Check achievements
            self.check_achievements(guesses_left, category)
        else:
            self.stats["current_streak"] = 0

        # Keep only last 50 games
        self.stats["game_history"] = self.stats["game_history"][:50]
        self.save_stats()

    def check_achievements(self, guesses_left, category):
        achievements = self.stats["achievements"]

        # First win
        if self.stats["total_wins"] == 1 and "first_win" not in achievements:
            achievements.append("first_win")

        # Perfect game
        if guesses_left == 6 and "perfect_game" not in achievements:
            achievements.append("perfect_game")

        # Winning streak
        if self.stats["current_streak"] >= 5 and "winning_streak_5" not in achievements:
            achievements.append("winning_streak_5")

        # Category master
        if len(self.stats["category_wins"]) == len(WORD_CATEGORIES) and "category_master" not in achievements:
            achievements.append("category_master")

        # Quick solver
        if guesses_left >= 4 and "quick_solver" not in achievements:
            achievements.append("quick_solver")

class PvPHangmanGame:
    def __init__(self, root):
        self.root = root
        self.setup_word_input()

    def setup_word_input(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(expand=True, fill='both')

        tk.Label(self.input_frame,
                text="Player 1: Enter a word for Player 2 to guess",
                font=("Helvetica", 18)).pack(pady=20)

        # Entry widget for the word
        self.word_var = tk.StringVar()
        self.word_entry = tk.Entry(self.input_frame,
                                 textvariable=self.word_var,
                                 font=("Helvetica", 14),
                                 show="*")  # Hide the input with asterisks
        self.word_entry.pack(pady=10)

        # Submit button
        tk.Button(self.input_frame,
                 text="Start Game",
                 font=("Helvetica", 14),
                 command=self.start_game).pack(pady=10)

        # Back button
        tk.Button(self.input_frame,
                 text="Back to Main Menu",
                 font=("Helvetica", 12),
                 command=self.return_to_menu).pack(pady=10)

    def start_game(self):
        word = self.word_var.get().upper()
        if not word:
            messagebox.showerror("Error", "Please enter a word!")
            return
        if not word.isalpha():
            messagebox.showerror("Error", "Word must contain only letters!")
            return

        self.input_frame.destroy()
        HangmanGame(self.root, "PvP", custom_word=word)

    def return_to_menu(self):
        self.input_frame.destroy()
        MainMenu(self.root)

class HangmanGame:
    def __init__(self, root, category, custom_word=None):
        self.root = root
        self.game_stats = GameStats()
        self.category = category
        self.game_frame = tk.Frame(root)
        self.game_frame.pack(expand=True, fill='both')

        if custom_word:
            self.root.title("Hangman Game - Player vs Player")
            self.word = custom_word
        else:
            self.root.title(f"Hangman Game - {category}")
            self.word = choice(WORD_CATEGORIES[category])

        self.guesses = 6
        self.correct_guesses = ["_"] * len(self.word)

        # Display for current word status
        self.word_label = tk.Label(self.game_frame, text=" ".join(self.correct_guesses), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        # Display for remaining guesses
        self.guess_label = tk.Label(self.game_frame, text=f"Guesses left: {self.guesses}", font=("Helvetica", 14))
        self.guess_label.pack(pady=10)

        # Canvas for hangman drawing
        self.canvas = tk.Canvas(self.game_frame, width=200, height=250, bg="white")
        self.canvas.pack(pady=20)
        self.draw_base()

        # QWERTY Keyboard Layout
        qwerty_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        # Frame for alphabet buttons
        self.buttons_frame = tk.Frame(self.game_frame)
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

        # Back to menu button
        tk.Button(self.game_frame,
                  text="Back to Main Menu",
                  command=self.return_to_menu).pack(pady=10)

        self.hangman_parts = [self.draw_head, self.draw_body, self.draw_left_arm,
                              self.draw_right_arm, self.draw_left_leg, self.draw_right_leg]

    def return_to_menu(self):
        self.game_frame.destroy()
        MainMenu(self.root)

    # Keep all your existing methods (draw_base, draw_head, etc.)
    # Just add 'self.game_frame' instead of 'root' where needed

    # Your existing methods here (draw_base, draw_head, draw_body, etc.)
    # Copy all the drawing methods from your original code here

    def draw_base(self):
        self.canvas.create_line(50, 230, 150, 230, width=2)
        self.canvas.create_line(100, 230, 100, 50, width=2)
        self.canvas.create_line(100, 50, 150, 50, width=2)
        self.canvas.create_line(150, 50, 150, 70, width=2)

    def draw_head(self):
        self.canvas.create_oval(140, 70, 160, 90, width=2)

    def draw_body(self):
        self.canvas.create_line(150, 90, 150, 150, width=2)

    def draw_left_arm(self):
        self.canvas.create_line(150, 100, 130, 120, width=2)

    def draw_right_arm(self):
        self.canvas.create_line(150, 100, 170, 120, width=2)

    def draw_left_leg(self):
        self.canvas.create_line(150, 150, 130, 180, width=2)

    def draw_right_leg(self):
        self.canvas.create_line(150, 150, 170, 180, width=2)

    def guess_letter(self, letter):
        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.correct_guesses[i] = letter
            self.word_label.config(text=" ".join(self.correct_guesses))

            if "_" not in self.correct_guesses:
                self.end_game("Congratulations! You guessed the word!")
        else:
            self.hangman_parts[6 - self.guesses]()
            self.guesses -= 1
            self.guess_label.config(text=f"Guesses left: {self.guesses}")
            if self.guesses == 0:
                self.end_game(f"Game Over! The word was '{self.word}'")

        self.buttons[letter].config(state="disabled")

    def end_game(self, message):
        for button in self.buttons.values():
            button.config(state="disabled")
        self.guess_label.config(text=message)
        is_win = "_" not in self.correct_guesses
        self.game_stats.add_game(
            word=self.word,
            category=self.category,
            guesses_left=self.guesses,
            is_win=is_win
        )

        # Add Play Again button
        tk.Button(self.game_frame,
                  text="Play Again",
                  command=self.return_to_menu).pack(pady=10)


# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()