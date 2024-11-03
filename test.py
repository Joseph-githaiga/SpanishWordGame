"""
test.py is a python file for my scrap work or testing code I don't fully understand to see the behaviour.
"""


def reversed_dictionary_constructor(dictionary: dict) -> dict:
    """
    Takes a dictionary and reverses it. Meaning the values in the original dictionary become the keys in the new.
    :param dictionary:
    :return: reversed_dictionary
    :rtype: dict
    """
    reversed_dictionary: dict = {}
    for key, value in dictionary.items():
        if isinstance(value, list):
            # Checks to see if a value is a list i.e. contains multiple values stored in a list.
            for item in value:
                # Takes each value in the list and makes it a key in the reversed_dictionary
                # with the old key as the value
                reversed_dictionary[item] = key
                if item in reversed_dictionary:
                    pass
        else:
            # The value is an int or a string etc...
            reversed_dictionary[value] = key  # swaps the key with the value in the new dictionary.
            if value in reversed_dictionary:
                pass
    return reversed_dictionary


words: dict = {
    "En Ese Caso": "In That Case",
    "Joke": ["Chiste", "Broma"],
    "Debil": "Weak",
    "Decaido": "Weak"}

reversed_words: dict = reversed_dictionary_constructor(words)
for k, v in reversed_words.items():
    print(f"{k}: {v}")
