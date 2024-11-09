import pyttsx3


my_voices_names = '''
    Microsoft David Desktop - English (United States)
    Microsoft Hazel Desktop - English (Great Britain)
    Microsoft Zira Desktop - English (United States)
    Microsoft Helena Desktop - Spanish (Spain)
    Microsoft Sabina Desktop - Spanish (Mexico)'''

my_voices_ids = '''
    HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0
    HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-GB_HAZEL_11.0
    HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0
    HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0
    HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0'''

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# List all available voices
voices = engine.getProperty('voices')
voices_dictionary = {}
for item in voices:
    voices_dictionary[item.id] = item.name

for key, value in voices_dictionary.items():
    print(key + ": " + value)


#  = set_voice(0)
#  = set_voice(1)
#  = set_voice(2)
#  = set_voice(3)
#  = set_voice(4)


'''if __name__ == "__main__":

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
    # speak_text(test_text)'''
