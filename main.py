from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import RoundedRectangle, Color
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from WordDictionary import words, sorted_words, words_key_list, reversed_dict
from admin_panel import write_dict_to_json
import random
import pyttsx3
from kivy import require


require("2.3.0")

Builder.load_string("""
#: kivy 2.3.0


<HomeScreen>:

    BoxLayout:
        orientation: "vertical"

        Label:
            text: "S P A N I S H  W O R D  G A M E"
            bold: True
            font_size: 33
            font_name: root.sackers_gothic_font
            color: (1, .5, .8, 1)
            size_hint: (1, .5)

        BoxLayout:
            orientation: "vertical"
            spacing: 5
            padding: 20

            MainMenuButton:
                text: "Main Game"
                on_release: root.manager.current = 'main'
            MainMenuButton:
                text: "Words List"
                on_release: root.manager.current = 'words'
            MainMenuButton:
                text: "Add New Words"
                on_release: root.manager.current = 'new words'
            MainMenuButton:
                text: "Voice Settings"
                on_release: root.manager.current = 'voices'
            MainMenuButton:
                text: "Records"
                on_release: root.manager.current = 'records'
            MainMenuButton:
                text: "Exit"
                on_release: exit()


<MainGame>:
    rows: 3

    BoxLayout:
        id: display_layout
        orientation: "horizontal"
        size_hint_y: .3

        BoxLayout:
            id: score_layout
            Label:
                id: score_label
                text: "Score: "
                font_name: root.eurostille_font
                font_size: 20
                color: (0, 1, 0, 1)

            Label:
                id: score_text
                text: str(root.score)
                font_name: root.eurostille_font
                font_size: 20
                color: (1, 0, 0, 1)

        Label:
            id: display_label
            text: "Match the words!"
            color: (1, 1, 0, 1)
            font_size: 27
            font_name: root.sackers_gothic_font

        BoxLayout:
            id: streak_layout

            Label:
                id: streak_label
                text: "Streak: "
                font_name: root.eurostille_font
                font_size: 20
                color: (0, 1, 0, 1)

            Label:
                id: streak_text
                text: str(root.streak)
                font_name: root.eurostille_font
                font_size: 20
                color: (1, 0, 0, 1)

    GridLayout:
        id: words_layout
        cols: 2
        size_hint_y: .6
        padding: 10

        BoxLayout:
            id: spanish_words
            orientation: "vertical"
            spacing: 5
            padding: [10, 10, 5, 10]  # [left, top, right, bottom]

        BoxLayout:
            id: english_words
            orientation: "vertical"
            padding: [5, 10, 10, 10]  # [left, top, right, bottom]
            spacing: 5

    BoxLayout:
        orientation: "horizontal"
        size_hint: (.5, .1)
        padding: 3
        spacing: 7

        RoundedButton:
            text: "Back"
            size_hint_x: .3
            font_size: 18
            on_release: root.manager.current = 'home'

        RoundedButton:
            id: next_round_button
            text: "Next Round"
            font_size: 18
            on_press:
                root.next_round(self)
            disabled: True


<MainMenuButton@RoundedButton>:

    size_hint: (.7, .7)
    pos_hint: {"center_x": .5}


<RoundedButton>:
    background_color: 0, 0, 0, 0
    canvas.before:
        Color:
            rgba: (.4, .4, .4, 1) if self.state == "normal" else (0, .7, .7, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [37]


<RVLabel@Label>:
    font_size: 20


<AllWords>:
    viewclass: "RVLabel"
    RecycleBoxLayout:
        default_size: None, dp(48)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"


<AddNewWords>:

    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        Button:
            text: "Back"
            on_release: root.manager.current = 'home'
            size_hint: (.3, .1)
        GridLayout:
            cols: 2
            rows: 2
            spacing: 10

            Label:
                id: spanish_textbox_label
                text: "Spanish Word"
                font_size: 40
                size_hint_y: .2
            Label:
                text: "English Word"
                font_size: 40
                size_hint_y: .2
            TextInput:
                id: spanish_word_textbox
                multiline: False
                size_hint_y: .02
                font_size: 30
                background_normal: ""
                background_color: (.3, .3, .3, 1)
                pos_hint: {"center_y": .5}
            TextInput:
                id: english_word_textbox
                multiline: False
                size_hint_y: .02
                font_size: 30
                background_normal: ""
                background_color: (.3, .3, .3, 1)
                pos_hint: {"center_y": .5}
        Button:
            text: "Submit"
            size_hint_x: .3
            size_hint_y: .1
            pos_hint: {"center_x": .5}
            on_press: root.submit()


<VoiceSettings>:

    Button:
        text: "Back"
        on_release: root.manager.current = 'home'
        size_hint: (.2, .08)
        padding: 50
        pos_hint: {"center_x": .5, "center_y": .3}


<Records>:

    Button:
        text: "Back"
        on_release: root.manager.current = 'home'
        size_hint: (.2, .08)
        padding: 50
        pos_hint: {"center_x": .5, "center_y": .3}

""")


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

        # Load audios
        self.correct_audio = SoundLoader.load("audios/correct.mp3")
        self.incorrect_audio = SoundLoader.load("audios/wrong.mp3")
        self.lesson_complete_audio = SoundLoader.load("audios/lesson_complete.mp3")

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

        # Animate button with the selected word
        if instance.text == self.selected_spanish_word:
            if instance.state == "normal":
                instance.background_color = 0, 0, 0, 0
                with self.canvas.before:
                    Color(.4, .4, .4, 1)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[37])
            else:
                instance.background_color = 0, 0, 0, 0
                with self.canvas.before:
                    Color(0, .7, .7, 1)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[37])

        self.check_match()  # Checks if there is a correct match assuming 2 words have been selected

    def english_button_press(self, instance: Button) -> None:
        """
        Handles what is done when a button with English text is pressed.
        :param instance: This is the representation of the button pressed
        :return: None
        """
        self.ids.display_label.text = ""  # Removes the text from the display label in the .kv file
        self.selected_english_word = instance.text  # Stores the text of the button pressed

        # Animate button with the selected word
        if instance.text == self.selected_english_word:
            if instance.state == "normal":
                instance.background_color = 0, 0, 0, 0
                with self.canvas.before:
                    Color(.4, .4, .4, 1)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[37])
            else:
                instance.background_color = 0, 0, 0, 0
                with self.canvas.before:
                    Color(0, .7, .7, 1)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[37])

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
        self.correct_audio.play()  # Plays audio

        self.ids.display_label.color = (0, 1, 0, 1)  # Changes the label colour to green
        self.ids.display_label.text = "CORRECT!"  # Changes label text to correct
        self.score += 1  # Increases the score by 1
        self.streak += 1  # Increases the streak by 1
        self.matched_words += 1  # Increases the matched words count by 1
        self.ids.score_text.text = str(self.score)  # Updates the score label to the current score
        self.ids.streak_text.text = str(self.streak)  # Updates the streak label to the current streak

        if self.matched_words == self.words_total:  # If all words have been matched
            self.lesson_complete_audio.play()  # plays audio
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
        self.incorrect_audio.play()  # Plays audio

        self.streak = 0  # Resets the streak to 0
        self.ids.streak_text.text = str(self.streak)  # Updates the streak label to the current streak
        self.ids.display_label.color = (1, 0, 0, 1)  # Changes the label colour to red
        self.ids.display_label.text = "INCORRECT!"  # Updates the display label text to nothing

        # Write the wrong the corrections to a json file
        corrections: list = [{self.selected_spanish_word: words[self.selected_spanish_word]},
                             {self.find_key_from_value(self.selected_english_word): self.selected_english_word}]
        write_dict_to_json(data=corrections, path="corrections.json", is_sorted=True)

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
            if isinstance(words[es], list):
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

    @staticmethod
    def find_key_from_value(value):
        """
        Finds the key in dictionary using its corresponding value
        """

        for key in words:
            if words[key] == value:
                return key


