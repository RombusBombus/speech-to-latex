import pyaudio
import wave
import threading
import time


class AudioManager:

    def __init__(self, root):
        self.root = root

        # Audio recording parameters
        self.audio_format = pyaudio.paInt16
        self.channels = 1  # Mono
        self.rate = 44100  # Sample rate (Hz)
        self.chunk = 1024  # Buffer size
        self.frames = []

        # Recording state
        self.is_recording = False
        self.audio = None
        self.stream = None
        self.record_thread = None

        # Initialize PyAudio
        self.init_audio()

    def init_audio(self):
        """Initialize PyAudio instance"""
        try:
            self.audio = pyaudio.PyAudio()
        except Exception as e:
            print("Error", f"Could not initialize audio: {e}")
            self.root.quit()
    
    def record_audio(self):
        """Record audio in a loop until stopped"""
        print("Recording started...")
        
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
            except Exception as e:
                print(f"Error during recording: {e}")
                break
        
        print("Recording stopped")

    def save_audio(self, filename):
        """Save recorded frames to a WAV file"""
        try:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print(f"Audio saved to {filename}")
        except Exception as e:
            print("Error", f"Could not save audio: {e}")
    

    def start_recording(self):
        """Start recording audio"""
        try:
            print("Starting recording...")
            self.frames = []
            self.is_recording = True
            
            # Open audio stream
            self.stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=None  # Use blocking mode for simplicity
            )
            
            # Start recording in a separate thread
            self.record_thread = threading.Thread(target=self.record_audio)
            self.record_thread.daemon = True
            self.record_thread.start()
            
        except Exception as e:
            print("Error", f"Could not start recording: {e}")
            self.is_recording = False
    
    def stop_recording(self):
        """Stop recording and save the audio file, returns the filename of the saved audio"""
        print("Stopping recording...")
        self.is_recording = False
        
        # Wait for recording thread to finish
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.join(timeout=1.0)
        
        # Close stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        # Save the recorded audio to a file
        if self.frames:
            filename = f"recording_{int(time.time())}.wav"
            self.save_audio(filename)
            print(f"Status: Saved to {filename}")
            return filename
        else:
            print("Status: No audio recorded")
            return None

    def on_closing(self):
        """Clean up resources when closing the app"""
        if self.is_recording:
            self.stop_recording()
        
        if self.audio:
            self.audio.terminate()
        
        self.root.destroy()