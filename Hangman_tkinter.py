import tkinter as tk
from random import choice
from tkinter import messagebox
import json
import os
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import tkinter.ttk as ttk
import math

COLORS = {
    'primary': '#2C3E50',      # Dark blue-grey
    'secondary': '#3498DB',    # Bright blue
    'accent': '#E74C3C',       # Red
    'background': '#ECF0F1',   # Light grey
    'text': '#2C3E50',         # Dark blue-grey
    'button': '#2980B9',       # Darker blue
    'button_hover': '#3498DB', # Lighter blue
    'success': '#27AE60',      # Green
    'warning': '#F1C40F'       # Yellow
}
LIGHT_COLORS = COLORS.copy()  # Store the original light colors

DARK_COLORS = {
    'primary': '#ECF0F1',      # Light grey
    'secondary': '#3498DB',    # Bright blue
    'accent': '#E74C3C',       # Red
    'background': '#2C3E50',   # Dark blue-grey
    'text': '#ECF0F1',         # Light grey
    'button': '#34495E',       # Darker blue-grey
    'button_hover': '#2980B9', # Blue
    'success': '#27AE60',      # Green
    'warning': '#F1C40F'       # Yellow
}

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
class StyledButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=COLORS['button'],
            fg='white',
            font=('Helvetica', 12, 'bold'),
            pady=10,
            bd=0,
            cursor='hand2',
            activebackground=COLORS['button_hover'],
            activeforeground='white'
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = COLORS['button_hover']

    def on_leave(self, e):
        self['background'] = COLORS['button']


def create_gear_icon(size=32, color='white'):
    # Create a new image with transparency
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw outer circle
    draw.ellipse([4, 4, size - 4, size - 4], outline=color, width=2)

    # Draw gear teeth (simplified)
    for i in range(8):
        angle = i * 45
        x = size / 2 + (size / 2 - 2) * math.cos(math.radians(angle))
        y = size / 2 + (size / 2 - 2) * math.sin(math.radians(angle))
        draw.rectangle([x - 3, y - 3, x + 3, y + 3], fill=color)

    return ImageTk.PhotoImage(image)

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x800")
        self.root.configure(bg=COLORS['background'])

        # Main container with padding
        self.menu_frame = tk.Frame(root, bg=COLORS['background'])
        self.menu_frame.pack(expand=True, fill='both')

        # Create top frame for gear icon
        self.gear_frame = tk.Frame(self.menu_frame, bg=COLORS['background'])
        self.gear_frame.pack(fill='x', pady=(10, 0))  # Add to top with padding

        # Create gear icon button in top-right corner
        self.gear_icon = create_gear_icon()
        gear_button = tk.Button(self.gear_frame,
                              image=self.gear_icon,
                              bg=COLORS['background'],
                              activebackground=COLORS['background'],
                              bd=0,
                              cursor='hand2',
                              command=self.show_settings)
        gear_button.pack(side='right', padx=20)  # Position on right side

        # Title section
        title_frame = tk.Frame(self.menu_frame, bg=COLORS['background'])
        title_frame.pack(pady=(20, 40))  # Adjusted padding

        tk.Label(title_frame,
                text="HANGMAN",
                font=("Helvetica", 52, "bold"),
                fg=COLORS['primary'],
                bg=COLORS['background']).pack()

        tk.Label(title_frame,
                text="GAME",
                font=("Helvetica", 24),
                fg=COLORS['secondary'],
                bg=COLORS['background']).pack()

        # Buttons container
        buttons_frame = tk.Frame(self.menu_frame, bg=COLORS['background'])
        buttons_frame.pack(pady=20)

        # Menu buttons with consistent styling
        StyledButton(buttons_frame,
                    text="Single Player",
                    command=self.show_categories,
                    width=20).pack(pady=10)

        StyledButton(buttons_frame,
                    text="Player vs Player",
                    command=self.start_pvp,
                    width=20).pack(pady=10)

        StyledButton(buttons_frame,
                    text="Game History",
                    command=self.show_history,
                    width=20).pack(pady=10)

        StyledButton(buttons_frame,
                    text="Exit",
                    command=root.quit,
                    width=20).pack(pady=10)


    # history
    def show_history(self):
        self.menu_frame.pack_forget()
        GameHistoryWindow(self.root)
    # Add this method to MainMenu class
    def start_pvp(self):
        self.menu_frame.pack_forget()
        PvPHangmanGame(self.root)

    def show_categories(self):
        self.menu_frame.pack_forget()

        self.category_frame = tk.Frame(self.root, bg=COLORS['background'], padx=40, pady=40)
        self.category_frame.pack(expand=True, fill='both')

        # Title
        tk.Label(self.category_frame,
                 text="Select Category",
                 font=("Helvetica", 36, "bold"),
                 fg=COLORS['primary'],
                 bg=COLORS['background']).pack(pady=(0, 30))

        # Category buttons container
        categories_frame = tk.Frame(self.category_frame, bg=COLORS['background'])
        categories_frame.pack()

        # Create styled category buttons
        for category in WORD_CATEGORIES.keys():
            StyledButton(categories_frame,
                         text=category,
                         command=lambda c=category: self.start_game(c),
                         width=25).pack(pady=8)

        # Back button
        StyledButton(self.category_frame,
                     text="Back to Main Menu",
                     command=self.back_to_menu,
                     width=20).pack(pady=(30, 0))

    def show_settings(self):
        self.menu_frame.pack_forget()
        SettingsWindow(self.root, self)

    def back_to_menu(self):
        self.category_frame.pack_forget()
        self.menu_frame.pack(expand=True, fill='both')

    def start_game(self, category):
        self.category_frame.pack_forget()
        HangmanGame(self.root, category)

