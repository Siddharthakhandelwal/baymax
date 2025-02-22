import bot
import audio
import json

while True:
    audio.record_voice()
    response = bot.bot()  # This is now a JSON string

    try:
        response_json = json.loads(response)  # Convert JSON string to dictionary
        print(response_json)  # Debugging: See actual JSON output

        if response_json.get("thankyou", False):  # Check if "thankyou": true
            print("User said thank you. Exiting loop.")
            break  # Exit loop
    except json.JSONDecodeError:
        print("Error: Invalid JSON response received.")
