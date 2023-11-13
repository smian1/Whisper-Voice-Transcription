# Whisper Voice Transcription Tool

This Python script offers a convenient way to record audio through the microphone and transcribe it using OpenAI's powerful API. The transcription is automatically copied to the clipboard and pasted into the currently active window, making it ideal for quickly capturing and transcribing spoken words.

## Features
- Audio recording with a simple keyboard shortcut.
- Transcription of recorded audio using OpenAI's API.
- Automatic pasting of the transcribed text into any text input field.
- Easy to use with minimal setup required.

## Prerequisites
Before running the script, ensure you have the following:
- Python 3.x installed on your system.
- An OpenAI API key (sign up at [OpenAI](https://openai.com/) to obtain one).

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/smian1/Whisper-Voice-Transcription.git

2. Navigate to the cloned directory:
   ```bash
   cd Whisper-Voice-Transcription
3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt

## Usage
1. Run the script:
   ```bash
   python voice_transcription.py

2. Start recording by pressing Ctrl+R. Speak into your microphone.
3. Stop recording by pressing Ctrl+R again. The script will transcribe the audio and paste the transcription into the current active window.

## API Key Configuration
Place your OpenAI API key in a file named openai_api_key.txt in the same directory as the script.

## Contributing
   Contributions to this project are welcome! Please feel free to fork the repository, make improvements, and submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- OpenAI for providing the powerful transcription API.

## Running in a Virtual Environment (Optional)
Using a virtual environment is recommended as it keeps dependencies required by different projects separate. Here's how you can set up and use a virtual environment for this script:


1. Install Virtualenv (if not already installed):

   ```bash
   pip install virtualenv

2. Create a Virtual Environment:
Navigate to the project directory and run:

   ```bash
   virtualenv venv
This command creates a new directory named venv in your project directory, which contains the virtual environment.

3. Activate the Virtual Environment:

- On macOS and Linux:
   ```bash
   source venv/bin/activate

- On Windows:
   ```bash
   .\venv\Scripts\activate

4. Install Dependencies:
With the virtual environment activated, install the project dependencies:

   ```bash
   pip install -r requirements.txt
5. Run the Script:
Still in the virtual environment, you can now run the script:

   ```bash
   python voice_transcription.py
   
6. Deactivate the Virtual Environment:
Once you're done, you can deactivate the virtual environment by running:

   ```bash
   deactivate

Using a virtual environment ensures that your project's dependencies are isolated and do not interfere with other Python projects.
