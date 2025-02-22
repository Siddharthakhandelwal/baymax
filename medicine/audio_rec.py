import speech_recognition as sr

def record_voice(filename="voice_input.txt"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now:")
        recognizer.energy_threshold=500
        recognizer.pause_threshold=500
        recognizer.non_speaking_duration = 0.5
        recognizer.dynamic_energy_threshold = True
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)  # Convert speech to text
        print("You said:", text)

        # Save to file
        with open(filename, "w") as file:
            file.write(text)
        print(f"Text saved to {filename}")

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results, check your internet connection.")

# Run the function