class GameHistoryWindow:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg=COLORS['background'], padx=40, pady=40)
        self.frame.pack(expand=True, fill='both')

        # Title with decorative line
        tk.Label(self.frame,
                 text="Game History",
                 font=("Helvetica", 36, "bold"),
                 fg=COLORS['primary'],
                 bg=COLORS['background']).pack(pady=(0, 30))

        # Create tabbed interface
        self.create_notebook()

        # Back button
        StyledButton(self.frame,
                     text="Back to Main Menu",
                     command=self.return_to_menu,
                     width=20).pack(pady=20)

    def create_notebook(self):
        style = ttk.Style()
        style.configure("Custom.TNotebook", background=COLORS['background'])
        style.configure("Custom.TNotebook.Tab", padding=[12, 8], font=('Helvetica', 10))

        notebook = ttk.Notebook(self.frame, style="Custom.TNotebook")
        notebook.pack(fill='both', expand=True, pady=20)

        # Create and add tabs
        stats_frame = self.create_stats_tab(notebook)
        achievements_frame = self.create_achievements_tab(notebook)
        history_frame = self.create_history_tab(notebook)

        notebook.add(stats_frame, text='Statistics')
        notebook.add(achievements_frame, text='Achievements')
        notebook.add(history_frame, text='Recent Games')

    def create_stats_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['background'], padx=20, pady=20)
        stats = GameStats().stats

        # Create styled stats display
        stats_text = f"""
        Total Games Played: {stats['total_games']}
        Total Wins: {stats['total_wins']}
        Current Streak: {stats['current_streak']}
        Best Streak: {stats['best_streak']}
        Win Rate: {(stats['total_wins'] / stats['total_games'] * 100 if stats['total_games'] > 0 else 0):.1f}%
        """

        tk.Label(frame,
                 text=stats_text,
                 font=("Helvetica", 14),
                 justify='left',
                 bg=COLORS['background'],
                 fg=COLORS['text']).pack(pady=20)

        return frame

    def create_history_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['background'], padx=20, pady=20)
        stats = GameStats().stats

        # Create scrollable frame for game history
        canvas = tk.Canvas(frame, bg=COLORS['background'])
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add recent games to scrollable frame
        for game in stats['game_history'][:20]:  # Show last 20 games
            game_frame = tk.Frame(scrollable_frame, bg=COLORS['background'])
            game_frame.pack(fill='x', pady=5)

            game_text = f"{game['date']}\n{game['category']}: {game['word']}\n"
            game_text += f"Result: {game['result']} ({game['guesses_left']} guesses left)"

            tk.Label(game_frame,
                     text=game_text,
                     font=("Helvetica", 10),
                     bg=COLORS['background'],
                     fg=COLORS['text'],
                     justify='left').pack(anchor='w')

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        return frame

    def create_achievements_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['background'], padx=20, pady=20)
        stats = GameStats().stats

        for achievement_id in ACHIEVEMENTS:
            achievement = ACHIEVEMENTS[achievement_id]
            is_unlocked = achievement_id in stats['achievements']

            achievement_frame = tk.Frame(frame, bg=COLORS['background'])
            achievement_frame.pack(fill='x', pady=5)

            # Achievement icon and name
            tk.Label(achievement_frame,
                     text=f"{achievement['icon']} {achievement['name']}",
                     font=("Helvetica", 12, "bold"),
                     fg=COLORS['primary'] if is_unlocked else 'gray',
                     bg=COLORS['background']).pack(anchor='w')

            # Achievement description
            tk.Label(achievement_frame,
                     text=achievement['description'],
                     font=("Helvetica", 10),
                     fg=COLORS['text'] if is_unlocked else 'gray',
                     bg=COLORS['background']).pack(anchor='w')

        return frame

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
        self.stats["game_history"].insert(0, game_record)
        self.stats["total_games"] += 1

        if is_win:
            self.stats["total_wins"] += 1
            self.stats["current_streak"] += 1
            self.stats["best_streak"] = max(self.stats["best_streak"],
                                            self.stats["current_streak"])

            if category not in self.stats["category_wins"]:
                self.stats["category_wins"][category] = 0
            self.stats["category_wins"][category] += 1

            self.check_achievements(guesses_left, category)
        else:
            self.stats["current_streak"] = 0

        self.stats["game_history"] = self.stats["game_history"][:50]
        self.save_stats()

    def check_achievements(self, guesses_left, category):
        achievements = self.stats["achievements"]

        # First win achievement
        if self.stats["total_wins"] == 1 and "first_win" not in achievements:
            achievements.append("first_win")
            self.show_achievement_popup("First Victory! 🏆")

        # Perfect game achievement
        if guesses_left == 6 and "perfect_game" not in achievements:
            achievements.append("perfect_game")
            self.show_achievement_popup("Perfect Game! ⭐")

        # Winning streak achievement
        if self.stats["current_streak"] >= 5 and "winning_streak_5" not in achievements:
            achievements.append("winning_streak_5")
            self.show_achievement_popup("5-Win Streak! 🔥")

        # Category master achievement
        if (len(self.stats["category_wins"]) == len(WORD_CATEGORIES)
                and "category_master" not in achievements):
            achievements.append("category_master")
            self.show_achievement_popup("Category Master! 👑")

        # Quick solver achievement
        if guesses_left >= 4 and "quick_solver" not in achievements:
            achievements.append("quick_solver")
            self.show_achievement_popup("Quick Solver! ⚡")

    def show_achievement_popup(self, message):
        popup = tk.Toplevel()
        popup.title("Achievement Unlocked!")
        popup.configure(bg=COLORS['background'])

        # Center the popup
        window_width = 300
        window_height = 150
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Achievement message
        tk.Label(popup,
                 text="Achievement Unlocked!",
                 font=("Helvetica", 16, "bold"),
                 fg=COLORS['primary'],
                 bg=COLORS['background']).pack(pady=(20, 10))

        tk.Label(popup,
                 text=message,
                 font=("Helvetica", 14),
                 fg=COLORS['secondary'],
                 bg=COLORS['background']).pack(pady=10)

        # Close button
        StyledButton(popup,
                     text="OK",
                     command=popup.destroy,
                     width=10).pack(pady=10)

        # Auto-close after 3 seconds
        popup.after(3000, popup.destroy)

