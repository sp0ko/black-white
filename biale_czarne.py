import random
import json
import os

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

# Load statistics
stats = load_stats()
max_streak = stats.get("max_streak", 0)
max_miss_streak = stats.get("max_miss_streak", 0)

print("Hello, WorldxD")

def show_menu():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Start Game")
        print("2. Best and Worst Results")
        print("3. Quit Game")
        choice = input("Choose option (1, 2, or 3): ").strip()
        
        if choice == '1':
            play_game()
        elif choice == '2':
            show_results()
        elif choice == '3':
            print("See you later aligator!")
            break
        else:
            print("Whaaaaaaaaaat?!. Please choose 1, 2, or 3.")

def show_results():
    print("\n=== ALL-TIME RESULTS ===")
    print(f"Best streak (hits): {max_streak}")
    print(f"Worst streak (misses): {max_miss_streak}")
    
    # Load and display color history
    history_stats = load_stats()
    if "color_history" in history_stats and history_stats["color_history"]:
        color_sequence = history_stats["color_history"]
        print(f"\nTotal colors generated: {len(color_sequence)}")
        print(f"Color history (last 50): {' '.join(color_sequence[-50:])}")

def play_game():
    global max_streak, max_miss_streak
    
    points = 0
    current_streak = 0
    current_miss_streak = 0
    session_colors = []  # Track colors in this session

    while True:
        color = random.choice(['black', 'white'])
        session_colors.append(color)
        
        guess = input('Guess the color (black/white) or type "quit" to exit: ').strip().lower()

        if guess == 'quit':
            print("\nGame over!")
            print("Current session results:")
            print(f"Points: {points}")
            print(f"Current streak: {current_streak}")
            print(f"Current miss streak: {current_miss_streak}")
            print(f"Colors in this session: {' '.join(session_colors)}")
            
            print("\nAll-time best:")
            print(f"Max streak: {max_streak}")
            print(f"Max miss streak: {max_miss_streak}")
            
            # Save statistics including color history
            history_stats = load_stats()
            if "color_history" not in history_stats:
                history_stats["color_history"] = []
            history_stats["color_history"].extend(session_colors)
            history_stats["max_streak"] = max_streak
            history_stats["max_miss_streak"] = max_miss_streak
            save_stats(history_stats)
            break

        if guess not in ['black', 'white']:
            print("Invalid color. Choose 'black' or 'white'.")
            continue
        
        if guess == color:
            print('wow you got 6th sense!')
            points += 1
            current_streak += 1
            current_miss_streak = 0
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            print('try harder!')
            current_miss_streak += 1
            current_streak = 0
            if current_miss_streak > max_miss_streak:
                max_miss_streak = current_miss_streak

        print(f"Computer chose: {color}")
        print(f"Current streak: {current_streak}")
        print(f"Current miss streak: {current_miss_streak}")
        print(f"Points: {points}")

show_menu()
