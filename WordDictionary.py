from admin_panel import load_json, reverse_dict_constructor

# special_characters = ("ñ", "á", "é", "í", "ó", "ú")

words = load_json("words.json")
reversed_dict = reverse_dict_constructor(words)  # Creates a word dictionary of english(key) and spanish(values)
words_key_list = list(words.keys())
words_values_list = list(words.values())
reversed_dict_key_list = list(reversed_dict.keys())
reversed_dict_values_list = list(reversed_dict.values())


if __name__ == "__main__":

    # number_of_words = len(words)
    # print(f"\nThere are {number_of_words} words in the words dictionary", end=" ")
    # print(f"and {len(reversed_dict)} #WORDS in the #REVERSED DICTIONARY.\n")
    for k, v in reversed_dict.items():
        if isinstance(v, tuple):
            print(f"{k}: {v}")
