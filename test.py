from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from WordDictionary import words, words_key_list  # .py file containing words for the game
from admin_panel import write_dict_to_json
import random
import pyttsx3
from typing import Union, List


class MainGame(GridLayout, Screen):
    eurostille_font = StringProperty("fonts/Eurostile.ttf")  # Font for use in .kv file
    sackers_gothic_font = StringProperty("fonts/Sackers-Gothic-Std-Light.ttf")  # Font for use in .kv file
    score: int = 0  # Initial score
    streak: int = 0  # Initial streak
    matched_words: int = 0  # Counter for matched words
    words_total: int = 5  # Total number of words to match per round
    selected_spanish_word: Union[None, str] = None  # Spanish word selected
    selected_english_word: Union[None, str] = None  # English word selected

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize game state and load audio files once for reuse
        self.selected_spanish_words = random.sample(words_key_list, self.words_total)
        self.translations = self.find_translation()
        self.correct_audio = SoundLoader.load("audios/correct.mp3")
        self.incorrect_audio = SoundLoader.load("audios/wrong.mp3")
        self.lesson_complete_audio = SoundLoader.load("audios/lesson_complete.mp3")

        # Create and add buttons with Spanish words
        for i in range(self.words_total):
            spanish_btn = RoundedButton(text=self.selected_spanish_words[i])
            spanish_btn.bind(on_press=self.spanish_button_press)
            self.ids.spanish_words.add_widget(spanish_btn)

            # Create and add buttons with English translations
            english_btn = RoundedButton(text=self.translations[i])
            english_btn.bind(on_press=self.english_button_press)
            self.ids.english_words.add_widget(english_btn)

    def find_translation(self) -> List[str]:
        """
        Finds and shuffles translations for the randomly selected Spanish words.
        :return: List of English translations in random order.
        """
        translations = [
            random.choice(words[word]) if isinstance(words[word], (tuple, list)) else words[word]
            for word in self.selected_spanish_words
        ]
        random.shuffle(translations)
        return translations

    def spanish_button_press(self, instance: Button) -> None:
        """
        Handles press on a Spanish word button.
        :param instance: The Spanish button pressed.
        """
        self.ids.display_label.text = ""  # Clear display label text
        self.selected_spanish_word = instance.text
        self.check_match()

    def english_button_press(self, instance: Button) -> None:
        """
        Handles press on an English word button.
        :param instance: The English button pressed.
        """
        self.ids.display_label.text = ""  # Clear display label text
        self.selected_english_word = instance.text
        self.check_match()

    def correct(self) -> None:
        """
        Updates the game state for a correct match:
        - Increments score and streak.
        - Displays "CORRECT!" message.
        - Plays audio.
        - Disables matched buttons.
        - Enables next round if all words are matched.
        """
        if self.correct_audio:
            self.correct_audio.play()
        self.update_display("CORRECT!", color=(0, 1, 0, 1), score_increase=1, streak_increase=1)
        self.matched_words += 1
        self.disable_buttons()

        if self.matched_words == self.words_total:
            if self.lesson_complete_audio:
                self.lesson_complete_audio.play()
            self.ids.next_round_button.disabled = False
            self.matched_words = 0

    def incorrect(self) -> None:
        """
        Updates the game state for an incorrect match:
        - Resets streak to zero.
        - Displays "INCORRECT!" message.
        - Plays audio.
        - Records the incorrect match in a corrections file.
        """
        if self.incorrect_audio:
            self.incorrect_audio.play()
        self.update_display("INCORRECT!", color=(1, 0, 0, 1), streak_increase=-self.streak)

        # Record incorrect matches in corrections.json
        corrections = [
            {self.selected_spanish_word: words[self.selected_spanish_word]},
            {self.find_key_from_value(self.selected_english_word): self.selected_english_word}
        ]
        write_dict_to_json(data=corrections, path="corrections.json", is_sorted=True)
        self.reset_selections()

    def update_display(self, message: str, color: tuple, score_increase: int = 0, streak_increase: int = 0) -> None:
        """
        Updates display text, color, score, and streak.
        :param message: Text message for display.
        :param color: Color of display text.
        :param score_increase: Amount to increase score by.
        :param streak_increase: Amount to increase/decrease streak by.
        """
        self.score += score_increase
        self.streak = max(0, self.streak + streak_increase)
        self.ids.display_label.text = message
        self.ids.display_label.color = color
        self.ids.score_text.text = str(self.score)
        self.ids.streak_text.text = str(self.streak)

    def disable_buttons(self) -> None:
        """
        Disables buttons with matched words and resets selections.
        """
        for btn in self.ids.spanish_words.children:
            if btn.text == self.selected_spanish_word:
                btn.disabled = True
        for btn in self.ids.english_words.children:
            if btn.text == self.selected_english_word:
                btn.disabled = True
        self.reset_selections()

    def check_match(self) -> None:
        """
        Checks if the selected Spanish and English words match.
        """
        es, en = self.selected_spanish_word, self.selected_english_word
        if en and es and en in words[es] if isinstance(words[es], (tuple, list)) else en == words[es]:
            self.correct()
        elif en and es:
            self.incorrect()

    def reset_selections(self) -> None:
        """
        Resets selected Spanish and English words to None.
        """
        self.selected_spanish_word = None
        self.selected_english_word = None

    def next_round(self, instance: Button) -> None:
        """
        Prepares the next round by generating a new set of words and re-enabling all buttons.
        :param instance: The button initiating the next round.
        """
        instance.disabled = True
        self.selected_spanish_words = random.sample(words_key_list, self.words_total)
        self.translations = self.find_translation()

        # Update button texts for new words
        for idx, btn in enumerate(self.ids.spanish_words.children):
            btn.disabled = False
            btn.text = self.selected_spanish_words[idx]

        for idx, btn in enumerate(self.ids.english_words.children):
            btn.disabled = False
            btn.text = self.translations[idx]

    @staticmethod
    def find_key_from_value(value: str) -> str:
        """
        Finds the Spanish word (key) given an English word (value).
        :param value: The English word to match.
        :return: Corresponding Spanish word or empty string if not found.
        """
        for key, val in words.items():
            if val == value or (isinstance(val, (tuple, list)) and value in val):
                return key
        return ""


