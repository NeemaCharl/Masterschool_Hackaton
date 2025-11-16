import wikipedia
import json
import os
import random
from openai import OpenAI

# Initialize OpenAI client safely with environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# API_KEY = "your_api_key_here"
client = OpenAI(api_key=API_KEY)


# Import your list of articles as a set
from list_of_articles import hist_events_and_persons as hist_list

SCOREBOARD_FILE = "scoreboard.json"

# ---------------- Utility colored print ----------------
def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

# ---------------- Scoreboard Functions ----------------
def load_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r") as f:
            return json.load(f)
    return {}


def save_scoreboard(scoreboard):
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scoreboard, f, indent=4)


def update_scoreboard(player_id):
    scoreboard = load_scoreboard()
    for player, score in player_id.items():
        scoreboard[player] = scoreboard.get(player, 0) + score
    sorted_scoreboard = dict(sorted(scoreboard.items(), key=lambda x: x[1], reverse=True))
    save_scoreboard(sorted_scoreboard)
    return sorted_scoreboard


def display_scoreboard(scoreboard):
    print(colored("\n====== LEADERBOARD ======", "33"))
    for idx, (player, score) in enumerate(scoreboard.items(), start=1):
        print(colored(f"{idx}. {player}: {score} points", "36"))
    print(colored("=" * 25, "33"))


# ---------------- AI Hint Generator ----------------
def generate_hints(redacted_summary):
    try:
        completion = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"In ChronoGuesser, the player has to guess a Wikipedia article. "
                        f"They already received this summary with hidden words: {redacted_summary} "
                        f"Now generate exactly 2 very short hints (each on a new line). "
                        f"The hints must give new helpful info, but must NOT reveal "
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
    try:
        return wikipedia.summary(article_name, sentences=2, auto_suggest=False)
    except Exception:
        return "Summary not found."


# ---------------- Main Game Functions ----------------
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
    player_id = {}
    player_name = input(colored("Enter your name (will appear on leaderboard): ", "32"))
    player_id[player_name] = 0
    return player_id


def get_random_item(item_set):
    return random.choice(list(item_set))


def get_variants(article_name):
    variants = set(wikipedia.search(article_name))
    variants.add(article_name)
    return variants

def get_blanc_article(article_name, summary):
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
    guess_counter = 0
    hint_counter = 0
    correct_answer = False

    while guess_counter < 3:
        player_answer = input(colored("Your guess (or 'hint'): ", "36"))

        if player_answer.lower() == "hint":
            if hint_counter < 2:
                hint_counter += 1
                hints = generate_hints(blanc_summary)
                print(colored(f"\n💡 Hint {hint_counter}:\n{hints}\n", "33"))
                continue
            else:
                print(colored("❌ No hints left.", "31"))

        elif player_answer.lower() == article_name.lower():
            print(colored("✅ Correct! Well done.", "32"))
            correct_answer = True
            return correct_answer, guess_counter, hint_counter

        else:
            print(colored("❌ Wrong. Try again.", "31"))
            guess_counter += 1

    print(colored(f"\n⏳ Out of tries! The answer was: {article_name}", "33"))
    return correct_answer, guess_counter, hint_counter

def calculate_score(correct_answer, guess_counter, hint_counter):
    if not correct_answer:
        return 0
    return 1000 - (guess_counter * 200) - (hint_counter * 100)

def update_player_score(player_id, round_score):
    key = next(iter(player_id))
    player_id[key] += round_score
    return player_id

# ---------------- Main Loop ----------------
def main():
    show_menu()

    current_scoreboard = load_scoreboard()
    if current_scoreboard:
        display_scoreboard(current_scoreboard)

    player_id = get_player_id()

    for i in range(3):
        article_name = get_random_item(hist_list)
        summary = get_summary(article_name)
        blanc_summary = get_blanc_article(article_name, summary)

        print(colored(f"\n🔎 Round {i+1}", "34"))
        print(colored("Redacted summary:\n", "31"))
        print(blanc_summary, "\n")

        correct, guesses, hints = get_answer_and_hint_request(article_name, blanc_summary)
        score = calculate_score(correct, guesses, hints)
        player_id = update_player_score(player_id, score)

    print(colored("\n🎮 Game Over! Your final score:", "35"))
    print(player_id)

    scoreboard = update_scoreboard(player_id)
    display_scoreboard(scoreboard)

if __name__ == "__main__":
    main()
