from tkinter import *
import random
from WordDictionary import words

spanish_word = None
english_word = None


def spanish_buttons(button):
    global spanish_word
    spanish_word = button
    print(spanish_word)


def english_buttons(button):
    global english_word
    english_word = button
    print(english_word)


def match_checker():
    pass

key_list = list(words.keys())
word_list = []

for _ in range(10):
    spanish_word = random.choice(key_list)
    word_list.append(spanish_word)

translated_list = [words[key] for key in word_list]
random.shuffle(translated_list)

#  The GUI
window = Tk()
window.title("Word Matching Game")
window.geometry("720x1600")

left_frame = Frame(window, bg='darkgrey')
left_frame.grid(row=0, column=0, sticky=N+S+E+W)
Label(left_frame, bg='darkgrey', text="Spanish Words", font=("Arial", 20)).pack(fill=BOTH, expand=True)

for index in range(len(word_list)):
    Button(left_frame,
           text=word_list[index],
           width=15,
           font=("Times New Roman", 12),
           command=lambda w=word_list[index]: spanish_buttons(w)).pack(pady=12)

# Create the right column (for the shuffled matching words)
right_frame = Frame(window, bg='darkgrey')
right_frame.grid(row=0, column=1, sticky=N+S+E+W)

Label(right_frame, bg='darkgrey', text="English Words", font=("Arial", 20)).pack(fill=BOTH, expand=True)
final_display_label = Label(window, bg='darkgrey', fg="green", text="", font=("Arial", 20))
final_display_label.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)

for word in translated_list:
    Button(right_frame,
           text=word,
           width=15,
           font=("Times New Roman", 12),
           command=lambda w=word: english_buttons(w)).pack(pady=12)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

match_checker()

window.mainloop()
