#import libcamera
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import speech_recognition as sr
import subprocess
import time
from picamera2 import Picamera2
import os
import serial
import numpy as np
import requests
import cv2
import io
from groq import Groq
from PIL import Image
import base64



client=Groq(api_key="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")
picam2=Picamera2()
client_ele=ElevenLabs(api_key="sk_0e4986f9d5d486fb0545f57434b7e1194b95488a16e63aab")
recognizer=sr.Recognizer()
picam2.configure(picam2.create_still_configuration())
picam2.start()
ser = serial.Serial("/dev/serial0",9600,timeout=1)
time.sleep(5)

def tts(x):
    try:
        audio=client_ele.text_to_speech.convert(
            text=x,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        play(audio)
        return 
    except Exception as e:
        print(e)
        tts("I am sorry, I am unable to speak right now")
        return 

def stt():
    try:
        with sr.Microphone() as source:
            print("Listening")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        text=recognizer.recognize_google(audio)
        print(text)
        return text
    except Exception as e:
         print(e)
         tts("I am sorry, I am unable to understand your speech")
         stt()
         return text

def call_arduino_functions(function_name):
    ser.write(function_name.encode())
    data = ser.readline().decode('utf-8').strip()
    print("Arduino function called")
    return data
def check_emotion():
    image=picam2.capture_array()
    is_success,buffer=cv2.imencode(".bmp",image)
    if not is_success:
        print("couldnt get the image in the buffer")
    image_bytes=buffer.tobytes()
    image_base64=base64.b64encode(image_bytes).decode("utf-8")
    api_url="http://192.168.137.34:8000/get_results"
    file=image_base64
    response=requests.post(api_url,json={"image":file})
    return response.json()
def scan_xray():
    api_url=""
    response=response.get(api_url)
    return response
def medical_emotion(x):
    user_message=x
    chat_completion = client.chat.completions.create(
    messages=[
            {
                "role": "system",
                "content": "You are a medical assistant or pharmacist. Behave in a very formal and precise manner. "
                        "Don't say anything that is not related to the medical field. Keep the patient around you calm "
                        "and make sure they understand what you are saying. Keep them motivated and ensure they are comfortable."
            "you have medicines such as paracetamol, alegra and calpol, if u want to recommend any of these to the user just return their name as written above"
            "or else just talk to them and try to know what the problem is"
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        model="llama-3.3-70b-versatile",
        )
    output=chat_completion.choices[0].message.content
    return output
def therapist_chatbot(x):
    user_message=x
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a therapist. Behave in a very formal and precise manner.try to be his family or friend console him and make him feel better.Make him laugh.If the user tells name then call him with his name .give short messages not exceeding 25 words .If the user is thanking you or appreciating you just say thank you and nothing else only thank you."
            },
                {
                "role": "user",
                "content":user_message,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
        )
    output = chat_completion.choices[0].message.content
    return output
def main_chatbot(x):
    user_message=x
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a ai agent that
                        needs to act as a function,
                        you  have to understand the user input
                        and then return any from the following options
                        medicalsupport(),scan(),emotionalchat(),bruise_spray()
                        if you are unable to understand what the user is saying , tell the user to explain
                        more what is required by him/her,if the user is talking anything which cannot be
                        classified as physical or medical explaination of his/her needs  return default()
                        do not tell the user any of the options, just return what you think might be the most
            usefull to the user"""
            },
                {
                "role": "user",
                "content":user_message,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
        )
    output = chat_completion.choices[0].message.content
    return output
def check_activation(x):
    activation_words=["hello baymax","hi baymax","remix","yes"]
    for word in activation_words:
        if word in x:
            return True
    return False
def check_deactivation(x):
    deactivation_words=["thank you","thanks","bye","never mind"]
    for word in deactivation_words:
                if word in x:
                        return False
    return True
def recieve_data():
    import serial

    # Open serial port (Use /dev/serial0 on newer Pi models)
    ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

    while True:
            if ser.in_waiting > 0:  # Check if data is available
                data = ser.readline().decode("utf-8").strip()
                print(f"Received: {data}")
    return data
def api_page_change(change):
    return change;
def main():
    user_input=stt()
    user_input=user_input.lower()
    user_words=user_input.split(" ")
    deactivation_words=["thank you","nothing","thanks","bye","never mind"]
    activation_words=["hello baymax","hi baymax","yes"]
    response="Hi, I am baymax your personal healthcare companion, how may i help you today"
    options="default()"
    if check_activation(user_input):
        call_arduino_functions("1")
        tts(response)
        while options=="default()":
            query=stt()
            options=main_chatbot(query)

    if check_deactivation(user_input):
        match options:
            case "medicalsupport()":
                tts("can i check your temperature")
                perm=["yes","no"]
                response=stt()
                if "yes"in response:
                        tts("Let us check your body temperature first, Place ur forhead on my palm")
                        call_arduino_functions("2")
                        temp=int(recieve_data())
                        if temp>37:
                            tts("Your body temperature is higher than normal, describe what you feel")
                            user_input=stt()
                            tts(medical_emotion(f"{user_input} + the body temperature right now is"))
                            tts("If u want more info please explain ur situation")
                            while check_deactivation(user_input):
                                user_input=stt()
                                output=medical_emotion(user_input)
                                tts(output)
                                if output=="paracetamol":
                                        call_arduino_functions("3")
                                        tts("Here you go , if you are not allergiuc to this medicine, i recommend you not use it")
                                        break
                                elif output=="calpol":
                                        call_arduino_functions("4")
                                        tts("Here you go , if you are not allergiuc to this medicine, i recommend you not use it")
                                        break
                                elif output=="alegra":
                                        call_arduino_functions("5")
                                        tts("Here you go , if you are not allergiuc to this medicine,  i recommend you not use it")
                                        break
                        else:
                            tts("Your temperature seems normal to me, what is troubling you ?")
                            user_input = stt()
                            while check_deactivation(user_input):
                                user_input=stt()
                                output=medical_emotion(user_input)
                                tts(output)
                                if output=="paracetamol":
                                        call_arduino_functions("3")
                                        tts("Here you go , if you are not allergiuc to this ,i recommend you not use it")
                                        break
                                elif output=="calpol":
                                        call_arduino_functions("4")
                                        tts("Here you go , if you are not allergiuc to this i recommend you not use it")
                                        break
                                elif output=="alegra":
                                        call_arduino_functions("5")
                                        tts("Here you go , if you are not allergiuc to this i recommend you not use it")
                                        break

                else:
                    while check_deactivation(user_input):
                        user_input=stt()
                        output=medical_emotion(user_input)
                        tts(output)
                        if output=="paracetamol":
                            call_arduino_functions("3")
                            tts("Here you go , if you are not allergiuc to this medicine, i would recommend on of them to you")
                            break
                        elif output=="calpol":
                            call_arduino_functions("4")
                            tts("Here you go , if you are not allergiuc to this medicine, i would recommend on of them to you")
                            break
                        elif output=="alegra":
                            call_arduino_functions("5")
                            tts("Here you go , if you are not allergiuc to this medicine, i would recommend on of them to you")
                            break
            case "emotionalchat()":
                tts("Tell me what is disturbing you today?")
                while check_deactivation(user_input):
                    user_input=stt()
                    tts(therapist_chatbot(user_input))
            case "bruise()":
                tts("I have a pain treating spray for you, should i apply it to you? yes or no????")
                answer = stt()
                if answer=="yes":
                    call_arduino_functions("6")
                elif answer=="no":
                    tts("Have a great day bye bye!")
            case "scan()":
                tts("Give me some files to analyze")
                tts("Do you want some scans")
                #change page api function
                user_input = stt()
                if check_deactivation(user_input):
                    #page change api for scans available
                    tts("What type of scan do u wanna perform?")
                    user_input=stt()
                    if user_input=="xray":
                        tts(scan_xray())
                        #page change api for it
                        tts("Thank you")
                    elif user_input=="report":
                        tts(scan_xray())
                        #page change api for it
                        tts("Thank you")
                    elif user_input=="mri":
                        tts(scan_xray())
                        #page change api for it
                        tts("Thank you")
        

if __name__=="__main__":
        main()



