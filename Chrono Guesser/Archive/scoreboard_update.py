import json
import os

SCOREBOARD_FILE = "scoreboard.json"

def load_scoreboard():
    """Loads the scoreboard json file"""
    if os.path.isfile(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r") as scoreboard_file:
            return json.load(scoreboard_file)
    return {}

def save_scoreboard(scoreboard):
    """Saves the scoreboard json file"""
    with open(SCOREBOARD_FILE, "w") as scoreboard_file:
        json.dump(scoreboard, scoreboard_file)

def update_scoreboard(scoreboard):
    """Updates the scoreboard json file with players cumulative score"""
    scoreboard = load_scoreboard()

   #Merge cumulative scores
   for player, score in player_id.items():
       if player in scoreboard:
           scoreboard[player] += score
       else:
           scoreboard[player] = score

   # Sort by descending order
   sorted_scoreboard = dict(sorted(scoreboard.items(), key=lambda x: x[1], reverse=True))
   save_scoreboard(sorted_scoreboard)
   return sorted_scoreboard


def display_scoreboard(scoreboard):
    """Print scoreboard in descending order."""
    print("\n\033[1;33m==== LEADERBOARD ====\033[0m")
    for idx, (player, score) in enumerate(scoreboard.items(), start=1):
        print(f"{idx}. {player}: {score} points")
    print("=" * 25)


