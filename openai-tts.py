import json
import asyncio

from pathlib import Path
from openai import OpenAI

voices = {
    'алесь': 'onyx',
    'мара': 'shimmer',
    'ron': 'onyx',
    'hermiona': 'shimmer'
}

json_file_path = 'text-en.json'

async def synthesize_speech(text, voice, id):
    id_str = str(id)
    print("№" + id_str + " started")
    client = OpenAI()
    file_path = "speech" + id_str + ".mp3";
    speech_file_path = Path(__file__).parent / file_path
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text
    )

    response.stream_to_file(speech_file_path)
    print("№" + id_str + " done")

async def voice_dialogues(json_file, voices):
    with open(json_file, 'r', encoding='utf-8') as file:
        dialogues = json.load(file)

    for dialogue in dialogues:
        speaker = dialogue['name']
        text = dialogue['text']
        id = dialogue['id']

        voice = voices.get(speaker, 'default')

        await synthesize_speech(text, voice, id)

asyncio.run(voice_dialogues(json_file_path, voices))

  