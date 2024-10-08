import random
import json
from WordDictionary import words, reversed_dict
from admin_panel import write_json

json_file = "new_dict.json"


def check_answer(user_input, correct_answer):  # Checks if the user input is the correct translation.

    score = 0
    corrections = {}  # Empty dictionary to collect wrong translations by user along with the correct answer.

    def corrector(word):  # Checks which dictionary the word selected at random is from.

        if word in reversed_dict:
            translation_ = reversed_dict[word]  # Finds the correct translation.
        else:  # This means the word is in the word's dictionary.
            translation_ = words[word]
        return translation_

    if user_input == correct_answer:  # Checks if user translated correctly.
        score += 1
        print("CORRECT!")
        print()
    else:  # Collects the wrong translation and adds it to the dictionary and gives the user the correct answer.
        translation = corrector(correct_answer)
        corrections[translation] = correct_answer
        score += 0
        print("WRONG!")
        print(f"Correct answer: {correct_answer}.")
        print()
    return score, corrections


def main():  # Main body of code.

    counter = 1
    score = 0
    merged_dict = {}

    print("Welcome to SpanishWordGame. Type 'Exit' to stop playing.\nGood Luck!\n")
    print("Select a mode:")
    mode_type = input("Test yourself on all words (A):\nor\nMake corrections on previous mistakes (B)? ").upper()

    def english_or_spanish(mode):  # Randomly selects a dictionary and returns the dictionary.

        while True:

            if mode == "A":
                english_and_spanish_list = [words, reversed_dict]  # Creates a list of the 2 dictionaries.
                eng_or_esp = random.choice(english_and_spanish_list)
                return eng_or_esp

            elif mode == "B":
                try:
                    with open(json_file, 'r') as json_dict:
                        imported_corrections_dict = json.load(json_dict)
                except FileNotFoundError:

                    print("\nNo corrections found!".upper())
                    exit()
                return imported_corrections_dict
            else:
                print("Invalid response! Answer with 'A' or 'B'.")

    if mode_type == "A":

        while True:
            comp_choice = random.sample(list(english_or_spanish("A").keys()), 1)[0]
            print(f"\n{counter}. {comp_choice}:")
            response = input("Enter the translation: ").strip().title()
            if response in ("Exit", "Done", "Break", "Bye", "Quit"):
                break
            else:
                try:  # picks a word in spanish to be translated to English
                    score_1, corrections = check_answer(response, words[comp_choice])
                    score += score_1
                    merged_dict.update(corrections)
                except KeyError:  # picks a word in English to be translated to Spanish
                    score_2, corrections = check_answer(response, reversed_dict[comp_choice])
                    score += score_2
                    merged_dict.update(corrections)
            counter += 1
        return score, counter, merged_dict

    elif mode_type == "B":

        while True:
            comp_choice = random.sample(list(english_or_spanish("B").keys()), 1)[0]
            print(f"\n{counter}. {comp_choice}:")
            response = input("Enter the translation: ").strip().title()
            if response in ("Exit", "Done", "Break", "Bye", "Quit"):
                break
            else:
                try:  # picks a word in spanish to be translated to English
                    score_1, corrections = check_answer(response, words[comp_choice])
                    score += score_1
                    merged_dict.update(corrections)
                except KeyError:  # picks a word in English to be translated to Spanish
                    score_2, corrections = check_answer(response, reversed_dict[comp_choice])
                    score += score_2
                    merged_dict.update(corrections)
            counter += 1
        return score, counter, merged_dict
    else:
        print("Invalid Choice")


def final_display():  # Displays the final score

    try:
        correct_answers, questions_total, final_corrections = main()  # Calls the Main Function.
        write_json(file_path=json_file, new_data=final_corrections)
        percentage = (correct_answers / (questions_total - 1)) * 100

        print()
        print("****************************************************************************")
        print(f"You got {percentage:.2f}%")

        match percentage:
            case _ if 0 <= percentage <= 25:
                print("Poor effort. put in more work.😒")
                print("Here are your corrections:\n")
            case _ if 50 >= percentage >= 25:
                print("You can do better. Work a bit harder.😌")
                print("Here are your corrections:\n")
            case _ if 80 >= percentage >= 50:
                print("Splendid! But you're not quite there yet.😏")
                print("Here are your corrections:\n")
            case _ if 100 > percentage >= 80:
                print("Almost perfect. Well done!👏")
                print("Here are your corrections:\n")
            case _ if percentage == 100:
                print("You couldn't outdo yourself if you tried. Have a beer on the house.😉🎇")
            case _:
                print("Error! Something went Wrong")

        num_display = 1

        for key, value in final_corrections.items():
            print(f"{num_display}. {key}: {value}")
            num_display += 1

        print()
        print("Hope to you go so soon. BYE!")
        print("****************************************************************************")
    except ZeroDivisionError:
        print(f"\nThere are {len(words)} words in the dictionary.")

final_display()
