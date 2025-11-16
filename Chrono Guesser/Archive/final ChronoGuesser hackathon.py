import wikipedia
import json
import os
import random
from openai import OpenAI

# Import your list of articles
from list_of_articles import hist_events_and_persons as hist_list




# ------------------------------------------
# ChronoGuesser Game
# ------------------------------------------
SCOREBOARD_FILE = "scoreboard.json"

# ---------------- Scoreboard ----------------
def load_scoreboard():
    """Load the scoreboard from JSON file, or return empty dict if not exists."""
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_scoreboard(scoreboard):
    """Save scoreboard dictionary to JSON file."""
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scoreboard, f, indent=4)

def update_scoreboard(player_id):
    """Update the JSON scoreboard with the player's cumulative score."""
    scoreboard = load_scoreboard()
    for player, score in player_id.items():
        if player in scoreboard:
            scoreboard[player] += score
        else:
            scoreboard[player] = score

    # Sort by descending score
    sorted_scoreboard = dict(
        sorted(scoreboard.items(), key=lambda x: x[1], reverse=True)
    )
    save_scoreboard(sorted_scoreboard)
    return sorted_scoreboard

def display_scoreboard(scoreboard):
    """Print scoreboard in descending order."""
    print("\n\033[1;33m==== LEADERBOARD ====\033[0m")
    for idx, (player, score) in enumerate(scoreboard.items(), start=1):
        print(f"{idx}. {player}: {score} points")
    print("=" * 25)

# ---------------- AI Hint Generator ----------------
def generate_hints(redacted_summary):
    """Generate 2 small hints about the article using OpenAI."""
    try:
        completion = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"In ChronoGuesser, the player has to guess a Wikipedia article. "
                        f"They already received this summary with hidden words: {redacted_summary} "
                        f"Now generate exactly 2 very short hints (each on its own line). "
                        f"The hints must give new helpful info, but must NOT reveal "
                        f"or paraphrase the article title too directly."
                    )
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"(⚠️ Hint generation failed: {str(e)})"

# ---------------- Game Functions ----------------
def show_menu():
    print("\033[1;34m" + "-" * 100 + "\033[0m")
    print("\033[1;36m" + r"""
                -####+.
            ###############
         ####             ###+            #######   ##
       .##        ##.       +##         ###    +##- ##  -         #    -.         -        -
      ###         -#          ###      +##          ######## ###### ########  ########  #######
     ###    -     -#           ##-     ###          ##    ##  ##   -#-    ##  ##    ## ##     ##
     ##    .###    #    ##      ##      ###     ##+ ##    ##  ##   ##+    ##  ##   -## ##     ##
    ##.       #### # ####        #       #########  ##   -## +##    ########  ##   ###  #######
    ##           #####       ### #-          .      -     -   -        #+     -.    ..    -#-
    -##                         ##       ########.
     ##                        ##-      ###     ##- ##    ##    ###+    ####-    ####     ###+   ## +#-
      ##                      ###      +##          ##    ##  ##   ##  ##   ##.##   ### ##   ##- #####.
       ###                  ###        +##   ###### ##    ## +######## #####   +####    ######## ##
        .###             ####-          ###     +#. ##    ## -#             ##.     ### #-       ##
           ######.   ######              +######### -#######  +######  ####### #######  +######. ##.
               #########                                                      
        """ + "\033[0m")
    print("\033[1;33m----------------------------------- Welcome to ChronoGuesser! -----------------------------------\033[0m")
    print("\033[1;34m" + "-" * 100 + "\033[0m")
    print("                    Test your knowledge of historical events and famous figures.\n")
    print()
    print()
    print()
    print("\033[1;36mDescription:\033[0m")
    print("""
ChronoGuesser is a single-player game where you test your knowledge of history 
by guessing Wikipedia articles about events and figures. Across 3 rounds, 
you get a summary with missing words as clues. You can guess or ask for up to 2 hints, 
but each mistake or hint reduces your score.
""")
    print("\033[1;33mRules:\033[0m")
    print("""
1. Play 3 rounds.
2. Guess the Wikipedia article title from the redacted summary.
3. Up to 3 guesses per round.
4. Ask for up to 2 AI hints with 'hint'.
5. Scoring: 
   - First try correct = 1000 pts
   - Each wrong guess = -200 pts
   - Each hint = -100 pts
   - Fail = 0 pts
6. Scores are saved in a leaderboard.
""")
    print("\033[1;34m" + "-" * 80 + "\033[0m")
    input("\033[1;32mPress Enter to start the game...\033[0m")

