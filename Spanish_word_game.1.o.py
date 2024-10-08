import random
from WordDictionary import *

key_list = list(words.keys())
value_list = list(words.values())
english_and_spanish_list = [key_list, value_list]


def english_or_spanish():
    eng_or_esp = random.choice(english_and_spanish_list)
    return eng_or_esp


def check_answer(user_input, correct_answer):
    score = 0
    if user_input == correct_answer:
        score += 1
        print("CORRECT!")
        print()
    else:
        score += 0
        print("WRONG!")
        print(f"Correct answer: {correct_answer}.")
        print()
    return score


def take_input():
    count = 1
    score = 0
    while True:
        comp_choice = random.choice(english_or_spanish())
        print(f"{count}. {comp_choice}:")
        response = input("Enter the translation: ").strip().title()
        if response in ("Exit", "Done", "Break", "Bye"):
            break
        else:
            try:  # picks a word in spanish to be translated to English
                score += check_answer(response, words[comp_choice])
            except KeyError:  # picks a word in English to be translated to Spanish
                value_index = value_list.index(comp_choice)
                needed_key = key_list[value_index]
                score += check_answer(response, needed_key)
        count += 1
    return score, count


total = take_input()
correct_answers = total[0]
questions_total = total[1] - 1
percentage = (correct_answers / questions_total) * 100

print()
print("*****************************")
print(f"You got {percentage:.2f}%")
print("Hope to you go so soon. BYE!")
print("*****************************")
