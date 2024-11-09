from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from WordDictionary import words, words_key_list  # .py file containing words to be used in the game
import random
import pyttsx3


class MainGame(GridLayout, Screen):

    # Class variables
    eurostille_font = StringProperty("fonts/Eurostile.ttf")  # Font name used in the kv file
    sackers_gothic_font = StringProperty("fonts/Sackers-Gothic-Std-Light.ttf")  # Font name used in the kv file
    score: int = 0  # Score to be displayed. Default is 0
    streak: int = 0  # Streak to be displayed. Default is 0
    matched_words: int = 0  # Keeps track of number of matched words.
    words_total: int = 5  # Total number of words to be matched
    selected_spanish_word: None | str = None  # Spanish Word selected when the button is clicked. Default is None
    selected_english_word: None | str = None  # English Word selected when the button is clicked. Default is None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Instance variables
        self.selected_spanish_words: list = random.sample(words_key_list, self.words_total)  # Randomly selected words
        self.translations: list = self.find_translation()  # Translations to the randomly selected spanish words above

        # Adds text to the buttons and add them to the BoxLayout in the Kv File
        # Buttons containing text in Spanish
        for i in range(1, self.words_total + 1):
            btn = RoundedButton(text=self.selected_spanish_words[i-1])  # Adds text to the Spanish buttons
            btn.bind(on_press=self.spanish_button_press)  # Binds a function to the button press
            self.ids.spanish_words.add_widget(btn)  # Adds the buttons to the kivy window

        # Buttons containing text in English
        for i in range(1, self.words_total + 1):
            btn = RoundedButton(text=self.translations[i-1])  # Adds text to the English buttons
            btn.bind(on_press=self.english_button_press)  # Binds a function to the button press
            self.ids.english_words.add_widget(btn)  # Adds the buttons to the kivy window

    def find_translation(self) -> list:
        """
        Takes the 5 randomly selected words and finds their translations in the words dictionary
        :return: translations
        :rtype: list
        """

        translations: list = []  # Empty list to store words

        for word in self.selected_spanish_words:  # Iterates over the list
            translation: str | list | tuple = words[word]  # Adds the correct translation to the list above
            if isinstance(translation, tuple):  # Checks if a word has multiple translations stored in a tuple
                translation = random.choice(translation)  # Randomly picks one translation
            elif isinstance(translation, list):  # Checks if a word has multiple translations stored in a list
                translation = random.choice(translation)  # Randomly picks one translation
            translations.append(translation)  # Adds the translation to the list
        random.shuffle(translations)  # Shuffles the list so the words/ translations answers aren't aligned side to side
        return translations

    def spanish_button_press(self, instance: Button) -> None:
        """
        Handles what is done when a button with Spanish text is pressed.
        :param instance: This is the representation of the button pressed
        :return: None
        """
        self.ids.display_label.text = ""  # Removes the text from the display label in the .kv file
        self.selected_spanish_word = instance.text  # Stores the text of the button pressed
        self.check_match()  # Checks if there is a correct match assuming 2 words have been selected

    def english_button_press(self, instance: Button) -> None:
        """
        Handles what is done when a button with English text is pressed.
        :param instance: This is the representation of the button pressed
        :return: None
        """
        self.ids.display_label.text = ""  # Removes the text from the display label in the .kv file
        self.selected_english_word = instance.text  # Stores the text of the button pressed
        self.check_match()  # Checks if there is a correct match assuming 2 words have been selected

    def correct(self) -> None:

        """
        It does several things if words are matched correctly:
        - Increases the score and streak by 1
        - Changes the display label text and colour to green
        - Resets the selected Spanish and English words back to the default
        - Disables buttons containing matched words
        :return: None
        """
        # If the spanish word is correctly matched.
        my_audio = SoundLoader.load("audios/correct.mp3")  # Loads audio
        my_audio.play()  # Plays audio

        self.ids.display_label.color = (0, 1, 0, 1)  # Changes the label colour to green
        self.ids.display_label.text = "CORRECT!"  # Changes label text to correct
        self.score += 1  # Increases the score by 1
        self.streak += 1  # Increases the streak by 1
        self.matched_words += 1  # Increases the matched words count by 1
        self.ids.score_text.text = str(self.score)  # Updates the score label to the current score
        self.ids.streak_text.text = str(self.streak)  # Updates the streak label to the current streak

        if self.matched_words == self.words_total:  # If all words have been matched
            lesson_complete_audio = SoundLoader.load("audios/lesson_complete.mp3")  # Loads audio
            lesson_complete_audio.play()  # plays audio
            self.ids.next_round_button.disabled = False  # Activates the next round button
            self.matched_words = 0  # Resets the matched words count to 0 for the next round

        for btn in self.ids.spanish_words.children:  # Iterates over Spanish buttons
            if btn.text == self.selected_spanish_word:  # Validates which button to disable
                btn.disabled = True  # Disables the button

        for btn in self.ids.english_words.children:  # Iterates over English buttons
            if btn.text == self.selected_english_word:  # Validates which button to disable
                btn.disabled = True  # Disables the button

        # Resets the selected words to None
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
        my_audio = SoundLoader.load("audios/wrong.mp3")  # Loads audio
        my_audio.play()  # Plays audio

        self.streak = 0  # Resets the streak to 0
        self.ids.streak_text.text = str(self.streak)  # Updates the streak label to the current streak
        self.ids.display_label.color = (1, 0, 0, 1)  # Changes the label colour to red
        self.ids.display_label.text = "INCORRECT!"  # Updates the display label text to nothing

        # Resets the selected words to None
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
            if isinstance(words[es], tuple):
                # Checks if the english word has multiple meanings stored in a tuple
                if en in words[es]:
                    # Words are correctly matched
                    self.correct()
                else:
                    # Words are incorrectly matched
                    self.incorrect()
            else:
                # The translation only contains a single word in a string.
                if en == words[es]:
                    # Words are correctly matched
                    self.correct()
                else:
                    # Words are incorrectly matched
                    self.incorrect()

    def next_round(self, instance: Button) -> None:
        """
        It generates a new list of words if all the words have been matched correctly.
        Also changes the text of the old buttons to fit the new selected words
        Lastly disables the next round button
        :return: None
        """
        instance.disabled = True  # Disables the button
        self.selected_spanish_words = random.sample(words_key_list, self.words_total)  # Picks a new list of words
        self.translations: list = self.find_translation()  # Finds their translations

        for index, button in enumerate(self.ids.spanish_words.children):
            button.disabled = False  # Activates all the buttons
            button.text = self.selected_spanish_words[index]  # Changes the text according to the new selected words
        for index, button in enumerate(self.ids.english_words.children):
            button.disabled = False  # Activates all the buttons
            button.text = self.translations[index]  # Changes the text according to the new selected words


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

    engine = pyttsx3.init()  # Initiate text to speech engine

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.add_widget(Label(text="Records Under Development!", font_size=35, bold=True, color=(.5, .5, .5, 1)))

    
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
        sm.add_widget(VoiceSettings(name="voices"))
        sm.add_widget(Records(name="records"))
        return sm


if __name__ == "__main__":
    SpanishWordGameApp().run()
