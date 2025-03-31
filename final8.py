

import azure.cognitiveservices.speech as speechsdk
import serial
import time
from groq import Groq
import requests


groq_client = Groq(api_key="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")

ser = serial.Serial("/dev/serial0",115200, timeout=1)

SPEECH_KEY = "F9Gcgcr3uBODrscmhrMUEaorbV6WF9H6bqc4kghYsNqvcux9ZavxJQQJ99BCACYeBjFXJ3w3AAAYACOGYQHZ"
SERVICE_REGION = "eastus"

speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

def pg(d):
    url="https://baymax-ui.vercel.app/api/page-tracking"
    data ={
        "page":d,
    }
    response = requests.post(url, json=data)
    print(response.text)

def stt():
    print("Listening... Speak now!")

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized Text: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech recognition canceled:", result.cancellation_details)
        return None
def tts(text_given):
    text = text_given  # Taking user input
    pg(50)
    result = speech_synthesizer.speak_text_async(text).get()
    pg(13)
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis successful.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech synthesis canceled:", result.cancellation_details)

def mri():
    api_url="http://localhost:5000/mri"

    try:
        # Send POST request to the API endpoint
        response = requests.post(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            print(f"Response: {response.text}")
            
            # Try to parse JSON response if available
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=4)}")
                return json_response
            except json.JSONDecodeError:
                print("Response is not in JSON format")
                return response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


def esp32(num):
    ser.write(f"{num}\n".encode())
    print(num)
def scan ():
    tts("please upload your bone xrays only")
    pg(9)
    time.sleep(30)
    mri()
def receive_serial_data():
    """Receive data from Arduino"""
    try:
        if serial.in_waiting > 0:
            return serial.readline().decode().strip()
        return None
    except Exception as e:
        print(f"Error receiving serial data: {str(e)}")
        return None
def medical_chat(message):
    """Handle medical chat interactions"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                        "role": "system",
                        "content": "You are a medical assistant or pharmacist. Behave formally and precisely. "
                                "Keep patients calm and ensure understanding. Keep them motivated and comfortable. "
                                "You have medicines: paracetamol, alegra and calpol. Return just the medicine name "
                                "if recommending, otherwise provide medical advice."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error in medical chat: {str(e)}")
        return "I apologize, but I'm having trouble accessing my medical knowledge right now."
def therapy_chat(message):
    """Handle therapy chat interactions"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a therapist. Be formal and precise. Console and comfort the user. "
                            "Make them laugh. Use their name if provided. Keep responses under 25 words. "
                            "Just say 'thank you' for appreciation."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error in therapy chat: {str(e)}")
        return "I'm here to listen and support you, but I'm having trouble processing right now."
