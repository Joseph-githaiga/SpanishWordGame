from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from WordDictionary import words, words_key_list
from voice_config import read_out_loud
import random


class MainGame(GridLayout):

    eurostille_font = StringProperty("fonts/Eurostile.ttf")  # Font name used in the kv file
    sackers_gothic_font = StringProperty("fonts/Sackers-Gothic-Std-Light.ttf")  # Font name used in the kv file
    score: int = 0  # Score to be displayed. Default is 0
    streak: int = 0  # Streak to be displayed. Default is 0
    words_total: int = 5  # Total number of words to be matched
    selected_spanish_words = random.choices(words_key_list, k=words_total)  # Randomly selected words from word's keys
    selected_spanish_word: None | str = None  # Spanish Word selected when the button is tapped. Default is None
    selected_english_word: None | str = None  # English Word selected when the button is tapped. Default is None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.translations: list = self.find_translation()  # Translations to the randomly selected spanish words

        # Adds text to the buttons and add them to the BoxLayout in the Kv File
        # Buttons containing text in Spanish
        for i in range(1, self.words_total + 1):
            btn = Button(text=self.selected_spanish_words[i-1])
            btn.bind(on_press=self.spanish_button_press)
            self.ids.spanish_words.add_widget(btn)

        # Buttons containing text in English
        for i in range(1, self.words_total + 1):
            btn = Button(text=self.translations[i-1])
            btn.bind(on_press=self.english_button_press)
            self.ids.english_words.add_widget(btn)

    def find_translation(self) -> list:
        """
        Takes the 5 randomly selected words and finds their translations in the words dictionary
        :return: list
        """

        translations = []

        for word in self.selected_spanish_words:
            translation: str | list = words[word]
            if isinstance(translation, list):
                translation = random.choice(translation)
            translations.append(translation)
        random.shuffle(translations)
        return translations

    def spanish_button_press(self, instance) -> None:
        """
        Handles what is done when a button with Spanish text is pressed.
        :param instance: This is the representation of the button pressed
        :return: None
        """
        Clock.schedule_once(lambda dt: read_out_loud(output_text=instance.text, output_voice="mexican_spanish"), 1)
        self.ids.display_label.text = ""
        self.selected_spanish_word = instance.text
        self.check_match()

    def english_button_press(self, instance) -> None:
        """
        Handles what is done when a button with English text is pressed.
        :param instance: This is the representation of the button pressed
        :return: None
        """
        Clock.schedule_once(lambda dt: read_out_loud(output_text=instance.text, output_voice="british_english"), 1)
        self.ids.display_label.text = ""
        self.selected_english_word = instance.text
        self.check_match()

    def correct(self) -> None:

        """
        It does several things if words are matched correctly:
        - Increases the score and streak by 1
        - Changes the display label text and colour to green
        - Resets the selected Spanish and English words back to the default
        :return: None
        """

        # If the spanish word is correctly matched.
        self.ids.display_label.color = (0, 1, 0, 1)
        self.ids.display_label.text = "CORRECT!"
        self.score += 1
        self.streak += 1
        self.ids.score_text.text = str(self.score)
        self.ids.streak_text.text = str(self.score)
        self.selected_spanish_word = None
        self.selected_english_word = None

    def incorrect(self) -> None:
        """
        Performs actions if words are matched incorrectly:
        - Resets the streak to 0
        - Changes the display label text and colour
        - Resets the selected words back to None
        :return:
        """
        # Incorrect match
        self.streak = 0
        self.ids.streak_text.text = str(self.streak)
        self.ids.display_label.color = (1, 0, 0, 1)
        self.ids.display_label.text = "INCORRECT!"
        self.selected_spanish_word = None
        self.selected_english_word = None

    def check_match(self) -> None:
        """
        Checks if the selected spanish word matches with the selected english word or in other words checks if the
        translation is correct and increases the score by 1 and the streak by 1.
        If a wrong match is made, the streak resets to 0 but the score remains unchanged.
        :return: None
        """

        # This is simply a shortcut to get around typing the entire variable name
        es = self.selected_spanish_word
        en = self.selected_english_word

        if en is not None and es is not None:
            # Basically means an english word and a spanish word have been selected.
            if isinstance(words[es], list):
                # Checks if the english word has multiple meanings stored in a list
                if en in words[es]:
                    # Checks is the matched word is one in the possible translations
                    self.correct()
                else:
                    self.incorrect()
            else:
                if en == words[es]:
                    self.correct()
                else:
                    self.incorrect()


class SpanishWordGameApp(App):
    def build(self):
        return MainGame()


if __name__ == "__main__":
    SpanishWordGameApp().run()
