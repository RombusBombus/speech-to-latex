from openai import OpenAI
from dotenv import load_dotenv
import os


def transcribe_audio(file_path):
    print(file_path)
    load_dotenv()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio_file = open(file_path, "rb")

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="gpt-4o-transcribe",
    )

    return transcription.text