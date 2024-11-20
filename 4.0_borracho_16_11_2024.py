import json


# %%
def load_json() -> dict:
    with open("words.json", "r", encoding="utf-8") as file:
        return json.load(file)
    

def main():

    print("Welcome to Spanish Word Game.")
    print("Select a mode:")
    print("A: Play all words\nB: Make corrections on previous mistakes.")

    while mode := input().title().strip() not in ("Break", "Quit"):
        if mode == "A":
            print("A")
            break
        elif mode == "B":
            print("B")
            break
        else:
            print("Invalid reposnse. Please type A or B!")
    

words: dict = load_json()


if __name__ == "__main__":
    main()