import speech_recognition as sr
recognizer=sr.Recognizer()
def stt():
    with sr.Microphone() as source:
        print("Listening")
        # recognizer.dynamic_energy_threshold=True
        recognizer.energy_threshold=4000
        recognizer.adjust_for_ambient_noise(source)
        
        audio = recognizer.listen(source)
        print("done")
    text=recognizer.recognize_whisper(audio,language="en",model="large")
    print(text)
    return text
stt()


