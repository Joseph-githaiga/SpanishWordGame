import json
import os


def load_json(path: str) -> dict:
    """
    This function reads a json file and returns the dictionary stored within to be used in python code.
    :param path: The path of the json file to be read.
    :return: dict1: This is the constructed dictionary
    """

    with open(path, "r", encoding="utf-8") as words_dict:
        dict1 = json.load(words_dict)
        for key in dict1:
            value = dict1[key]
            if isinstance(value, list):
                dict1[key] = tuple(value)
        write_dict_to_json(data=dict1, path="sorted_words.json", is_sorted=True)
    return dict1


def write_dict_to_json(data: dict, path: str, is_sorted=False) -> None:
    """
    Writes a dictionary into a .json file.

    :param data: This is the dictionary to be written to a json file.
    :param path: This is the .json file's path.
    :param is_sorted: An optional argument to sort the dictionary alphabetically.
    :return: None
    """
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as sample_data:
            existing_data = json.load(sample_data)

        existing_data.update(data)

        if is_sorted:
            existing_data = dict(sorted(existing_data.items()))

        with open(path, "w", encoding="utf-8") as final_data:
            json.dump(existing_data, final_data, indent=4, ensure_ascii=False)
    else:
        with open(path, "w", encoding="utf-8") as new_file:
            if is_sorted:
                data = dict(sorted(data.items()))
            json.dump(data, new_file, indent=4, ensure_ascii=False)


def reversed_dictionary_constructor(dictionary: dict) -> dict:
    """
    This function takes a dictionary with words and their meanings,
    and returns a new dictionary where the keys are the meanings
    and the values are the corresponding words.

    If a meaning has multiple words associated with it, it stores them as a list.

    :return: The reversed dictionary
    :rtype: dict
    """
    reversed_dictionary = {}  # Initialize an empty dictionary for reversed data
    for key, value in dictionary.items():  # Iterate through the original dictionary
        if isinstance(value, list):  # If the value is a list of meanings
            for v in value:  # Iterate through each meaning in the list
                if v in reversed_dictionary:
                    # If the meaning is already in the reversed dictionary, append the new key
                    if isinstance(reversed_dictionary[v], list):
                        reversed_dictionary[v].append(key)  # Append to the existing list
                    else:
                        reversed_dictionary[v] = [reversed_dictionary[v], key]  # Convert to list and append
                else:
                    reversed_dictionary[v] = key  # Add meaning as key, and word as value
        else:
            # If the value is not a list (just a single meaning)
            if value in reversed_dictionary:
                # If the meaning already exists, append the new word to the list
                if isinstance(reversed_dictionary[value], list):
                    reversed_dictionary[value].append(key)
                else:
                    reversed_dictionary[value] = [reversed_dictionary[value], key]  # Convert to list and append
            else:
                reversed_dictionary[value] = key  # Add meaning as key, and word as value
    return reversed_dictionary  # Return the reversed dictionary


if __name__ == "__main__":
    # word_finder("word_")
    print("Hello World!!!")
