import tkinter as tk
from tkinter import ttk
import pyaudio
import threading
import time
import wave
from AudioManager import AudioManager
from OpenAIWrapper import transcribe_audio
import os


DARK_BG = "#1e1e1e"
START_RECORDING_TEXT = "Start Recording"
STOP_RECORDING_TEXT = "Stop Recording"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech To Latex Converter")
        self.root.geometry("900x600")
        self.root.configure(bg=DARK_BG)

        self.setup_style()
        self.create_widgets()
        self.configure_grid()

        self.audio_manager = AudioManager(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.audio_manager.on_closing)
    

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TFrame", background=DARK_BG)
        style.configure("TLabel", background=DARK_BG, foreground="white")
        style.configure("TButton", padding=10)

    def create_widgets(self):
        # Outer frame
        self.outer_frame = ttk.Frame(self.root, padding=10)
        self.outer_frame.grid(row=0, column=0, sticky="nsew")

        # Top display frames
        self.text_frame = tk.Frame(
            self.outer_frame,
            bg=DARK_BG,
            highlightbackground="white",
            highlightthickness=1
        )
        self.text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.image_frame = tk.Frame(
            self.outer_frame,
            bg=DARK_BG,
            highlightbackground="white",
            highlightthickness=1
        )
        self.image_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Labels centered inside frames
        self.text_label = ttk.Label(self.text_frame, text="Text Display")
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

        self.image_label = ttk.Label(self.image_frame, text="Image Display")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        self.button_frame = ttk.Frame(self.outer_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.recording_btn = ttk.Button(self.button_frame, text=START_RECORDING_TEXT, command=self.on_recording_btn)
        self.recording_btn.grid(row=0, column=0, padx=20)

    def configure_grid(self):
        # Root expands
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Outer frame expands
        self.outer_frame.grid_rowconfigure(0, weight=1)
        self.outer_frame.grid_rowconfigure(1, weight=0)

        self.outer_frame.grid_columnconfigure(0, weight=1)
        self.outer_frame.grid_columnconfigure(1, weight=1)

    def on_recording_btn(self):
        self.text_label.config(text="Button 1 clicked")
        self.toggle_recording()

    def toggle_recording(self):
        """Toggle between start and stop recording"""
        if not self.audio_manager.is_recording:
            self.audio_manager.start_recording()
            self.recording_btn.config(text=STOP_RECORDING_TEXT)
        else:
            filename = self.audio_manager.stop_recording()
            self.recording_btn.config(text=START_RECORDING_TEXT)

            # test transcription
            if filename:
                result = transcribe_audio(filename)
                self.text_label.config(text=result)
                # remove the audio file after transcription
                os.remove(filename)
            else:
                print("No audio file to transcribe")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

