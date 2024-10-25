from admin_panel import load_json, reversed_dictionary_constructor

# special_characters = ("ñ", "á", "é", "í", "ó", "ú")

words: dict = load_json("words.json")
'''words = {
         "Alcanzar": ["To Reach", "To Achieve"],
         "En Ese Caso": "In That Case",
         "Animarse": ["Bring Yourself To Do Something", "Up For"],
         "Presión": ["Pressure", "Blood Pressure"],
         "Joke": ["Chiste", "Broma"],
         "Novios": ["Bride & Groom", "Boyfriends"]}'''
reversed_dict: dict = reversed_dictionary_constructor(words)
words_key_list: list = list(words.keys())
words_values_list: list = list(words.values())
reversed_dict_key_list: list = list(reversed_dict.keys())
reversed_dict_values_list: list = list(reversed_dict.values())


if __name__ == "__main__":

    number_of_words = len(words)
    print(f"\nThere are {number_of_words} words in the words dictionary")  # , end=" ")
    # print(f"and {len(reversed_dict)} #WORDS in the #REVERSED DICTIONARY.\n")
    print(reversed_dict["To Get"])
