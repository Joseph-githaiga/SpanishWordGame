from admin_panel import load_json, swapped_words

# special_characters = ("ñ", "á", "é", "í", "ó", "ú")

words: dict = load_json("words.json")
sorted_words: dict = load_json("sorted_words.json")
reversed_dict: dict = swapped_words(words)
sorted_reversed_dict: dict = swapped_words(sorted_words)
# write_dict_to_json(reversed_dict, "reversed_words.json", is_sorted=True)
words_key_list: list = list(words.keys())
words_values_list: list = list(words.values())
reversed_dict_key_list: list = list(reversed_dict.keys())
reversed_dict_values_list: list = list(reversed_dict.values())


if __name__ == "__main__":

    print(f"\nThere are {len(words)} words in words.json", end=" ")
    print(f"and {len(reversed_dict)} words in the REVERSED DICTIONARY.\n")
