"""
Whisper Voice Transcription
Author: Salman Mian
Created: 11/12/2023


Description:
This script records audio through the microphone, transcribes it using OpenAI's API,
and pastes the transcription into the current active window. It's designed to be controlled
through keyboard shortcuts, specifically using Ctrl+R to start and stop recording.
"""


#using API key file
import pyaudio
import wave
import threading
from pynput import keyboard
from openai import OpenAI  # Importing OpenAI for transcription
import pyperclip  # Import pyperclip
import pyautogui  # allows you to programmatically control the mouse and keyboard.
import os
#import datetime  # Used for timestamping events

# Define the path to the API key file
API_KEY_FILE = 'openai_api_key.txt'

def get_api_key():
    # Check if the API key file exists in the current directory
    if os.path.isfile(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as file:
            api_key = file.read().strip()
            #print(f"API Key: {api_key}")  # Temporary print statement for debugging
            return api_key
    else:
        raise FileNotFoundError(f"API key file not found in the current directory. Please create a file named '{API_KEY_FILE}' with your OpenAI API key.")


# Set the recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FILE_NAME = "recording.wav"

# Global variables to control recording state
is_recording = False
recording_thread = None
ctrl_pressed = False  # To track the state of Ctrl key

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Function to start recording
def start_recording():
    global paste_done
    paste_done = False  # Reset the flag when starting a new recording
    global is_recording
    is_recording = True
    print("Recording started")

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Save the recording
    wave_file = wave.open(FILE_NAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    # After recording, transcribe the audio
    transcribe_audio()

def transcribe_audio():
    print("Transcribe audio called")  # Debug print
    global paste_done
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)
    with open(FILE_NAME, "rb") as audio_file:
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    
    if hasattr(transcript_response, 'text'):
        transcript = transcript_response.text
        print(transcript)
        pyperclip.copy(transcript)  # Copy to clipboard
        print("Transcription copied to clipboard.")
        if not paste_done:  # Check if paste hasn't been done yet
            #print("Clipboard content before paste:", pyperclip.paste())  # Debug print
            pyautogui.hotkey('command', 'v')  # Simulate Cmd+V to paste
            paste_done = True  # Set the flag to True after pasting
    else:
        print("Transcription failed or the response format is not as expected.")

# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False
    print("Recording stopped")

# Toggle recording state
def toggle_recording():
    global is_recording, recording_thread
    #print(f"Active Threads before toggling: {threading.active_count()}")  # New line
    
    if is_recording:
        stop_recording()
    else:
        recording_thread = threading.Thread(target=start_recording)
        recording_thread.daemon = True  # Set thread as daemon
        recording_thread.start()

# Listener for keyboard events
def on_press(key):
    global ctrl_pressed
    try:
        if key == keyboard.Key.ctrl:
            ctrl_pressed = True
            #print("Ctrl pressed")  # Debug print
        elif key.char == 'r' and ctrl_pressed:
            print("Ctrl+R pressed")  # Debug print
            toggle_recording()
    except AttributeError:
        pass

def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl:
        ctrl_pressed = False
        #print("Ctrl released")  # Debug print


# Main function
def main():
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("Exiting script...")
        stop_recording()

if __name__ == "__main__":
    main()
