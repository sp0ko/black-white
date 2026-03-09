import random
import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

# File for saving statistics
STATS_FILE = 'stats.json'

# Function to load statistics
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {"max_streak": 0, "max_miss_streak": 0, "color_history": []}

# Function to save statistics
def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

class BlackAndWhiteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Black & White Game")
        self.root.geometry("600x500")
        self.root.config(bg='#f0f0f0')
        
        # Load stats
        self.stats = load_stats()
        self.max_streak = self.stats.get("max_streak", 0)
        self.max_miss_streak = self.stats.get("max_miss_streak", 0)
        
        # Game state
        self.points = 0
        self.current_streak = 0
        self.current_miss_streak = 0
        self.session_colors = []
        self.game_active = False
        self.current_color = None
        
        # Create GUI
        self.create_main_menu()
    
    def create_main_menu(self):
        """Create main menu"""
        self.clear_window()
        
        # Title
        title_font = tkfont.Font(family="Arial", size=20, weight="bold")
        title = tk.Label(self.root, text="Hello, WorldxD", font=title_font, bg='#f0f0f0')
        title.pack(pady=20)
        
        # Menu frame
        menu_frame = tk.Frame(self.root, bg='#f0f0f0')
        menu_frame.pack(pady=30)
        
        button_font = tkfont.Font(family="Arial", size=14)
        
        btn_start = tk.Button(menu_frame, text="1. Start Game", command=self.start_game, 
                               width=20, font=button_font, bg='#4CAF50', fg='white')
        btn_start.pack(pady=10)
        
        btn_results = tk.Button(menu_frame, text="2. Best and Worst Results", 
                                 command=self.show_results, width=20, font=button_font, 
                                 bg='#2196F3', fg='white')
        btn_results.pack(pady=10)
        
        btn_quit = tk.Button(menu_frame, text="3. Quit Game", command=self.root.quit, 
                              width=20, font=button_font, bg='#f44336', fg='white')
        btn_quit.pack(pady=10)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def start_game(self):
        """Start the game"""
        self.game_active = True
        self.points = 0
        self.current_streak = 0
        self.current_miss_streak = 0
        self.session_colors = []
        # Session-specific max streaks
        self.session_max_streak = 0
        self.session_max_miss_streak = 0
        self.show_game_screen()
    
    def show_game_screen(self):
        """Display game screen"""
        self.clear_window()
        
        # Title
        title_font = tkfont.Font(family="Arial", size=16, weight="bold")
        title = tk.Label(self.root, text="Black & White Game", font=title_font, bg='#f0f0f0')
        title.pack(pady=10)
        
        # Generate new color
        self.current_color = random.choice(['black', 'white'])
        self.session_colors.append(self.current_color)
        
        # Color display box - neutral initially
        bg_color = '#cccccc'  # Neutral gray
        fg_color = 'black'
        self.color_display_frame = tk.Frame(self.root, bg=bg_color, width=200, height=100)
        self.color_display_frame.pack(pady=20)
        self.color_display_frame.pack_propagate(False)  # Prevent shrinking
        
        color_label = tk.Label(self.color_display_frame, text="Guess the color!", 
                               font=("Arial", 14), bg=bg_color, fg=fg_color)
        color_label.pack(expand=True)
        
        # Game info
        info_font = tkfont.Font(family="Arial", size=10)
        info_frame = tk.Frame(self.root, bg='#f0f0f0')
        info_frame.pack(pady=10)
        
        # Current session info
        session_text = f"Current Session: Points: {self.points} | Streak: {self.current_streak} | Miss Streak: {self.current_miss_streak}"
        self.session_label = tk.Label(info_frame, text=session_text, font=info_font, bg='#f0f0f0', fg='#333333')
        self.session_label.pack()
        
        # Session best records
        session_best_text = f"Session Best: Highest Streak: {self.session_max_streak} | Highest Miss Streak: {self.session_max_miss_streak}"
        self.session_best_label = tk.Label(info_frame, text=session_best_text, font=info_font, bg='#f0f0f0', fg='#0066cc')
        self.session_best_label.pack()
        
        # All-time results
        alltime_text = f"All-Time Best: Streak: {self.max_streak} | Worst Streak: {self.max_miss_streak}"
        self.info_label = tk.Label(info_frame, text=alltime_text, font=info_font, bg='#f0f0f0', fg='#666666')
        self.info_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(pady=30)
        
        button_font = tkfont.Font(family="Arial", size=14, weight="bold")
        
        self.btn_black = tk.Button(buttons_frame, text="BLACK", command=lambda: self.make_guess('black'),
                               width=12, font=button_font, bg='#000000', fg='white')
        self.btn_black.pack(side=tk.LEFT, padx=20)
        
        self.btn_white = tk.Button(buttons_frame, text="WHITE", command=lambda: self.make_guess('white'),
                               width=12, font=button_font, bg='#ffffff', fg='black', 
                               relief=tk.RAISED, bd=2)
        self.btn_white.pack(side=tk.LEFT, padx=20)
        
        # Result label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg='#f0f0f0')
        self.result_label.pack(pady=10)
        
        # Back button
        btn_back = tk.Button(self.root, text="Back to Menu", command=self.end_game,
                              font=("Arial", 10), bg='#FF9800', fg='white')
        btn_back.pack(pady=10)
    
    def save_current_stats(self):
        """Save statistics to file immediately"""
        self.stats["max_streak"] = self.max_streak
        self.stats["max_miss_streak"] = self.max_miss_streak
        if "color_history" not in self.stats:
            self.stats["color_history"] = []
        save_stats(self.stats)
    
    def next_round(self):
        """Prepare next round without reloading the screen"""
        # Generate new color
        self.current_color = random.choice(['black', 'white'])
        self.session_colors.append(self.current_color)
        
        # Update color display to neutral
        bg_color = '#cccccc'  # Neutral gray
        fg_color = 'black'
        self.color_display_frame.config(bg=bg_color)
        # Update label inside frame
        for child in self.color_display_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=bg_color, fg=fg_color)
        
        # Clear result label
        self.result_label.config(text="")
        
        # Enable buttons
        self.btn_black.config(state='normal')
        self.btn_white.config(state='normal')
    
    def make_guess(self, guess):
        """Process player's guess"""
        # Disable buttons to prevent multiple clicks
        self.btn_black.config(state='disabled')
        self.btn_white.config(state='disabled')
        
        if guess == self.current_color:
            self.result_label.config(text="✓ Correct! Wow, 6th sense!", fg='#4CAF50')
            self.points += 1
            self.current_streak += 1
            self.current_miss_streak = 0
            # Update session and all-time records
            if self.current_streak > self.session_max_streak:
                self.session_max_streak = self.current_streak
            if self.current_streak > self.max_streak:
                self.max_streak = self.current_streak
                self.save_current_stats()  # Save immediately when new all-time record
        else:
            self.result_label.config(text="✗ Wrong! Try harder!", fg='#f44336')
            self.current_miss_streak += 1
            self.current_streak = 0
            # Update session and all-time records
            if self.current_miss_streak > self.session_max_miss_streak:
                self.session_max_miss_streak = self.current_miss_streak
            if self.current_miss_streak > self.max_miss_streak:
                self.max_miss_streak = self.current_miss_streak
                self.save_current_stats()  # Save immediately when new all-time record
        
        # Update current session label
        session_text = f"Current Session: Points: {self.points} | Streak: {self.current_streak} | Miss Streak: {self.current_miss_streak}"
        self.session_label.config(text=session_text)
        
        # Update session best label
        session_best_text = f"Session Best: Highest Streak: {self.session_max_streak} | Highest Miss Streak: {self.session_max_miss_streak}"
        self.session_best_label.config(text=session_best_text)
        
        # Update all-time label
        alltime_text = f"All-Time Best: Streak: {self.max_streak} | Worst Streak: {self.max_miss_streak}"
        self.info_label.config(text=alltime_text)
        
        # Show what computer chose
        result_text = f"Computer chose: {self.current_color.upper()}"
        self.result_label.config(text=result_text + "\n" + self.result_label.cget("text"), fg='#333333')
        
        # Reveal the color in the frame
        bg_color = 'black' if self.current_color == 'black' else 'white'
        fg_color = 'white' if self.current_color == 'black' else 'black'
        self.color_display_frame.config(bg=bg_color)
        for child in self.color_display_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=bg_color, fg=fg_color)
        
        # Schedule next round
        self.root.after(2000, self.next_round)
    
    def show_results(self):
        """Show statistics"""
        self.clear_window()
        
        title_font = tkfont.Font(family="Arial", size=18, weight="bold")
        title = tk.Label(self.root, text="Best and Worst Results", font=title_font, bg='#f0f0f0')
        title.pack(pady=20)
        
        stats_font = tkfont.Font(family="Arial", size=14)
        stats_frame = tk.Frame(self.root, bg='#ffffff', relief=tk.RAISED, bd=2)
        stats_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Stats content
        stats_text = f"""
All-Time Results:

Best Streak (Hits): {self.max_streak}
Worst Streak (Misses): {self.max_miss_streak}

Total Colors Generated: {len(self.stats.get('color_history', []))}
        """
        
        stats_label = tk.Label(stats_frame, text=stats_text, font=stats_font, 
                               bg='#ffffff', justify=tk.LEFT)
        stats_label.pack(pady=20, padx=20)
        
        # Back button
        btn_back = tk.Button(self.root, text="Back to Menu", command=self.create_main_menu,
                              font=("Arial", 12), bg='#2196F3', fg='white')
        btn_back.pack(pady=20)
    
    def end_game(self):
        """End the game and save stats"""
        # Save statistics
        self.stats["max_streak"] = self.max_streak
        self.stats["max_miss_streak"] = self.max_miss_streak
        if "color_history" not in self.stats:
            self.stats["color_history"] = []
        self.stats["color_history"].extend(self.session_colors)
        save_stats(self.stats)
        
        # Show session summary
        summary = f"""Session Summary:

Points: {self.points}
Best Streak in Session: {self.max_streak}
Worst Streak in Session: {self.max_miss_streak}

These are all-time records!"""
        
        messagebox.showinfo("Game Over", summary)
        self.create_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackAndWhiteGame(root)
    root.mainloop()