class RoundedButton(Button):
    pass


class AllWords(Screen, BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.add_widget(Label(text="Words List Under Development!", font_size=35, bold=True, color=(.5, .5, .5, 1)))


class VoiceSettings(Screen, BoxLayout):

    engine = pyttsx3.init()  # Initiate text to speech engine

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.add_widget(Label(text="VoiceSettings Under Development!", font_size=35, bold=True, color=(.5, .5, .5, 1)))


class Records(Screen, BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.add_widget(Label(text="Records Under Development!", font_size=35, bold=True, color=(.5, .5, .5, 1)))


class AddNewWords(Screen, BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.add_widget(Label(text="Add new words Under Development!", font_size=35, bold=True, color=(.5, .5, .5, 1)))


class HomeScreen(Screen):

    sackers_gothic_font = StringProperty("fonts/Sackers-Gothic-Std-Light.ttf")  # Font name used in the kv file


class SpanishWordGameApp(App):
    def build(self) -> ScreenManager:
        """
        Method override
        Read the documentation from Kivy's website.
        :return: sm
        :rtype: ScreenManager
        """
        sm = ScreenManager()  # Instantiate the ScreenManager class
        # Add screens to the screen manager
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(MainGame(name="main"))
        sm.add_widget(AllWords(name="words"))
        sm.add_widget(AddNewWords(name="new words"))
        sm.add_widget(VoiceSettings(name="voices"))
        sm.add_widget(Records(name="records"))
        return sm


if __name__ == "__main__":
    SpanishWordGameApp().run()
