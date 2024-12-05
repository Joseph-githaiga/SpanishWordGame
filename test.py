def create_file():
    with open("test_file1.txt", "x") as file:
        file.write("\nHello There.")


def append_text():
    with open("test_file1.txt", "a") as file:
        file.write("\nPleasure to meet you.")


create_file()

while True:
    append_text()
