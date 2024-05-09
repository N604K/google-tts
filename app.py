import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from google.cloud import texttospeech
from google.auth.exceptions import DefaultCredentialsError

class TextToSpeechApp:
    def __init__(self, root):
        """Initializes the application, sets up the main window and default values for various options, and calls the `create_widgets()` method to create the GUI components."""
        self.root = root
        self.root.title("Text-to-Speech App")

        self.json_file = ""
        self.text = tk.StringVar()
        self.output_file = tk.StringVar()
        self.language_code = tk.StringVar(value='en-US')
        self.voice_name = tk.StringVar()
        self.ssml_gender = tk.StringVar(value='FEMALE')
        self.audio_encoding = tk.StringVar(value='MP3')

        self.voice_options = []
        self.create_widgets()

    def create_widgets(self):
        """Sets up the GUI components including labels, entries, buttons, and comboboxes for user interaction. It also configures the grid layout and handles widget resizing."""
        tk.Label(self.root, text="Text:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text).grid(row=0, column=1, columnspan=3, sticky="we")

        tk.Label(self.root, text="Output File:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.output_file).grid(row=1, column=1, columnspan=3, sticky="we")

        tk.Button(self.root, text="Select Credentials File", command=self.select_json_file).grid(row=2, column=0, columnspan=4, sticky="we")

        tk.Label(self.root, text="Voice Options:").grid(row=3, column=0, columnspan=4, sticky="we")

        tk.Label(self.root, text="Voice Name:").grid(row=4, column=0, sticky="e")
        self.voice_combobox = ttk.Combobox(self.root, textvariable=self.voice_name, values=[v[0] for v in self.voice_options])
        self.voice_combobox.grid(row=4, column=1, sticky="we")

        tk.Label(self.root, text="Language Code:").grid(row=5, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.language_code).grid(row=5, column=1, sticky="we")

        tk.Label(self.root, text="Gender:").grid(row=5, column=2, sticky="e")
        ttk.Combobox(self.root, textvariable=self.ssml_gender, values=["FEMALE", "MALE", "NEUTRAL"]).grid(row=5, column=3, sticky="we")

        tk.Label(self.root, text="Audio Encoding:").grid(row=6, column=0, sticky="e")
        ttk.Combobox(self.root, textvariable=self.audio_encoding, values=["MP3", "LINEAR16", "OGG_OPUS"]).grid(row=6, column=1, sticky="we")

        tk.Button(self.root, text="Generate", command=self.generate_speech).grid(row=7, column=0, columnspan=4, sticky="we")

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def select_json_file(self):
        """Opens a file dialog for the user to select a Google Cloud credentials JSON file. Sets the selected file as the environment variable required for Google Cloud API authentication and updates the voice options based on the selected credentials."""
        file = filedialog.askopenfilename(title="Select Google Credentials JSON File", filetypes=[("JSON files", "*.json")])
        if file:
            self.json_file = file
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file
            try:
                self.voice_options = self.get_voices()
                self.voice_combobox['values'] = [v[0] for v in self.voice_options]
                messagebox.showinfo("File Selected", f"Selected file: {file}")
            except DefaultCredentialsError:
                messagebox.showerror("Error", "Invalid credentials file. Please select a valid JSON file.")

    def get_voices(self):
        """Fetch the available voices from Google Cloud Text-to-Speech API."""
        client = texttospeech.TextToSpeechClient()
        voices = client.list_voices().voices
        voice_options = [(voice.name, voice.language_codes[0], texttospeech.SsmlVoiceGender(voice.ssml_gender).name)
                         for voice in voices]
        return voice_options

    def generate_speech(self):
        """Generates speech from the input text using the selected voice and audio settings. Saves the output to a file with the appropriate audio encoding extension."""
        if not self.json_file:
            messagebox.showwarning("No JSON File", "Please select a JSON credentials file.")
            return

        # Determine file extension based on audio encoding
        extension_map = {
            "MP3": ".mp3",
            "LINEAR16": ".wav",
            "OGG_OPUS": ".ogg"
        }
        extension = extension_map.get(self.audio_encoding.get(), ".mp3")

        output_file_with_extension = self.output_file.get()
        if not output_file_with_extension.endswith(extension):
            output_file_with_extension += extension

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.json_file

        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.SynthesisInput(text=self.text.get())

        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code.get(),
            name=self.voice_name.get(),
            ssml_gender=texttospeech.SsmlVoiceGender[self.ssml_gender.get()]
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding[self.audio_encoding.get()]
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        with open(output_file_with_extension, 'wb') as out:
            out.write(response.audio_content)

        messagebox.showinfo("Success", f"Generated file: {output_file_with_extension}")

def main():
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
