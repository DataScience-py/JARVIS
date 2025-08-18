"""Speech to text convertor from microphokne for JARVIS."""

import os
import wave

import pyaudio
import whisper

# Configuration for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Sample rate for Whisper
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust as needed
WAVE_OUTPUT_FILENAME = "temp_audio.wav"

# Load the Whisper model
model = whisper.load_model("base")


def record_audio() -> None:
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream for recording
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


while True:
    # Transcribe the audio using Whisper
    try:
        record_audio()
        result = model.transcribe(WAVE_OUTPUT_FILENAME)
        print("Transcription:", result["text"])
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            os.remove(WAVE_OUTPUT_FILENAME)
