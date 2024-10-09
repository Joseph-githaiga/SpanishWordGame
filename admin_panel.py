import json
import os


def load_json(path):
    with open(path, "r", encoding="utf-8") as words_dict:
        dict1 = json.load(words_dict)
        for key in dict1:
            value = dict1[key]
            if isinstance(value, list):
                dict1[key] = tuple(value)
    return dict1


def write_json(file_path, new_data):
    # Check if the file exists
    if os.path.exists(file_path):
        # If the file exists, read its current content
        with open(file_path, 'r', encoding="utf-8") as file:
            try:
                # Load existing data from the JSON file
                existing_data = json.load(file)
            except json.JSONDecodeError:
                # If the file is empty or invalid, start with an empty list
                existing_data = []

        # Append new data to the existing data
        if isinstance(existing_data, list):
            existing_data.append(new_data)
        elif isinstance(existing_data, dict):
            existing_data.update(new_data)

        # Write the updated data back to the file
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
    else:
        # If the file doesn't exist, create a new one and write the new data
        with open(file_path, 'w') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)


def reverse_dict_constructor(d):
    reversed_dict = {}

    for key, value in d.items():
        if isinstance(value, tuple):
            # If the value is a tuple, create multiple keys for each item in the tuple
            for v in value:
                if v in reversed_dict:
                    # If the key exists, append the new key to a tuple
                    if isinstance(reversed_dict[v], tuple):
                        reversed_dict[v] += (key,)
                    else:
                        reversed_dict[v] = (reversed_dict[v], key)
                else:
                    reversed_dict[v] = key
        else:
            # If the value is a string, handle it directly
            if value in reversed_dict:
                # If the key already exists, append the new key
                if isinstance(reversed_dict[value], tuple):
                    reversed_dict[value] += (key,)
                else:
                    reversed_dict[value] = (reversed_dict[value], key)
            else:
                reversed_dict[value] = key

    return reversed_dict


if __name__ == "__main__":
    # word_finder("word_")
    print("Hello World!!!")
