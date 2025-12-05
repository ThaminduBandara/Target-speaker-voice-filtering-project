import os
import sounddevice as sd
import soundfile as sf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
VOICE_DIR = os.path.join(BASE_DIR, "recordings", "my_voice_samples")
os.makedirs(VOICE_DIR, exist_ok=True)

ENROLL_PATH = os.path.join(VOICE_DIR, "enroll.wav")
SAMPLE_RATE = 16000
DURATION = 5

def record_enroll():
    print("🎤 Recording enroll voice...")
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    sf.write(ENROLL_PATH, audio, SAMPLE_RATE)
    print("✅ Saved:", ENROLL_PATH)
    return ENROLL_PATH
