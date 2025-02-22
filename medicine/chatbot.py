from groq import Groq
client = Groq(api_key="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")
def bot(filename="voice_input.txt"):
    # Open the file in read mode and store its content in a variable
    with open(filename, "r", encoding="utf-8") as file:
        text_content = file.read()  # Read the entire content
    # Print the text
    print(text_content)
    user_message = text_content
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a medical assistant or pharmacist. Behave in a very formal and precise manner. "
                        "Don't say anything that is not related to the medical field. Keep the patient around you calm "
                        "and make sure they understand what you are saying. Keep them motivated and ensure they are comfortable."
                        "you have to give medicine only which i am listing  Paracetmol, Calpol,Allegra, Bandages"
                        "Respond in JSON format with the following structure:\n"
                    "{\n"
                    '  "medicine": ["paracetmol", "savlon", "dolo", "vicks"]\n'
                    "}"
                    "if u can't understand a problem of the user aska him again , in other way motivating but don't suggest any medicine if u don't understands "},
            {
                "role": "user",
                "content": user_message
            }
        ],
        
        model="llama-3.3-70b-versatile",  # Make sure the model name is correct    
    )
    # Corrected way to access the response content
    output=chat_completion.choices[0].message.content
    print(output)
    return output
