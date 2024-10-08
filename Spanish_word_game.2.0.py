import random
from WordDictionary import *

spanish_list = list(words.keys())  # Creates a list of the words in spanish
english_list = list(words.values())  # Creates a list of the words in english
english_and_spanish_list = [spanish_list, english_list]  # Creates a 2D list of the lists above.


def english_or_spanish():  # Randomly selects a list and returns the list.
    eng_or_esp = random.choice(english_and_spanish_list)
    return eng_or_esp


def corrector(word):
    if word in english_list:  # Checks which list the word selected at random is from.
        word_index = english_list.index(word)  # Finds the index of the word chosen.
        translation = spanish_list[word_index]  # Uses the index to find the correct translation in the second list.
    else:
        word_index = spanish_list.index(word)  # Finds the index of the word chosen.
        translation = english_list[word_index]  # Uses the index to find the correct translation in the second list.
    return translation


def check_answer(user_input, correct_answer):  # Checks if the user input is the correct translation.
    score = 0
    corrections = {}  # Empty dictionary to collect wrong translations by user along with the correct answer.
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
    print("Welcome to SpanishWordGame. Type 'Exit' to stop playing.\nGood Luck!\n")
    count = 1
    score = 0
    merged_dict = {}
    while True:
        comp_choice = random.choice(english_or_spanish())
        print(f"{count}. {comp_choice}:")
        response = input("Enter the translation: ").strip().title()
        if response in ("Exit", "Done", "Break", "Bye", "Quit"):
            break
        else:
            try:  # picks a word in spanish to be translated to English
                score_1, corrections = check_answer(response, words[comp_choice])
                score += score_1
                merged_dict.update(corrections)
            except KeyError:  # picks a word in English to be translated to Spanish
                value_index = english_list.index(comp_choice)
                needed_key = spanish_list[value_index]
                score_2, corrections = check_answer(response, needed_key)
                score += score_2
                merged_dict.update(corrections)
        count += 1
    return score, count, merged_dict


try:
    correct_answers, questions_total, final_corrections = main()  # Calls the Main Function.
    percentage = (correct_answers / (questions_total - 1)) * 100

    print()
    print("****************************************************************************")
    print(f"You got {percentage:.2f}%")

    if percentage <= 25:
        print("Poor effort. put in more work.😒")
        print("Here are your corrections:\n")
    elif 50 >= percentage >= 25:
        print("You can do better. Work a bit harder.😌")
        print("Here are your corrections:\n")
    elif 80 >= percentage >= 50:
        print("Splendid! But you're not quite there yet.😏")
        print("Here are your corrections:\n")
    elif 100 > percentage >= 80:
        print("Almost perfect. Well done!👏")
        print("Here are your corrections:\n")
    else:
        print("You couldn't outdo yourself if you tried. Have a beer on the house.😉🎇")

    num_display = 1

    for key, value in final_corrections.items():
        print(f"{num_display}. {key}: {value}")
        num_display += 1

    print()
    print("Hope to you go so soon. BYE!")
    print("****************************************************************************")
except ZeroDivisionError:
    print(f"\nThere are {len(words)} words in the dictionary.")
