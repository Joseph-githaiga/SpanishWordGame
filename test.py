
words_sample = {
    "Soportar": ["To Support", "To Endure", "To Stand", "To Stomach"],  # Multiple meanings for "Soportar"
    "Desagradable": "Unpleasant",
    "Empleo": "Employment",
    "Terrorismo": "Terrorism",
    "Por Último": "Lastly",
    "Apropiado": ["Suitable", "Adequate"],  # Multiple meanings for "Apropiado"
    "Carpa": "Tent",
    "Armar": "To Set Up",
    "Sí O Sí": "No Matter What",
    "Mochilero": "Backpacker",
    "Chiste": "Joke",  # "Chiste" and "Broma" have the same value
    "Broma": "Joke"
}


def reversed_dictionary_constructor(dictionary: dict) -> dict:
    """
    This function takes a dictionary with words and their meanings,
    and returns a new dictionary where the keys are the meanings
    and the values are the corresponding words.

    If a meaning has multiple words associated with it, it stores them as a list.
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


# Call the function with the words_sample dictionary
my = reversed_dictionary_constructor(words_sample)

# Print the reversed dictionary in a readable format
for k, val in my.items():  # Loop through the reversed dictionary
    if isinstance(val, list):  # If the value is a list (multiple words)
        val = ", ".join(val)  # Join the list into a comma-separated string for printing
    print(f"{k}: {val}")  # Print the meaning (key) and its corresponding word(s) (value)
