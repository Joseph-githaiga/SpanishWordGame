import json
import os
from typing import Union, Dict, List


def load_json(path: str) -> dict:
    """
    This function reads a json file and returns the dictionary stored within to be used in python code.
    :param path: The path of the json file to be read.
    :return: dict1: This is the constructed dictionary
    """

    with open(path, "r", encoding="utf-8") as words_dict:
        dict1 = json.load(words_dict)
        write_dict_to_json(data=dict1, path="sorted_words.json", is_sorted=True)
    return dict1


def write_dict_to_json(data: Union[dict, list], path: str, is_sorted: bool = False) -> None:
    """
    Writes a dictionary or list into a .json file.

    :param data: The dictionary or list to be written to a JSON file.
    :param path: The .json file's path.
    :param is_sorted: Optionally sorts the dictionary alphabetically.
    :return: None
    """
    if os.path.exists(path):
        # Use a context manager to ensure file is closed after reading
        with open(path, "r", encoding="utf-8") as sample_data:
            existing_data: Union[dict, list] = json.load(sample_data)

        if isinstance(data, dict) and isinstance(existing_data, dict):
            existing_data.update(data)
            if is_sorted:
                existing_data = dict(sorted(existing_data.items()))

        elif isinstance(data, list) and isinstance(existing_data, list):
            existing_data.extend(data)

        # Use another context manager for writing
        with open(path, "w", encoding="utf-8") as final_data:
            json.dump(existing_data, final_data, indent=4, ensure_ascii=False)

    else:
        # Write new file if path doesn't exist
        with open(path, "w", encoding="utf-8") as new_file:
            if is_sorted and isinstance(data, dict):
                data = dict(sorted(data.items()))
            json.dump(data, new_file, indent=4, ensure_ascii=False)


def swapped_words(dictionary: Dict[str, Union[str, List[str]]]) -> Dict[str, Union[str, List[str]]]:
    """
    This function takes a dictionary with Spanish words as keys and their translations in English as values
    and returns a new dictionary where the English words are keys and the Spanish words are values.

    Some of the Spanish words in the original dictionary have multiple translations stored in a list.

    If several Spanish words have the same translation, e.g., "Chiste - Joke" and "Broma - Joke,"
    the English word becomes a key, and its value is a list containing all the former keys, e.g., ["Broma", "Chiste"].

    :param dictionary: Dictionary containing keys and values as strings or lists.
    :return: A new dictionary containing values as keys and vice versa.
    :rtype: dict
    """
    reversed_dictionary: Dict[str, Union[str, List[str]]] = {}

    for spanish_word, english_translations in dictionary.items():
        # Handle when English translations are a list
        if isinstance(english_translations, list):
            for english_word in english_translations:
                if english_word in reversed_dictionary:
                    # Append to list if key exists
                    if isinstance(reversed_dictionary[english_word], list):
                        reversed_dictionary[english_word].append(spanish_word)
                    else:
                        reversed_dictionary[english_word] = [reversed_dictionary[english_word], spanish_word]
                else:
                    reversed_dictionary[english_word] = spanish_word
        else:
            # Handle single English translation
            english_word = english_translations
            if english_word in reversed_dictionary:
                if isinstance(reversed_dictionary[english_word], list):
                    reversed_dictionary[english_word].append(spanish_word)
                else:
                    reversed_dictionary[english_word] = [reversed_dictionary[english_word], spanish_word]
            else:
                reversed_dictionary[english_word] = spanish_word

    # Ensure all values in the result are lists if they contain multiple items
    for key, value in reversed_dictionary.items():
        if isinstance(value, list):
            reversed_dictionary[key] = list(set(value))  # Remove duplicates if any

    write_dict_to_json(reversed_dictionary, "reversed_words.json", is_sorted=True)

    return reversed_dictionary


if __name__ == "__main__":
    # word_finder("word_")
    write_dict_to_json({"Hello": "Hola"}, "new_words.json")
