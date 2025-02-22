# baymax.py
import json
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import speech_recognition as sr
import requests
import time
import serial
import serial.tools.list_ports
from groq import Groq
from playsound import playsound

class Baymax:
    def __init__(self):
        # Initialize API clients with your keys
        self.groq_client = Groq(api_key="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")
        self.eleven_labs_client = ElevenLabs(api_key="sk_34b650649758616292b945a4d6900c247121aec1894e236d")
        self.recognizer = sr.Recognizer()
        
        # Initialize serial connection to Arduino
        self.serial = self.initialize_arduino()
        time.sleep(2)

    def initialize_arduino(self):
        """Automatically detect and connect to Arduino"""
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino" in port.description or "CH340" in port.description or "USB Serial" in port.description:
                try:
                    serial_conn = serial.Serial(port.device, 9600, timeout=1)
                    print(f"Connected to Arduino on {port.device}")
                    return serial_conn
                except serial.SerialException as e:
                    print(f"Failed to connect to {port.device}: {e}")
                    continue
        raise Exception("No Arduino found. Please check connection.")

    def update_page(self, page):
        try:
            response = requests.post(
                "https://baymax-ui.vercel.app/api/page-tracking",
                headers={"Content-Type": "application/json"},
                json={"page": page}
            )
            response.raise_for_status()
            print(f"Page updated to {page}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to update page: {e}")

    def text_to_speech(self, text):
       
        print(f"Converting to speech: {text}")
        audio = self.eleven_labs_client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        play(audio)
        

    def speech_to_text(self):

        with sr.Microphone() as source:
            print("\nListening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5)
        text = self.recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text.lower()
        

    def call_arduino(self, command):
        try:
            print(f"Sending command to Arduino: {command}")
            self.serial.write(command.encode())
            time.sleep(0.1)  # Give Arduino time to process
        except serial.SerialException as e:
            print(f"Failed to send command to Arduino: {e}")
            self.initialize_arduino()  # Try to reconnect

    def receive_serial_data(self):
        try:
            if self.serial.in_waiting > 0:
                data = self.serial.readline().decode().strip()
                print(f"Received from Arduino: {data}")
                return data
        except serial.SerialException as e:
            print(f"Failed to read from Arduino: {e}")
            self.initialize_arduino()  # Try to reconnect
        return None

    def medical_chat(self, message):
        try:
            chat_completion = self.groq_client.chat.completions.create(
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
            print(f"Medical chat error: {e}")
            return "I apologize, but I'm having trouble accessing my medical knowledge right now."

    def therapy_chat(self, message):
        try:
            chat_completion = self.groq_client.chat.completions.create(
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
            print(f"Therapy chat error: {e}")
            return "I'm here to listen and support you, but I'm having trouble formulating my response right now."

    def main_chat(self, message):
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI agent that returns one of these options based on user input: "
                                "medicalsupport(), scan(), emotionalchat(), bruise_spray(). "
                                "If unclear, ask for clarification. If not medical/physical, return default()"
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
            print(f"Main chat error: {e}")
            return "default()"

    def check_temperature(self):
        self.text_to_speech("Let us check your body temperature first, Place your forehead on my palm")
        self.call_arduino("2")
        time.sleep(2)
        temp_data = self.receive_serial_data()
        try:
            return int(temp_data) if temp_data else 0
        except ValueError:
            print("Invalid temperature data received")
            return 0

    def dispense_medication(self, medication):
        medication_commands = {
            "paracetamol": ("3", 5),
            "calpol": ("4", 6),
            "alegra": ("5", 7)
        }
        
        if medication in medication_commands:
            command, page = medication_commands[medication]
            self.call_arduino(command)
            self.update_page(page)
            self.text_to_speech("Here you go, if you are not allergic to this medicine, I recommend you use it")

    def handle_medical_support(self):
        self.text_to_speech("Can I check your temperature?")
        response = self.speech_to_text()
        
        if response and "yes" in response:
            self.update_page(3)
            temp = self.check_temperature()
            self.update_page(4)
            
            if temp > 37:
                self.text_to_speech("Your temperature is higher than normal, describe what you feel")
            else:
                self.text_to_speech("Your temperature seems normal, what is troubling you?")
            
            while True:
                user_input = self.speech_to_text()
                if not user_input or "thank you" in user_input or "bye" in user_input:
                    break
                
                response = self.medical_chat(user_input)
                self.text_to_speech(response)
                
                if response in ["paracetamol", "calpol", "alegra"]:
                    self.dispense_medication(response)
                    break

    def handle_emotional_chat(self):
        self.text_to_speech("Tell me what is disturbing you today?")
        while True:
            user_input = self.speech_to_text()
            if not user_input or "thank you" in user_input or "bye" in user_input:
                break
            response = self.therapy_chat(user_input)
            self.text_to_speech(response)

    def handle_bruise(self):
        self.text_to_speech("I have a pain treating spray for you, should I apply it?")
        answer = self.speech_to_text()
        if answer and "yes" in answer:
            self.call_arduino("6")
            self.update_page(8)
            self.text_to_speech("Applying spray now")
        else:
            self.text_to_speech("Have a great day bye bye!")

    def handle_scan(self):
        self.text_to_speech("Do you want some scans?")
        self.update_page(9)
        user_input = self.speech_to_text()
        
        if user_input and "thank you" not in user_input and "bye" not in user_input:
            self.text_to_speech("What type of scan do you want to perform?")
            scan_type = self.speech_to_text()
            if scan_type and scan_type.lower() in ["xray", "report", "mri"]:
                self.text_to_speech(f"Performing {scan_type} scan. Please wait.")
                time.sleep(10)
                try:
                    api_url = "http://192.168.29.145:5000/predict"
                    response = requests.post(api_url)
                    if response.status_code == 200:
                        self.update_page(10)
                        self.text_to_speech("Scan complete. Thank you for your patience.")
                    else:
                        self.text_to_speech("I'm sorry, there was an error performing the scan.")
                except requests.exceptions.RequestException:
                    self.text_to_speech("I'm sorry, I couldn't connect to the scanning system.")

    def run(self):
        print("Baymax is running. Say 'hello baymax' or 'hi baymax' to start.")
        while True:
            try:
                user_input = "Hi remix"
                if not user_input:
                    continue

                if any(greeting in user_input for greeting in ["hello baymax", "hi baymax", "remix","max"]):
                    self.call_arduino("1")
                    self.text_to_speech("Hi, I am baymax your personal healthcare companion, how may I help you today?")
                    
                    query = self.speech_to_text()
                    if not query:
                        continue

                    action = self.main_chat(query)
                    
                    if "medicalsupport()" in action:
                        self.handle_medical_support()
                    elif "emotionalchat()" in action:
                        self.handle_emotional_chat()
                    elif "bruise()" in action:
                        self.handle_bruise()
                    elif "scan()" in action:
                        self.handle_scan()

            except KeyboardInterrupt:
                print("\nShutting down Baymax...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    def cleanup(self):
        if hasattr(self, 'serial') and self.serial:
            self.serial.close()
        print("Baymax shutdown complete.")

if __name__ == "__main__":
    baymax = Baymax()
    baymax.run()
   