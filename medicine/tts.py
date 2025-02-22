def tts():
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play

    with open("voice_input.txt", "r", encoding="utf-8") as file:
        text_content = file.read()  # Read the entire content
    # Print the text
    print(text_content)


    client = ElevenLabs(api_key="sk_cad8d96e98ac67e9a9a6f3965a66b6c904d48acbae3907e7")

    audio = client.text_to_speech.convert(
        text=text_content,
        voice_id="iP95p4xoKVk53GoZ742B",
        model_id="eleven_turbo_v2",
        output_format="mp3_44100_128",
    )
    play(audio)