class RoundedButton(Button):
    pass


class AllWords(Screen, RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data = [{"text": f"{key}:    {value}"} for key, value in sorted_words.items()]


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


class AddNewWords(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words_file = "new_words.json"

    def submit(self) -> None:
        spanish_word: str = self.ids.spanish_word_textbox.text
        english_word: str = self.ids.english_word_textbox.text
        spanish_word = spanish_word.title().strip()
        english_word = english_word.title().strip()

        if not self.words_already_exist(spanish_word, english_word):
            new_words_dict = {spanish_word: english_word}
            write_dict_to_json(new_words_dict, self.words_file, is_sorted=True)

        self.ids.spanish_word_textbox.text = ""
        self.ids.english_word_textbox.text = ""

    @staticmethod
    def words_already_exist(word, translation) -> bool:
        if word in words and translation in reversed_dict:
            return True
        else:
            return False


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
        self.title = "Word Matching Game"  # Window title
        sm = ScreenManager()  # Instantiate the ScreenManager class
        # Add screens to the screen manager
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(MainGame(name="main"))
        sm.add_widget(AllWords(name="words"))
        sm.add_widget(AddNewWords(name="new words"))
        sm.add_widget(VoiceSettings(name="voices"))
        sm.add_widget(Records(name="records"))
        return sm

    def on_start(self):
        Window.size = (640, 800)
        Window.top = 30


if __name__ == "__main__":
    SpanishWordGameApp().run()
