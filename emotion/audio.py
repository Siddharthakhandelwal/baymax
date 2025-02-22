import speech_recognition as sr

def record_voice(filename="voice_input.txt"):
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise

        try:
            audio = recognizer.listen(source, timeout=5)  # Listen with a 5s timeout
            print("Processing...")

            # Convert speech to text using Google's speech recognition API
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")

            # Save the text to a file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)

            print(f"Text saved to {filename}")
            return text

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Error with the speech recognition service.")
        except Exception as e:
            print(f"An error occurred: {e}")

    return None