def main_chat(message):
    """Handle main chat routing"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI agent keep the response small as much possible and  that returns one of                                                                                                                         these options based on user input: "
                            "medicalsupport(), scan(), emotionalsupport(), bruise_spray(). "
                            "If unclear, ask for clarification. If not a mdeical/emotional query or input by the user                                                                                                                         , return default()"
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error in main chat: {str(e)}")
        return "default()"
def check_temperature():
    """Check body temperature"""
    try:
        pg(3)
        esp32("2")
        time.sleep(8)
        temp_data = receive_serial_data()
        if temp_data:
            pg(4)
            return int(temp_data)

    except Exception as e:
        print(f"Error checking temperature: {str(e)}")
        return 37
def dispense_medication(medication):
    """Dispense medication and update UI"""
    try:
        if medication == "paracetamol":
            esp32("3")
            pg(5)
        elif medication == "calpol":
            esp32("4")
            pg(6)
        elif medication == "alegra":
            esp32("5")
            pg(7)
        tts("Here you go, if you are not allergic to this medicine, I recommend you not use it")
        return 0
    except Exception as e:
        stt(f"Error dispensing medication: {str(e)}")
        return 1
def check_d(x):
    deactivation_words = ["bye", "thank you"]
    for i in deactivation_words:
         if i in x.lower():
             return False
         else:
             return True
def bruise():
        tts("I have a pain relief spray for you, DFO spray, would u like me to apply it ? ")
        user_input = stt()
        output2 = main_chat(user_input.lower())
        if "yes" in  user_input.lower() or "yep" in user_input.lower() or "sure" in user_input.lower():
                pg(8)
                esp32("6")
                tts("Place ur hand directly above the nozel for me to spray it for you")
        else:
            while (check_d(user_input.lower())):
                tts(therapy_chat(user_input.lower()))
                user_input = stt()
                user_input = user_input.lower()
                if output2 == "scan()":
                    tts("Switching to Medical Scan Diagnosis")
                    scan()
                    break
                elif output2 == "medicalsupport()":
                    tts("Switching to medcial support")
                    bruise()
                    break
                elif output2 == "emotion()":
                    tts("Switching to emotional support")
                    emotionalsupport()
                    break
def medicalsupport():
    tts("Switching to medical support Can i know what is troubling you so that i can help ")
    user_input = stt()
    tts(medical_chat(user_input.lower()))
    tts("can i check your temperature ? ")
    user_input = stt()
    if "yes" in user_input.lower() or "yep" in user_input.lower() or "sure" in user_input.lower() or "ofcourse" in user_input.lower():
        temperature = 28
        tts("Place your forehead on my palm, So that i can check your temperature.")
        pg(3)
        if temperature > 27:
                 medical_chat("my temperature is 37 degree celcius ")
                 while (check_d(user_input.lower())):
                     user_input = stt()
                     output = medical_chat(user_input)
                     output2 = (main_chat(user_input))
                     if output2 == "scan()":
                         tts("Switching to Medical Scan Diagnosis")
                         scan()
                         break
                     elif output2 == "bruise()":
                         tts("Switching to pain relief mechanism")
                         bruise()
                         break
                     elif output2 == "emotion()":
                         tts("Switching to emotional support")
                         emotionalsupport()
                         break
                     tts(output)
                     if output == "calpol":
                         dispense_medication("calpol")
                         tts("I suggest you to take Calpol, if u are not allergic to it.")
                     elif output == "paracetamol":
                         dispense_medication("paracetamol")
                         tts("I suggest you to take paracetamol")
                     elif output == "alegra":
                         dispense_medication("alegra")
                         tts("I suggest u to take allegra")
    while (check_d(user_input.lower())):
        output = medical_chat(user_input)
        output2 = (main_chat(user_input))
        if output2 == "scan()":
            tts("Switching to Medical Scan Diagnosis")
            scan()
            break
        elif output2 == "bruise()":
            tts("Switching to pain relief mechanism")
            bruise()
            break
        elif output2 == "emotion()":
            tts("Switching to emotional support")
            emotionalsupport()
            break
        tts(output)
        if output == "calpol":
            dispense_medication("calpol")
            tts("I suggest you to take Calpol, if u are not allergic to it.")
        elif output == "paracetamol":
            dispense_medication("paracetamol")
            tts("I suggest you to take paracetamol")
        elif output == "alegra":
            dispense_medication("alegra")
            tts("I suggest u to take allegra")
        user_input = stt()
def emotionalsupport():
        tts("Switching to emotional support tell me what i can help you with?")
        user_input = stt()
        user_input = user_input.lower()
        output2 = main_chat(user_input)
        while(check_d(user_input)):
                tts(therapy_chat(user_input()))
                user_input = stt()
                user_input = user_input.lower()
                if output2 == "scan()":
                    tts("Switching to Medical Scan Diagnosis")
                    scan()
                    break
                elif output2 == "bruise()":
                    tts("Switching to pain relief mechanism")
                    bruise()
                    break
                elif output2 == "medicalsupport()":
                    tts("Switching to medical support")
                    medicalsupport()
                    break
user_input = stt()
user = user_input.lower()
activation = ["b max","baymax","max","baemax"]
deactivation ="bye"
for i in activation:
    if i in user:
        pg(100)
        esp32("1")
        tts("Hi I am BayMax Your Personal Healthcare Assistant How may I help you Today !")
        time.sleep(3.7)
        break
while(deactivation not in user_input):
        user_input = stt()
        user_input = user_input.lower()
        action = main_chat(user_input)
        if "medicalsupport()" in  action:
                medicalsupport()
        elif "emotionalsupport()" in action:
                emotionalsupport()
        elif "bruise()" in action:
                bruise()
        elif "scan()" in action:
                scan()
        else:
            tts(action)
