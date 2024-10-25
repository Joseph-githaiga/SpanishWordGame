import pyttsx3
from kivy.clock import Clock


# Function to set a specific voice
def set_voice(voice_index):
    engine.setProperty('voice', voices[voice_index].id)


# Function to read text aloud
def speak_text(text):
    engine.setProperty('rate', 150)  # Speed (words per minute)
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()


def read_out_loud(output_text, output_voice):
    if output_voice == "american_english_male":
        set_voice(0)
    elif output_voice == "british_english":
        set_voice(1)
    elif output_voice == "american_english_female":
        set_voice(2)
    elif output_voice == "european_spanish":
        set_voice(3)
    elif output_voice == "mexican_spanish":
        set_voice(4)
    else:
        print("No such voice")
        set_voice(1)
    speak_text(output_text)

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# List all available voices
voices = engine.getProperty('voices')

#  = set_voice(0)
#  = set_voice(1)
#  = set_voice(2)
#  = set_voice(3)
#  = set_voice(4)


if __name__ == "__main__":

    # Print all available voices with details
    for index, voice in enumerate(voices):
        print(f"Voice {index}:")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Gender: {'Male' if 'male' in voice.id.lower() else 'Female'}")
        print(f" - Language: {voice.languages}")
    # Example usage: set a Spanish voice (change the index to match the desired voice)
    # set_voice(3)  # Adjust the index based on your output above

    # Example text in Spanish
    test_text = "Hola, estoy leyendo este texto en voz alta utilizando un acento español."
    # speak_text(test_text)
    read_out_loud(test_text, "mexican_spanish")
