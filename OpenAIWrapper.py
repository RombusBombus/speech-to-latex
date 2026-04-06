from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path


class OpenAIWrapper:
    def __init__(self):
        load_dotenv()
        prompts_folder = Path("prompts")

        with open(prompts_folder / "generate_latex_prompt.txt", "r") as f:
            self.generate_latex_prompt = f.read()

        with open(prompts_folder / "edit_latex_prompt.txt", "r") as f:
            self.edit_latex_prompt = f.read()

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        with open("prompts/generate_latex_prompt.txt", "r") as f:
            self.generate_latex_prompt = f.read()
    
    def transcribe_audio(self, file_path):
        audio_file = open(file_path, "rb")

        transcription = self.client.audio.transcriptions.create(
            file=audio_file,
            model="gpt-4o-transcribe",
        )

        return transcription.text

    def generate_latex(self, text):
        model = "gpt-5.4-nano"
        input = [
            {"role": "system", "content": self.generate_latex_prompt},
            {"role": "user", "content": text}
        ]
        response = self.client.responses.create(
            model=model,
            input=input,
        )
        return response.output_text

    def edit_latex(self, current_latex, edit_description):
        prompt = self.edit_latex_prompt
        prompt = prompt.replace("[CURRENT_CODE]", current_latex)
        prompt = prompt.replace("[EDIT_DESCRIPTION]", edit_description)
        
        model = "gpt-5.4-nano"
        input = [
            {"role": "system", "content": prompt},
        ]
        response = self.client.responses.create(
            model=model,
            input=input,
        )
        return response.output_text