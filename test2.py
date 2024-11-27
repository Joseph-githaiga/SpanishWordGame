from kivy.app import App
from kivy. uix.recycleview import RecycleView
from WordDictionary import words


class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{"text": f"{key}: {value}"} for key, value in words.items()]


class MyApp(App):
    def build(self):
        return MyRecycleView()


if __name__ == "__main__":
    MyApp().run()
