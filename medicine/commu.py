# import assemblyai as aai
import pyttsx3
text="Hi I am siddhartha , how are you"
def tts(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 125)  # Reduced speed for a softer tone
    engine.setProperty('volume', 0.7)  # Lower volume for a gentler sound

    # Choose a soft voice
    voices = engine.getProperty('voices')
    # Print all available voices
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name}, ID: {voice.id}, Language: {voice.languages}")

    # Select a soft voice (adjust the index based on your preferences)
    engine.setProperty('voice', voices[1].id)  # Adjust index as needed

    # Input text to speak
    
    #if not passed then define it here first
    # Speak the text
    engine.say(text)
    file_path = "baymax_audio.mp3"  # Change the path as needed  
    engine.save_to_file(text, file_path)  


    # Wait for the speech to finish
    engine.runAndWait()
tts(text)
# tts()
# stt()