def get_player_id():
    """Create a dictionary mapping player name to score."""
    player_id = {}
    player_name = input("Enter your name (will appear on leaderboard): ")
    player_id[player_name] = 0
    return player_id

def get_random_item(item_set):
    """Returns a random article from the set."""
    return random.choice(list(item_set))

def get_variants(article_name):
    """Return a set of variant names based on the article name."""
    variants = set(wikipedia.search(article_name))
    variants.add(article_name)
    return variants

def get_summary(article_name):
    """Return 2 sentences summary of article."""
    return wikipedia.summary(article_name, sentences=2, auto_suggest=False)

def get_blanc_article(article_name, summary):
    """Blank out article name and variants in summary."""
    for name in article_name.split():
        if name.lower() in {"of", "the"}:
            continue
        summary = summary.replace(name, "???")
    for variant in get_variants(article_name):
        for word in variant.split():
            if word.lower() in {"of", "the"}:
                continue
            summary = summary.replace(word, "???")
    return summary

def get_answer_and_hint_request(article_name, blanc_summary):
    """Handle guesses and use GPT hints for 'hint'."""
    guess_counter = 0
    hint_counter = 0
    correct_answer = False

    while guess_counter < 3:
        player_answer = input("Your guess (or 'hint'): ")
        guess_counter += 1
        if player_answer.lower() == "hint":
            if hint_counter < 2:
                hint_counter += 1

                hints = generate_hints(blanc_summary)
                print(f"\n💡 Hint {hint_counter}:\n{hints}\n")
                print()
                print()
                continue
            else:
                print(f"❌ No hints left.")

        elif player_answer.lower() == article_name.lower():
            print("✅ Correct! Well done.")
            correct_answer = True
            return correct_answer, guess_counter, hint_counter

        else:
            print("❌ Wrong. Try again.")
            guess_counter += 1

    print(f"\n⏳ Out of tries! The answer was: {article_name}")
    return correct_answer, guess_counter, hint_counter

def calculate_score(correct_answer, guess_counter, hint_counter):
    """Calculate score for the round."""
    if not correct_answer:
        return 0
    return 1000 - (guess_counter * 200) - (hint_counter * 100)

def update_player_score(player_id, round_score):
    """Update player score."""
    key = next(iter(player_id))
    player_id[key] += round_score
    return player_id

# ---------------- Main Loop ----------------
def main():
    show_menu()

    # Show existing scores first
    current_scoreboard = load_scoreboard()
    if current_scoreboard:
        display_scoreboard(current_scoreboard)

    # Player setup
    player_id = get_player_id()

    # 3 Rounds
    for i in range(3):
        article_name = get_random_item(hist_list)
        summary = get_summary(article_name)
        blanc_summary = get_blanc_article(article_name, summary)

        print(f"\n🔎 Round {i+1}")
        print("Redacted summary:\n")
        print(blanc_summary, "\n")

        correct, guesses, hints = get_answer_and_hint_request(article_name, blanc_summary)
        score = calculate_score(correct, guesses, hints)
        player_id = update_player_score(player_id, score)

    print("\n🎮 Game Over! Your final score:")
    print(player_id)

    # Save and show leaderboard
    scoreboard = update_scoreboard(player_id)
    display_scoreboard(scoreboard)

if __name__ == "__main__":
    main()
