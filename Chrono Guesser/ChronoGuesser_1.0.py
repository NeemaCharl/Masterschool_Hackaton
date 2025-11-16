import wikipedia
import json
import os
from openai import OpenAI

# Import your list of articles as a set
from list_of_articles import hist_events_and_persons as hist_list


# Initialize OpenAI client API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Initialize Scoreboard file
SCOREBOARD_FILE = "scoreboard.json"

# ---------------- Utility colored print ----------------
def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

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
        scoreboard[player] = scoreboard.get(player, 0) + score

    # Sort by descending score
    sorted_scoreboard = dict(sorted(scoreboard.items(), key=lambda x: x[1], reverse=True))
    save_scoreboard(sorted_scoreboard)
    return sorted_scoreboard


def display_scoreboard(scoreboard):
    """Print scoreboard in descending order."""
    print(colored("\n====== LEADERBOARD ======", "33"))
    for idx, (player, score) in enumerate(scoreboard.items(), start=1):
        print(colored(f"{idx}. {player}: {score} points", "36"))
    print(colored("=" * 25, "33"))


# ---------------- AI Hint Generator ----------------
def generate_hints(redacted_summary):
    """Generate small hints about the article using OpenAI."""
    try:
        completion = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"In ChronoGuesser, the player has to guess a Wikipedia article."
                        f"They already received this summary with hidden words: {redacted_summary}"
                        f"Now generate exactly 1 very short hint."
                        f"The hints must give new helpful info, but must NOT reveal"
                        f"or paraphrase the article title too directly."
                    )
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"(⚠️ Hint generation failed: {str(e)})"


# ---------------- Wikipedia Wrapper ----------------
def get_summary(article_name):
    '''Returns a the first sentence of the article summary'''
    try:
        return wikipedia.summary(article_name, sentences=1, auto_suggest=False)
    except Exception:
        return "Summary not found."


# ---------------- Game Functions ----------------
def show_menu():
    print(colored("-" * 100, "34"))
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
    print(colored("                    ------------------- Welcome to ChronoGuesser! -------------------", "31"))
    print(colored("-" * 100, "34"))
    print(colored("                  Test your knowledge of historical events and famous figures.\n", "35"))
    print()#prints a blank line
    print()#prints another blank line
    print(colored("Description:", "33"))
    print("""
ChronoGuesser is a single-player game where you test your knowledge of history 
by guessing Wikipedia articles about events and figures. Across 3 rounds, 
you get a summary with missing words as clues. You can guess or ask for up to 2 hints, 
but each mistake or hint reduces your score.
""")
    print()#prints blank line
    print(colored("Rules:", "33"))
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
    print(colored("-" * 80, "34"))
    input(colored("Press Enter to start the game...", "32"))

def get_player_id():
    '''Create a dictionary that maps player name and score'''
    player_id = {}
    player_name = input(colored("Enter your name. It will be shown at the leaderboard:", "32"))
    player_id[player_name] = 0
    return player_id


def get_random_item(item_set):
    '''Returns a random item from the set'''
    chosen = item_set.pop()
    return chosen


def get_variants(article_name):
    '''Returns a set of variant names based on the article_name'''
    variants = set(wikipedia.search(article_name))
    variants.add(article_name)
    return variants

def get_blanc_article(article_name, summary):
    '''Blanc's out the article_name and variants and returns the summary'''
    for name in article_name.split():
        if name.lower() in {"of", "the"}:
            continue
        summary = summary.replace(name, "_" * len(name))
    for variant in get_variants(article_name):
        if variant.lower() in {"of", "the"}:
                continue
        summary = summary.replace(variant, "_" * len(variant))
    return summary


def get_answer_and_hint_request(article_name, blanc_summary):
    '''Handles players answers and hint requests, use GPT for hints and returns parameters for Calculation'''
    guess_counter = 0
    hint_counter = 0
    correct_answer = False

    while guess_counter < 3:
        player_answer = input(colored("Make your guess! Do you need a hint? "
                              "Try typing 'hint': ", "36"
                                      )
                              )

        if player_answer.lower() == "hint":
            if hint_counter < 2:
                hint_counter += 1
                hints = generate_hints(blanc_summary)
                print(colored(f"\n💡 Hint {hint_counter}:\n{hints}\n", "33"))
                continue
            else:
                print(colored("❌ No hints left. Try guessing.", "31"))

        elif player_answer.lower() == article_name.lower():
            print(colored("✅ You guessed correctly! Congratulations!", "32"))
            correct_answer = True
            return correct_answer, guess_counter, hint_counter

        else:
            print(colored("❌ Sorry, that was not correct. try again.", "31"))
            guess_counter += 1

    print(colored(f"\n⏳ Out of tries! The articles name is: {article_name}", "33"))
    return correct_answer, guess_counter, hint_counter


def calculate_score(correct_answer, guess_counter, hint_counter):
    '''Calculates and adds the score to player_id'''
    if not correct_answer:
        return 0
    return 1000 - (guess_counter * 200) - (hint_counter * 100)


def update_player_score(player_id, round_score):
    '''Updates the player's final score'''
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

    # Game runs 3 Rounds
    for i in range(3):
        article_name = get_random_item(hist_list)
        summary = get_summary(article_name)
        blanc_summary = get_blanc_article(article_name, summary)

        print(colored(f"\n🔎 Round {i+1}", "34"))
        print(colored("Let's try guessing! Here is your first hint:\n", "31"))
        print(blanc_summary, "\n")

        correct, guesses, hints = get_answer_and_hint_request(article_name, blanc_summary)
        score = calculate_score(correct, guesses, hints)
        player_id = update_player_score(player_id, score)

    print(colored("\n🎮 Game Over! Your final score:", "35"))
    print(player_id)

    # Save and show leaderboard
    scoreboard = update_scoreboard(player_id)
    display_scoreboard(scoreboard)

if __name__ == "__main__":
    main()
