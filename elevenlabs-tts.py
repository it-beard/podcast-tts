import asyncio
import json
import os
import requests

from pathlib import Path

voices = {
    'ron': '29vD33N1CtxCmqQRPOHJ', # Drew, news
    'hermiona': 'EXAVITQu4vr4xnSDxMaL' # Sarah, news
}

json_file_path = 'text-en.json'

async def synthesize_speech(text, voice, id):
    id_str = str(id)
    print("№" + id_str + " started")

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": os.getenv('xi-api-key')
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.1,
            "similarity_boost": 0.5
        }
    }
    output_file_name = "speech" + id_str + ".mp3";
    response = requests.post(url, json=data, headers=headers)
    with open(output_file_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
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

  