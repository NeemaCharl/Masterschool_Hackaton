import wikipedia
from list_of_articles import hist_events_and_persons as hist_list


def show_menu():
    print("\033[1;34m" + "-" * 50 + "\033[0m")
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
    print("\033[1;33m-----------Welcome to ChronoGuesser!-----------\033[0m")  # blue line
    print("\033[1;34m" + "-" * 50 + "\033[0m")
    print("Test your knowledge of historical events and famous figures.")
    print()

    # Game description print
    print("\033[0;37m" + "Description:" + "\033[0m")
    print("""
      ChronoGuesser is a single-player game where players test their knowledge of history by identifying
      Wikipedia articles about famous events and figures. Across three rounds, excerpts with hidden words
      serve as clues. Players have up to three attempts and can request hints, but each mistake or hint lowers
      the possible score. After the final round, the player’s total is saved to the scoreboard to compare with
      others.
      """)

    # Separator line in blue
    print("\033[1;33mRules:\033[0m")

    # Game rules in bright yellow
    print("""
     1. The game is single-player game.
     2. The player plays 3 rounds.
     3. In each round, the player has to guess the name of an article on the Wikipedia Website.
        The only hint s/he is getting is few lines of the articles summary with certain words hidden.
     4. The Players has 3 attempts to guess the title or request up to 2 additional hints per round.
     5. Points are awarded based on the attempts and hints used to guess the title:
        - Correct answer on the first try? → 1000 Points!
        - For each false guess and each hint used the maximum points will be reduced.
        - Incorrect answer and no more guessing attempts left → 0 points
     6. When the player finished the game, the scoreboard is displayed.
        The Players name and final score will be saved to the scoreboard to compare with other players.
     """)

    # Separator line in blue
    print("\033[1;34m" + "-" * 60 + "\033[0m")

    # Prompt to start
    input("\033[1;32mPress Enter to start the game...\033[0m")


def get_player_id():
    '''Create a dictionary that maps player name and score'''
    player_id = {}
    player_name = input("Enter your name. It will be shown at the leaderboard: ")
    player_id[player_name] = 0
    return player_id


def get_random_item(item_set):
    '''Returns a random item from the set'''
    chosen = item_set.pop()
    print(f"Selected: {chosen}")
    return chosen


def get_variants(article_name):
    '''Returns a set of variant names based on the article_name'''
    variants = set(wikipedia.search(article_name))
    variants.add(article_name)
    return variants


def get_summary(article_name):
    '''Returns a few sentence of the article summary'''
    summary = wikipedia.summary(article_name, sentences=2, auto_suggest=False)
    return summary


def get_blanc_article(article_name, summary):
    '''Blanc's out the article_name and variants and returns the summary'''
    splitted_article_name = article_name.split()
    for name in splitted_article_name:
        if name in {"of", "the"}:
            continue
        else:
            summary = summary.replace(name, "???")
    for variant in get_variants(article_name):
        if variant in {"of", "the"}:
            continue
        else:
            summary = summary.replace(variant, "???")
    return summary


def get_answer_and_hint_request(article_name):
    '''Handles players answers and hint requests. Returns parameters for Calculation'''
    guess_counter = 0
    hint_counter = 0
    correct_answer = False
    while guess_counter < 3:
        player_answer = input("Make your guess! Do you need a hint? "
                              "Try typing 'hint': "
                              )
        if player_answer.lower() == "hint":
            if hint_counter < 2:
                hint_counter += 1
                continue
            else:
                print("You already got 2 hints. No more left. Now try guessing.")
        elif player_answer.lower() == article_name.lower():
            print("You guessed correctly! Congratulations!")
            correct_answer = True
            return correct_answer, guess_counter, hint_counter
        else:
            print("Sorry, that was not correct. try again.")
            guess_counter += 1
    print(f"Sorry, no more tries left. You didn't find the correct answer."
          f"The articles name is {article_name}"
          )
    return correct_answer, guess_counter, hint_counter


def calculate_score(correct_answer, guess_counter, hint_counter):
    '''Calculates and adds the score to player_id'''
    if correct_answer:
        score = 1000
        hint_penalty = hint_counter * 100
        guess_penalty = guess_counter * 200
        round_score = score - hint_penalty - guess_penalty
        return round_score


def update_player_score(player_id, round_score):
    '''Updates the player's final score'''
    key = next(iter(player_id))
    player_id[key] += round_score
    return player_id


def main():
    show_menu()
    player_id = get_player_id()
    for i in range(3):
        article_name = get_random_item(hist_list)
        summary = get_summary(article_name)
        blanc_summary = get_blanc_article(article_name, summary)
        print("Let's try guessing! Here is your first hint:")
        print(blanc_summary)
        print()
        player_answer, guess_counter, hint_counter = get_answer_and_hint_request(article_name)
        player_score = calculate_score(player_answer, guess_counter, hint_counter)
        player_id = update_player_score(player_id, player_score)
        print(player_id)


if __name__ == '__main__':
    main()
