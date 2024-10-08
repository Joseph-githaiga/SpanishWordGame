import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# List all available voices
voices = engine.getProperty('voices')

# Print all available voices with details
for index, voice in enumerate(voices):
    print(f"Voice {index}:")
    print(f" - ID: {voice.id}")
    print(f" - Name: {voice.name}")
    print(f" - Gender: {'Male' if 'male' in voice.id.lower() else 'Female'}")
    print(f" - Language: {voice.languages}")

# Function to set a voice
def set_voice(voice_index):
    engine.setProperty('voice', voices[voice_index].id)

# Function to read text aloud
def speak_text(text):
    engine.setProperty('rate', 150)  # Speed (words per minute)
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# Example usage: set a Spanish voice (you may need to change the index)
set_voice(1)  # Change the index to choose a different voice

# Example text in Spanish
text = "Hola, estoy leyendo este texto en voz alta utilizando Python."
speak_text(text)
