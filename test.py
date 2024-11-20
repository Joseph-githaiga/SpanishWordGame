from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
import random
import pyttsx3

# Assuming the following imports and variables are defined elsewhere:
# words: Dictionary mapping words to their definitions or translations
# words_key_list: List of all keys (words) from the `words` dictionary
# reversed_dict: A dictionary mapping translations/definitions back to words
# write_dict_to_json: Function to save the dictionary to a JSON file

from WordDictionary import words, words_key_list, reversed_dict
from admin_panel import write_dict_to_json

# Kivy UI layout
Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Welcome to Word Trainer!"
            font_size: '24sp'
            size_hint_y: 0.2
        Button:
            text: "Start Practice"
            font_size: '20sp'
            size_hint_y: 0.4
            on_release: app.root.current = 'practice_screen'
        Button:
            text: "Exit"
            font_size: '20sp'
            size_hint_y: 0.4
            on_release: app.stop()

<PracticeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: word_label
            text: root.current_word
            font_size: '32sp'
            size_hint_y: 0.2
        GridLayout:
            cols: 2
            Button:
                id: choice_1
                text: root.choice_1
                font_size: '18sp'
                on_release: root.check_answer(self.text)
            Button:
                id: choice_2
                text: root.choice_2
                font_size: '18sp'
                on_release: root.check_answer(self.text)
            Button:
                id: choice_3
                text: root.choice_3
                font_size: '18sp'
                on_release: root.check_answer(self.text)
            Button:
                id: choice_4
                text: root.choice_4
                font_size: '18sp'
                on_release: root.check_answer(self.text)
        Label:
            id: feedback_label
            text: root.feedback
            font_size: '18sp'
            size_hint_y: 0.1
        Button:
            text: "Back to Home"
            font_size: '20sp'
            size_hint_y: 0.2
            on_release: app.root.current = 'home'
""")

# Screen classes
class HomeScreen(Screen):
    pass


class PracticeScreen(Screen):
    current_word = StringProperty("")
    choice_1 = StringProperty("")
    choice_2 = StringProperty("")
    choice_3 = StringProperty("")
    choice_4 = StringProperty("")
    feedback = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_correct = SoundLoader.load('audios/correct.mp3')
        self.audio_wrong = SoundLoader.load('audios/wrong.mp3')
        self.tts_engine = pyttsx3.init()
        self.generate_question()

    def generate_question(self):
        """Generate a new question with one correct and three incorrect choices."""
        self.current_word = random.choice(words_key_list)
        correct_answer = words[self.current_word]
        choices = [correct_answer] + random.sample(
            [v for v in words.values() if v != correct_answer], 3
        )
        random.shuffle(choices)

        self.choice_1, self.choice_2, self.choice_3, self.choice_4 = choices
        self.feedback = ""

    def check_answer(self, selected_choice):
        """Check if the selected answer is correct and provide feedback."""
        correct_answer = words[self.current_word]
        if selected_choice == correct_answer:
            self.feedback = "Correct!"
            if self.audio_correct:
                self.audio_correct.play()
        else:
            self.feedback = f"Wrong! The correct answer was: {correct_answer}"
            if self.audio_wrong:
                self.audio_wrong.play()

        # Text-to-speech for the current word
        self.tts_engine.say(self.current_word)
        self.tts_engine.runAndWait()

        # Generate a new question
        self.generate_question()


# Main application
class WordTrainerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PracticeScreen(name='practice_screen'))
        return sm


if __name__ == "__main__":
    WordTrainerApp().run()
