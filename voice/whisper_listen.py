import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from config import (
    SAMPLE_RATE,
    BLOCK_SIZE,
    START_THRESHOLD,
    SILENCE_THRESHOLD,
    SILENCE_DURATION,
    MAX_DURATION,
)

print("Loading Whisper model...")
_whisper_model = None


def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = WhisperModel("base", compute_type="int8")
        print("Whisper model ready.")
    return _whisper_model


def listen():
    model = get_whisper_model()
    print("🎤 Listening...")

    silence_blocks = 0
    speech_started = False
    recording = []

    max_blocks = int(MAX_DURATION * SAMPLE_RATE / BLOCK_SIZE)
    silence_limit = int(SILENCE_DURATION * SAMPLE_RATE / BLOCK_SIZE)

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=BLOCK_SIZE,
        ) as stream:
            for _ in range(max_blocks):
                chunk, overflowed = stream.read(BLOCK_SIZE)
                chunk = chunk[:, 0]
                rms = float(np.sqrt(np.mean(chunk * chunk)))

                if rms >= START_THRESHOLD:
                    speech_started = True
                    silence_blocks = 0
                    recording.append(chunk.copy())
                    continue

                if speech_started:
                    recording.append(chunk.copy())
                    silence_blocks += 1
                    if silence_blocks >= silence_limit and len(recording) > 0:
                        break
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return ""

    if not speech_started or not recording:
        print("No speech detected.")
        return ""

    audio = np.concatenate(recording).astype(np.float32)

    try:
        segments, _ = model.transcribe(
            audio,
            language="en",
            vad_filter=True,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip().lower()
    except Exception as e:
        print(f"❌ Whisper transcription error: {e}")
        return ""

    if text:
        print(f"You said: {text}")
    else:
        print("No speech detected.")

    return text