from groq import Groq
import json
client = Groq(api_key="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")
def bot(filename="voice_input.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        text_content = file.read()  # Read the entire content
    # Print the text
    print(text_content)
    user_message = text_content
    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "you are a therapist. Behave in a very formal and precise manner.try to be his family or friend console him and make him feel better.Make him laugh.If the user tells name then call him with his name .give short messages not exceeding 25 words .If the user is thanking you or appreciating you just say thank you and nothing else only thank you."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content":user_message,
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.3-70b-versatile",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_completion_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Print the completion returned by the LLM.
    output = chat_completion.choices[0].message.content
    print(output)
    if output.lower() == "thank you":
        return json.dumps({"thankyou": True})  # Return as JSON string
    return json.dumps({"thankyou": False, "response": output}) 