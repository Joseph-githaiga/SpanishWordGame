from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        # Create a label that will display pressed keys
        self.label = Label(text="Press a key!")
        # Bind the on_key_down event to a function
        Window.bind(on_key_down=self.on_key_down)
        return self.label

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # Update label text with the key information
        self.label.text = f"Key pressed: {text} (keycode: {keycode})"

if __name__ == "__main__":
    MyApp().run()
