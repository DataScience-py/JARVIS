"""Speech to text convertor from microphokne for JARVIS."""

import json
import os
import wave

import pyaudio
import requests
import whisper

# Configuration for audio recording
config = {
    "FORMAT": pyaudio.paInt32,
    "CHANNELS": 1,
    "RATE": 16000,  # Sample rate for Whisper
    "CHUNK": 1024,
    "RECORD_SECONDS": 5,  # Adjust as needed
    "WAVE_OUTPUT_FILENAME": "temp_audio.wav",
    "SERVER": "http://127.0.0.1:9000",
    "MODEL": "base",
}


FILE_CONFIG = "stt_config.json"


def load_config() -> None:
    """
    load_config get config from file if file if not exists create new file.

    Use default setting if config is empty.

    Returns
    -------
    None
        Managment file
    """
    global config
    if not os.path.exists(FILE_CONFIG):
        with open(FILE_CONFIG, "w") as f:
            json.dump(config, f, indent=4)
    with open(FILE_CONFIG, "r") as f:
        temp_config = json.load(f)
        config = config if temp_config == {} else temp_config
    with open(FILE_CONFIG, "w") as f:
        json.dump(config, f, indent=4)


def record_audio(seconds: int = 5) -> None:
    """
    record_audio function records audio from the microphon.

    Parameters
    ----------
    seconds : int, optional
        times record audio, by default 5
    """
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=config["FORMAT"],
        channels=config["CHANNELS"],
        rate=config["RATE"],
        input=True,
        frames_per_buffer=config["CHUNK"],
    )

    print("Recording...")
    frames = []

    for _ in range(0, int(config["RATE"] / config["CHUNK"] * seconds)):
        data = stream.read(config["CHUNK"])
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(config["WAVE_OUTPUT_FILENAME"], "wb")
    wf.setnchannels(config["CHANNELS"])
    wf.setsampwidth(audio.get_sample_size(config["FORMAT"]))
    wf.setframerate(config["RATE"])
    wf.writeframes(b"".join(frames))
    wf.close()


def send_to_server(text: str) -> None:
    """
    send_to_server create post request to server.

    Parameters
    ----------
    text : str
        The text to be sent to the server.
    """
    print("Sending text to server...: ", text)
    requests.post(f"{config['SERVER']}/stt", json={"text": text})


load_config()


# Load the Whisper model
model = whisper.load_model(config["MODEL"])

while True:
    try:
        record_audio(seconds=config["RECORD_SECONDS"])
        result = model.transcribe(config["WAVE_OUTPUT_FILENAME"])
        send_to_server(result["text"])
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        if os.path.exists(config["WAVE_OUTPUT_FILENAME"]):
            os.remove(config["WAVE_OUTPUT_FILENAME"])
