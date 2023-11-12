# Voice Transcription Tool

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
   git clone https://github.com/[YourGitHubUsername]/Voice-Transcription-Tool.git

2. Navigate to the cloned directory:
   ```bash
   cd Voice-Transcription-Tool
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
