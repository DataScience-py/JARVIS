"""Speech to text convertor from microphokne for JARVIS."""

import json
import os
import threading
import time
import wave

import pyaudio
import requests
import whisper

# Configuration for audio recording
config = {
    "FORMAT": pyaudio.paInt32,
    "CHANNELS": 1,
    "RATE": 16000,
    "CHUNK": 1024,
    "RECORD_SECONDS": 5,
    "SERVER": "http://127.0.0.1:9000",
    "MODEL": "base",
}

FILE_CONFIG = "stt_config.json"

# --- Shared resources for threading ---
# Use a lock to protect access to the shared file name
file_lock = threading.Lock()
# Variable to hold the name of the new audio file
new_audio_file = ""


def load_config() -> None:
    """Load_config."""
    global config
    if not os.path.exists(FILE_CONFIG):
        with open(FILE_CONFIG, "w") as f:
            json.dump(config, f, indent=4)
    with open(FILE_CONFIG, "r") as f:
        temp_config = json.load(f)
        config = temp_config if temp_config else config


def record_audio_thread() -> None:
    """record_audio_thread."""
    global new_audio_file
    p = pyaudio.PyAudio()

    stream = p.open(
        format=config["FORMAT"],
        channels=config["CHANNELS"],
        rate=config["RATE"],
        input=True,
        frames_per_buffer=config["CHUNK"],
    )
    print("Recording thread started.")

    try:
        while True:
            frames = []
            for _ in range(
                0,
                int(
                    config["RATE"] / config["CHUNK"] * config["RECORD_SECONDS"]
                ),
            ):
                data = stream.read(config["CHUNK"])
                frames.append(data)

            # Create a unique file name based on the current timestamp
            current_time = int(time.time())
            filename = f"audio_{current_time}.wav"

            # Use the lock to safely update the shared variable
            with file_lock:
                # Remove the previous file if it exists
                if new_audio_file and os.path.exists(new_audio_file):
                    os.remove(new_audio_file)
                new_audio_file = filename

            wf = wave.open(filename, "wb")
            wf.setnchannels(config["CHANNELS"])
            wf.setsampwidth(p.get_sample_size(config["FORMAT"]))
            wf.setframerate(config["RATE"])
            wf.writeframes(b"".join(frames))
            wf.close()
            print(f"Recorded and saved: {filename}")

    except Exception as e:
        print(f"Recording error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def transcribe_audio_thread() -> None:
    """Thread function to transcribe and send audio."""
    global new_audio_file
    load_config()
    model = whisper.load_model(config["MODEL"])
    print("Transcription thread started.")

    last_processed_file = ""

    while True:
        current_file_to_process = ""
        # Use the lock to get a consistent state of the shared variable
        with file_lock:
            current_file_to_process = new_audio_file

        # Check if the file has changed since the last check
        if (
            current_file_to_process
            and current_file_to_process != last_processed_file
        ):
            try:
                print(f"Transcribing: {current_file_to_process}")
                result = model.transcribe(current_file_to_process)
                send_to_server(result["text"])
            except Exception as e:
                print(f"Transcription error: {e}")
            finally:
                last_processed_file = current_file_to_process
        else:
            # If no new file, wait a bit before checking again
            time.sleep(0.5)


def send_to_server(text: str) -> None:
    """Send transcribed text to the server."""
    print("Sending text to server: ", text)
    try:
        requests.post(
            f"{config['SERVER']}/stt/text?text={text}",
        )
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}. Is the server running?")


# --- Main execution ---
if __name__ == "__main__":
    load_config()

    # Create and start the recording and transcription threads
    record_thread = threading.Thread(target=record_audio_thread, daemon=True)
    transcribe_thread = threading.Thread(
        target=transcribe_audio_thread, daemon=True
    )

    record_thread.start()
    transcribe_thread.start()

    # Keep the main thread alive so the daemon threads can run
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
