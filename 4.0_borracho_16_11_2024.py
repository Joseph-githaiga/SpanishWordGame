import json
import random


# %%
def load_json(path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_questions(words_file: dict):
    while True:
        selected_word = random.choice(words_file)
        counter: int = 1
        print(f"{counter}. {selected_word}\n\n")
        counter += 1
        return selected_word, input("Translation: ")


def match_check(selected_word, user_input, words_dictionary):
    if words_dictionary[selected_word] == user_input:
        return True
    else:
        return False


def main():

    score: int = 0

    print("Welcome to Spanish Word Game.")
    print("Select a mode:\n\n")
    print("A: Play all words\nB: Make corrections on previous mistakes.")

    while mode := input("\n\n").title().strip() not in ("Break", "Quit"):
        if mode == "A":
            selected_word, user_input = load_questions(all_words)

            if match_check(selected_word, user_input, all_words):
                score += 1
            break
        elif mode == "B":
            selected_word, user_input = load_questions(corrections)
            if match_check(selected_word, user_input, all_words):
                score += 1
    

all_words: dict = load_json("words.json")
corrections = load_json("corrections.json")


if __name__ == "__main__":
    main()