class PvPHangmanGame:
    def __init__(self, root):
        self.root = root
        self.setup_word_input()

    def setup_word_input(self):
        self.input_frame = tk.Frame(self.root, bg=COLORS['background'], padx=40, pady=40)
        self.input_frame.pack(expand=True, fill='both')

        # Title
        tk.Label(self.input_frame,
                text="Player vs Player Mode",
                font=("Helvetica", 36, "bold"),
                fg=COLORS['primary'],
                bg=COLORS['background']).pack(pady=(0, 20))

        # Instructions
        tk.Label(self.input_frame,
                text="Player 1: Enter a word for Player 2 to guess",
                font=("Helvetica", 16),
                fg=COLORS['text'],
                bg=COLORS['background']).pack(pady=(0, 20))

        # Word entry with styled frame
        entry_frame = tk.Frame(self.input_frame, bg=COLORS['background'])
        entry_frame.pack(pady=20)

        self.word_var = tk.StringVar()
        self.word_entry = tk.Entry(entry_frame,
                                 textvariable=self.word_var,
                                 font=("Helvetica", 14),
                                 show="*",
                                 width=30)
        self.word_entry.pack()

        # Buttons
        StyledButton(self.input_frame,
                    text="Start Game",
                    command=self.start_game,
                    width=20).pack(pady=10)

        StyledButton(self.input_frame,
                    text="Back to Main Menu",
                    command=self.return_to_menu,
                    width=20).pack(pady=10)

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
        self.game_frame = tk.Frame(root, bg=COLORS['background'])
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
        self.word_label = tk.Label(self.game_frame,
                                   text=" ".join(self.correct_guesses),
                                   font=("Helvetica", 24),
                                   bg=COLORS['background'])
        self.word_label.pack(pady=20)

        # Display for remaining guesses
        self.guess_label = tk.Label(self.game_frame,
                                    text=f"Guesses left: {self.guesses}",
                                    font=("Helvetica", 14),
                                    bg=COLORS['background'])
        self.guess_label.pack(pady=10)

        # Canvas for hangman drawing
        self.canvas = tk.Canvas(self.game_frame, width=200, height=250, bg="white")
        self.canvas.pack(pady=20)
        self.draw_base()

        # Setup keyboard (only once)
        self.setup_keyboard()

        # Back to menu button
        StyledButton(self.game_frame,
                     text="Back to Main Menu",
                     command=self.return_to_menu,
                     width=20).pack(pady=10)

        self.hangman_parts = [self.draw_head, self.draw_body, self.draw_left_arm,
                              self.draw_right_arm, self.draw_left_leg, self.draw_right_leg]

    def setup_keyboard(self):
        settings = Settings().settings
        scale = settings["keyboard_scale"]

        keyboard_frame = tk.Frame(self.game_frame, bg=COLORS['background'])
        keyboard_frame.pack(pady=20)

        qwerty_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.buttons = {}

        button_width = max(2, int(4 / scale))
        button_height = max(1, int(2 / scale))
        font_size = int(14 * scale)

        for row, keys in enumerate(qwerty_layout):
            row_frame = tk.Frame(keyboard_frame, bg=COLORS['background'])
            row_frame.pack(pady=5)

            if row == 1:
                tk.Label(row_frame, width=2, bg=COLORS['background']).pack(side='left')
            elif row == 2:
                tk.Label(row_frame, width=4, bg=COLORS['background']).pack(side='left')

            for key in keys:
                btn = tk.Button(row_frame,
                                text=key,
                                font=("Helvetica", font_size, "bold"),
                                width=button_width,
                                height=button_height,
                                bg=COLORS['button'],
                                fg=COLORS['text'],
                                bd=0,
                                activebackground=COLORS['button_hover'],
                                activeforeground=COLORS['text'],
                                command=lambda l=key: self.guess_letter(l))
                btn.pack(side='left', padx=3)
                self.buttons[key] = btn
    def draw_hangman_improved(self):
            # Enhanced hangman drawing with thicker lines and better proportions
            self.canvas.delete("all")

            # Base
            self.canvas.create_line(50, 230, 150, 230, width=3)
            # Pole
            self.canvas.create_line(100, 230, 100, 50, width=3)
            # Top beam
            self.canvas.create_line(100, 50, 150, 50, width=3)
            # Rope
            self.canvas.create_line(150, 50, 150, 70, width=3)
    def update_game_status(self, message, is_win=False):
            color = COLORS['success'] if is_win else COLORS['warning']
            self.guess_label.configure(text=message, fg=color)
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


