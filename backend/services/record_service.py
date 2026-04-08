import os
import torch
import torchaudio
import sounddevice as sd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENROLL_DIR = os.path.join(BASE_DIR, "recordings", "my_voice_samples")
os.makedirs(ENROLL_DIR, exist_ok=True)

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

def record_enroll():
    out_path = os.path.join(ENROLL_DIR, "clean_voice.wav")

    print("🎤 Recording clean voice...")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    torchaudio.save(out_path, torch.tensor(audio).transpose(0, 1), SAMPLE_RATE)
    print(f"✅ Saved clean voice: {out_path}")

    return out_path



# import os
# import sounddevice as sd
# import soundfile as sf

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# VOICE_DIR = os.path.join(BASE_DIR, "recordings", "my_voice_samples")
# os.makedirs(VOICE_DIR, exist_ok=True)

# ENROLL_PATH = os.path.join(VOICE_DIR, "enroll.wav")
# SAMPLE_RATE = 16000
# DURATION = 5

# def record_enroll():
#     print("🎤 Recording enroll voice...")
#     audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
#     sd.wait()
#     sf.write(ENROLL_PATH, audio, SAMPLE_RATE)
#     print("✅ Saved:", ENROLL_PATH)
#     return ENROLL_PATH
