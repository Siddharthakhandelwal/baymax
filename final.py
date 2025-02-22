import json
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import speech_recognition as sr
import subprocess
import time
from picamera2 import Picamera2
import serial
import requests
import cv2
import base64
from groq import Groq

class Baymax:
    def __init__(self):
        self.groq_client = Groq(api_key="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")
        self.eleven_labs_client = ElevenLabs(api_key="sk_37038c01d573407a8d4400a15b7ec7b9db7d5215252e596a")
        self.recognizer = sr.Recognizer()

        # Add maximum retry attempts for speech recognition
        self.max_retries = 3

        # Initialize camera
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start()

        # Initialize serial
        self.serial = serial.Serial("/dev/serial0", 9600, timeout=1)
        time.sleep(2)

    def response(self):
        api_url = "http://192.168.137.1:5000/mri"
        response = requests.post(api_url)


    def update_page(self, page):
        """Update the UI page"""
        try:
            data = json.dumps({"page": page})
            subprocess.run([
                "curl", "-X", "POST",
                "https://baymax-ui.vercel.app/api/page-tracking",
                "-H", "Content-Type: application/json",
                "-d", data
            ])
        except Exception as e:
            print(f"Error updating page: {str(e)}")

    def text_to_speech(self, text):
        """Convert text to speech using ElevenLabs"""
        try:
            audio = self.eleven_labs_client.text_to_speech.convert(
                text=text,
                voice_id="JBFqnCBsd6RMkjVDRZzb",
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            play(audio)
        except Exception as e:
            print(f"Text-to-speech error: {str(e)}")
            self.text_to_speech("I am sorry, I am unable to speak right now")

    def speech_to_text(self, prompt=None, max_attempts=3):
        """
        Enhanced speech to text with retry mechanism and user feedback
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                if prompt:
                    self.text_to_speech(prompt)

                with sr.Microphone() as source:
                    self.update_page(13)
                    print(f"Listening... (Attempt {attempts + 1}/{max_attempts})")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)

                text = self.recognizer.recognize_google(audio)
                if text:
                    print(f"Recognized: {text}")
                    return text.lower()

            except sr.WaitTimeoutError:
                self.text_to_speech("I didn't hear anything. Could you please speak again?")
                self.update_page(50)
            except sr.UnknownValueError:
                self.update_page(50)
                self.text_to_speech("I couldn't understand that. Could you please repeat?")
            except sr.RequestError:
                self.update_page(50)
                self.text_to_speech("There was an error with the speech recognition service.")
            except Exception as e:
                self.update_page(50)
                print(f"Error in speech recognition: {str(e)}")

            attempts += 1
        self.update_page(50)
        return None

    def call_arduino(self, command):
        """Send command to Arduino"""
        try:
            self.serial.write(command.encode())
        except Exception as e:
            print(f"Error sending command to Arduino: {str(e)}")

    # def check_emotion(self):
    #     """Analyze emotion from camera image"""
    #     try:
    #         image = self.picam2.capture_array()
    #         _, buffer = cv2.imencode(".bmp", image)
    #         image_base64 = base64.b64encode(buffer).tobytes().decode("utf-8")

    #         response = requests.post(
    #             "http://192.168.137.34:8000/get_results",
    #             json={"image": image_base64}
    #         )
    #         return response.json()
    #     except Exception as e:
    #         print(f"Error in emotion detection: {str(e)}")
    #         return None
    def medical_support(self):
        response = self.speech_to_text("Can I check your temperature?")

        if response and "yes" in response or "sure" in response:
            self.update_page(3)
            temp = self.check_temperature()
            self.update_page(4)

            prompt = "Your temperature is higher than normal, describe what you feel" if temp > 37 else "Your temperature seems normal, what is troubling you?"

            retry_count = 0
            while retry_count < self.max_retries:
                user_input = self.speech_to_text(prompt)
                if not user_input:
                    retry_count += 1
                    continue

                if "thank you" in user_input or "bye" in user_input:
                    break

                response = self.medical_chat(user_input)
                self.text_to_speech(response)

                if response in ["paracetamol", "calpol", "alegra"]:
                    self.dispense_medication(response)
                    break
                if "bruise" in user_input:
                    self.bruise()
                    break
                elif "scan" in user_input:
                    self.scan()
                    break
                elif "emotional" or "sad" in user_input:
                    self.emotional_support()
                    break
        else :
             prompt="then what else can i help u with"
             self.update_page(3)
             retry_count = 0
             while retry_count < self.max_retries:
                user_input = self.speech_to_text(prompt)
                if not user_input:
                    retry_count += 1
                    continue

                if "thank you" in user_input or "bye" in user_input:
                    break

                response = self.medical_chat(user_input)
                self.text_to_speech(response)

                if response in ["paracetamol", "calpol", "alegra"]:
                    self.dispense_medication(response)
                    break
                if "bruise" in user_input:
                    self.bruise()
                    break
                elif "scan" in user_input:
                    self.scan()
                    break
                elif "emotional" or "sad" in user_input:
                    self.emotional_support()
                    break
    def emotional_support(self):
        retry_count = 0
        while retry_count < self.max_retries:
            user_input = self.speech_to_text("Tell me what is disturbing you today?")
            if not user_input:
                retry_count += 1
                continue

            if "thank you" in user_input or "bye" in user_input:
                break

            self.text_to_speech(self.therapy_chat(user_input))
            if "bruise" in user_input:
                self.bruise()
                break
            elif "scan" in user_input:
                self.scan()
                break
            elif "fever" in user_input or "ill" in user_input or "headache" in user_input:
                self.emotional_support()
                break
            retry_count = 0
    def scan(self):
        user_input = self.speech_to_text("Do you want some scans?")
        self.update_page(9)

        if user_input and "thank you" not in user_input and "bye" not in user_input:
            scan_type = self.speech_to_text("What type of scan do you want to perform?")

            if scan_type in ["xray", "report", "mri"]:
                self.response()
                self.update_page(10)
                self.text_to_speech("Thank you")

            if "bruise" in user_input:
                self.bruise()
                return
            elif "fever" in user_input or "ill" in user_input or "headache" in user_input:
                self.emotional_support()
                return
            elif "emotional" or "sad" in user_input:
                self.emotional_support()
                return
    def bruise(self):
        answer = self.speech_to_text("I have a pain treating spray for you, should I apply it?")
        if answer and "yes" in answer:
            self.call_arduino("6")
            self.update_page(8)
        else:
            self.text_to_speech("Have a great day bye bye!")
        user_input = self.speech_to_text("Do you want something else")
        if "scan" in user_input:
            self.scan()
            return
        elif "fever" in user_input or "ill" in user_input or "headache" in user_input:
            self.emotional_support()
            return
        elif "emotional" or "sad" in user_input:
            self.emotional_support()
            return

    def receive_serial_data(self):
        """Receive data from Arduino"""
        try:
            if self.serial.in_waiting > 0:
                return self.serial.readline().decode().strip()
            return None
        except Exception as e:
            print(f"Error receiving serial data: {str(e)}")
            return None

    def medical_chat(self, message):
        """Handle medical chat interactions"""
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
            print(f"Error in medical chat: {str(e)}")
            return "I apologize, but I'm having trouble accessing my medical knowledge right now."

    def therapy_chat(self, message):
        """Handle therapy chat interactions"""
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
            print(f"Error in therapy chat: {str(e)}")
            return "I'm here to listen and support you, but I'm having trouble processing right now."

    def main_chat(self, message):
        """Handle main chat routing"""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI agent keep the response small as much possible and  that returns one of these options based on user input: "
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
            print(f"Error in main chat: {str(e)}")
            return "default()"

    def check_temperature(self):
        """Check body temperature"""
        try:
            self.text_to_speech("Let us check your body temperature first, Place your forehead on my palm")
            self.call_arduino("2")
            time.sleep(10)
            temp_data = self.receive_serial_data()
            if temp_data:
                return int(temp_data)

        except Exception as e:
            print(f"Error checking temperature: {str(e)}")
            return 37

    def dispense_medication(self, medication):
        """Dispense medication and update UI"""
        try:
            if medication == "paracetamol":
                self.call_arduino("3")
                self.update_page(5)
            elif medication == "calpol":
                self.call_arduino("4")
                self.update_page(6)
            elif medication == "alegra":
                self.call_arduino("5")
                self.update_page(7)
            self.text_to_speech("Here you go, if you are not allergic to this medicine, I recommend you not use it")
        except Exception as e:
            print(f"Error dispensing medication: {str(e)}")

    def run(self):
        user_input = self.speech_to_text("Waiting for activation. say 'hi max'")
        """Main run loop"""
        if "hello baymax" in user_input or "hi baymax" in user_input or "remix" in user_input or "max" in user_input or "hi" in user_input :
            self.update_page(1)
            self.call_arduino("1")
            time.sleep(1)
            query = self.speech_to_text("Hi, I am baymax your personal healthcare companion, how may I help you today?")
            action = self.main_chat(query)
            while True:
                
                if "medicalsupport()" in action:
                    self.medical_support()

                elif "emotionalchat()" in action:
                    self.emotional_support() # Reset counter for new valid inputs

                elif "bruise()" in action:
                    self.bruise()

                elif "scan()" in action:
                    self.scan()
                else:
                    queery=self.speech_to_text(action)
                    action=self.main_chat(queery)
                    
                    


    def cleanup(self):
        """Clean up resources"""
        try:
            self.picam2.stop()
            self.serial.close()
            self.update_page(100)
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    baymax = Baymax()
    try:
        baymax.run()
    except KeyboardInterrupt:
        baymax.cleanup()
    except Exception as e:
        print(f"Critical error: {str(e)}")
        baymax.cleanup()
