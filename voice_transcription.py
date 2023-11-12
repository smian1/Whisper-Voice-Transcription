"""
Whisper Voice Transcription
Author: Salman Mian
Created: 11/12/2023


Description:
This script records audio through the microphone, transcribes it using OpenAI's API,
and pastes the transcription into the current active window. It's designed to be controlled
through keyboard shortcuts, specifically using Ctrl+R to start and stop recording.
"""


import pyaudio
import wave
import threading
from pynput import keyboard
from openai import OpenAI  # Used for accessing OpenAI's transcription services
import pyperclip  # Handles copying text to the clipboard
import pyautogui  # Automates keyboard and mouse operations
import os
import datetime  # Used for timestamping events

# Path to the file containing the OpenAI API key
API_KEY_FILE = 'openai_api_key.txt'

def get_api_key():
    # Check if the API key file exists and read the API key from it
    if os.path.isfile(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"API key file not found in '{API_KEY_FILE}'.")

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FILE_NAME = "recording.wav"

# Variables to control the recording state
is_recording = False
recording_thread = None
ctrl_pressed = False

# Initialize the PyAudio object
audio = pyaudio.PyAudio()

def start_recording():
    """Starts the audio recording."""
    global is_recording
    is_recording = True
    print(f"{datetime.datetime.now()}: Recording started")

    # Open the audio stream and start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    # Record audio in chunks until recording is stopped
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()

    # Save the recorded audio to a WAV file
    wave_file = wave.open(FILE_NAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    # Transcribe the recorded audio
    transcribe_audio()

def transcribe_audio():
    """Transcribes the recorded audio and handles the clipboard and pasting."""
    global paste_done
    paste_done = False  # Reset the flag for each transcription
    print(f"{datetime.datetime.now()}: Transcription started")
    
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    # Open the recorded audio file and send it for transcription
    with open(FILE_NAME, "rb") as audio_file:
        transcript_response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    # Handle the transcription response
    if hasattr(transcript_response, 'text'):
        transcript = transcript_response.text
        print(transcript)
        pyperclip.copy(transcript)  # Copy the transcript to the clipboard
        print(f"{datetime.datetime.now()}: Transcription copied to clipboard.")
        
        # Paste the transcript if not already done
        if not paste_done:
            pyautogui.hotkey('command', 'v')  # Simulate Cmd+V to paste
            paste_done = True
            print(f"{datetime.datetime.now()}: Transcription pasted.")
    else:
        print("Transcription failed or the response format is not as expected.")

def stop_recording():
    """Stops the audio recording."""
    global is_recording
    is_recording = False
    print(f"{datetime.datetime.now()}: Recording stopped")

def toggle_recording():
    """Toggles the recording state."""
    global is_recording, recording_thread
    # Start or stop recording based on the current state
    if is_recording:
        stop_recording()
    else:
        recording_thread = threading.Thread(target=start_recording)
        recording_thread.daemon = True  # Run thread as a daemon
        recording_thread.start()

# Keyboard event handlers
def on_press(key):
    """Handles key press events."""
    global ctrl_pressed
    try:
        # Check if either Ctrl key is pressed
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = True
    except AttributeError:
        pass

def on_release(key):
    """Handles key release events."""
    global ctrl_pressed
    try:
        # Check for Ctrl+R key combination
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = False
        elif key.char == 'r' and ctrl_pressed:
            toggle_recording()
    except AttributeError:
        pass

def main():
    """Main function to set up the keyboard listener."""
    try:
        # Start the keyboard listener
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        # Handle script exit
        print("Exiting script...")
        stop_recording()

if __name__ == "__main__":
    main()
