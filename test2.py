
for number in range(1, 101):

    if number % 3 == 0 and number % 5 == 0:
        print(f"{number}: fizzbizz")
    elif number % 3 == 0:
        print(f"{number}: fizz")
    elif number % 5 == 0:
        print(f"{number}: bizz")
