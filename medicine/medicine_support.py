import medicine.commu as commu
import medicine.audio_rec as audio_rec
import medicine.chatbot as chatbot
import json

def main():
    ismed = False  # This should be set to True only when a medicine is found
    texts = "Ohh!! You are not well. Tell me what's the problem? Maybe I can help."
    commu.tts(texts)
    while not ismed:
        audio_rec.record_voice()
        response = chatbot.bot()

        try:
            response_json = json.loads(response)  # Convert response to JSON
            if "medicine" in response_json and response_json["medicine"]:  # Check if medicines exist
                ismed = True
            else:
                commu.tts(response)  # Continue conversation
        except json.JSONDecodeError:
            commu.tts("I'm sorry, I didn't understand that. Can you repeat?")

main()
