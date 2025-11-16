def show_menu():
    print("\033[1;34m" + "-" * 50 + "\033[0m")
    print("\033[1;36m" + r"""
      ____ _                          ____                   
    / ___| |__   ___  _ __   ___    / ___|___  _ __ ___  _ __  
    | |   | '_ \ / _ \| '_ \ / _ \  | |   / _ \| '_ ` _ \| '_ \ 
    | |___| | | | (_) | | | |  __/  | |__| (_) | | | | | | |_) |
     \____|_| |_|\___/|_| |_|\___|   \____\___/|_| |_| |_| .__/                                                        
    """ + "\033[0m")
    print("\033[1;33m-----------Welcome to ChronoGuesser!-----------\033[0m")  # blue line
    print("\033[1;34m" + "-" * 50 + "\033[0m")
    print("Test your knowledge of historical events and famous figures.")
    print()

    # Game descriptionprint
    print("\033[0;37m" + "Description:" + "\033[0m")
    print("""
      ChronoGuesser is a competitive game where players race to find the shortest route between Wikipedia articles.
      The game supports multiple players and multiple rounds. Scores are updated after each player’s turn,
      and at the end of each round. The player with the highest cumulative score at the end of all rounds is declared the winner.
      """)

    # Separator line in blue
    print("\033[1;33mRules:\033[0m")

    # Game rules in bright yellow
    print("""
     1. The game is single-player or multiplayer.
     2. Each player plays 3 rounds.
     3. In each round, a Wikipedia article is shown with the title blanked and only a few lines displayed.
     4. Players can guess the title or request up to 3 hints per round.
     5. Points are awarded based on attempts and hints used:
        - Correct answer with fewer hints → more points
        - Incorrect or skipped answer → 0 points
     6. After all rounds, the final scoreboard is displayed for players to compare scores.
     """)

    # Separator line in blue
    print("\033[1;34m" + "-" * 60 + "\033[0m")

    # Prompt to start
    input("\033[1;32mPress Enter to start the game...\033[0m")

show_menu()



