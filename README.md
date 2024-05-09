# Text-to-Speech Application

## Description
This application is a simple GUI tool built with Tkinter for converting text to speech using Google Cloud's Text-to-Speech API. It allows users to input text, select various voice options, and generate an audio file from the text.

## Features
- Input text via a text field.
- Select output file name.
- Choose from available voices after selecting Google Cloud credentials.
- Select language code, gender, and audio encoding options.
- Generate an audio file in MP3, WAV, or OGG format.

## Requirements
- Python 3.x
- Tkinter
- google-cloud-texttospeech library

## Setup
1. Install Python and pip.
2. Install required packages
3. Set up Google Cloud credentials:
- Obtain a Google Cloud service account key.
- Save the key as a JSON file.
- Use the application to load the JSON file for authentication.

## Usage
1. Run the script (app.py)
2. Use the GUI to:
- Enter the text you want converted to speech.
- Select your Google Cloud JSON credentials file.
- Choose the desired voice and audio settings.
- Generate the audio file.

## Contributions
Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.