from openai import OpenAI
from dotenv import load_dotenv
import os


class OpenAIWrapper:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def transcribe_audio(self, file_path):
        audio_file = open(file_path, "rb")

        transcription = self.client.audio.transcriptions.create(
            file=audio_file,
            model="gpt-4o-transcribe",
        )

        return transcription.text

    def generate_latex(self, text):
        prompt = "You will receive a verbal description of a mathematical expression. Your task is to convert this description into LaTeX code. Please provide only the LaTeX code without any additional explanations or text. Here is the description: "
        model = "gpt-5.4-nano"
        input = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
        response = self.client.responses.create(
            model=model,
            input=input,
        )
        return response.output_text