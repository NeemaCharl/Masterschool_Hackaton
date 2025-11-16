import wikipedia
from list_of_articles import hist_events_and_persons as hist_list



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
    summary = wikipedia.summary(article_name, sentences=1, auto_suggest=False)
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
        final_score = score - hint_penalty - guess_penalty
        #player_id[player_name] += final_score
        return f"Your final score is {final_score}"


def main():
    show_menu()
    for i in range(3):
        article_name = get_random_item(hist_list)
        summary = get_summary(article_name)
        blanc_summary = get_blanc_article(article_name, summary)
        print("Let's try guessing! Here is your first hint:")
        print(blanc_summary)
        print()
        player_answer, guess_counter, hint_counter = get_answer_and_hint_request(article_name)
        player_score = calculate_score(player_answer, guess_counter, hint_counter)
        print(player_score)


#if __name__ == '__main__':
#    main()

print(get_blanc_article("Marie Curie", get_summary("Marie Curie")))