class Settings:
    def __init__(self):
        self.settings_file = "hangman_settings.json"
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "dark_mode": False,
                "button_size": "normal",  # normal, large, extra-large
                "keyboard_scale": 1.0  # 1.0 = normal, 1.5 = large, 2.0 = extra-large
            }

        # Apply settings immediately upon loading
        self.apply_settings()

    def apply_settings(self):
        global COLORS
        COLORS = DARK_COLORS if self.settings["dark_mode"] else LIGHT_COLORS

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)
        self.apply_settings()


class SettingsWindow:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.settings = Settings()
        self.setup_window()

    def setup_window(self):
        self.frame = tk.Frame(self.root, bg=COLORS['background'], padx=40, pady=40)
        self.frame.pack(expand=True, fill='both')

        # Title
        tk.Label(self.frame,
                text="Settings",
                font=("Helvetica", 36, "bold"),
                fg=COLORS['primary'],
                bg=COLORS['background']).pack(pady=(0, 30))

        # Settings Container
        settings_frame = tk.Frame(self.frame, bg=COLORS['background'])
        settings_frame.pack(pady=20)

        # Dark Mode Toggle
        dark_mode_frame = tk.Frame(settings_frame, bg=COLORS['background'])
        dark_mode_frame.pack(fill='x', pady=10)

        tk.Label(dark_mode_frame,
                text="Dark Mode",
                font=("Helvetica", 14),
                fg=COLORS['text'],
                bg=COLORS['background']).pack(side='left', padx=10)

        self.dark_mode_var = tk.BooleanVar(value=self.settings.settings["dark_mode"])
        tk.Checkbutton(dark_mode_frame,
                      variable=self.dark_mode_var,
                      command=self.toggle_dark_mode,
                      bg=COLORS['background'],
                      activebackground=COLORS['background'],
                      selectcolor=COLORS['button']).pack(side='left')

        # Button Size Selection
        size_frame = tk.Frame(settings_frame, bg=COLORS['background'])
        size_frame.pack(fill='x', pady=10)

        tk.Label(size_frame,
                text="Button Size:",
                font=("Helvetica", 14),
                fg=COLORS['text'],
                bg=COLORS['background']).pack(side='left', padx=10)

        self.button_size_var = tk.StringVar(value=self.settings.settings["button_size"].title())
        sizes = ["Normal", "Large", "Extra Large"]
        size_menu = ttk.OptionMenu(size_frame,
                                 self.button_size_var,
                                 self.button_size_var.get(),
                                 *sizes,
                                 command=self.change_button_size)
        size_menu.pack(side='left')

        # Preview Section
        preview_frame = tk.Frame(self.frame, bg=COLORS['background'])
        preview_frame.pack(pady=20)

        tk.Label(preview_frame,
                text="Preview:",
                font=("Helvetica", 14),
                fg=COLORS['text'],
                bg=COLORS['background']).pack(pady=10)

        self.preview_button = StyledButton(preview_frame,
                                         text="Sample Button",
                                         command=lambda: None,
                                         width=15)
        self.preview_button.pack()

        # Save and Return Button
        StyledButton(self.frame,
                    text="Save and Return",
                    command=self.save_and_return,
                    width=20).pack(pady=30)

    def toggle_dark_mode(self):
        global COLORS
        self.settings.settings["dark_mode"] = self.dark_mode_var.get()
        COLORS = DARK_COLORS if self.dark_mode_var.get() else LIGHT_COLORS

        # Update all visible elements with new colors
        self.frame.configure(bg=COLORS['background'])
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=COLORS['background'], fg=COLORS['text'])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=COLORS['background'])

        self.update_preview()

    def change_button_size(self, *args):
        size = self.button_size_var.get().lower()
        scale = 1.0
        if size == "large":
            scale = 1.5
        elif size == "extra large":
            scale = 2.0

        self.settings.settings["button_size"] = size
        self.settings.settings["keyboard_scale"] = scale
        self.update_preview()

    def update_preview(self):
        scale = self.settings.settings["keyboard_scale"]
        font_size = int(12 * scale)
        button_width = int(15 / scale)

        self.preview_button.configure(
            font=('Helvetica', font_size, 'bold'),
            width=button_width,
            bg=COLORS['button'],
            fg='white'
        )

    def save_and_return(self):
        self.settings.save_settings()
        self.frame.destroy()
        self.main_menu.__init__(self.root)  # Refresh main menu with new settings


# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()