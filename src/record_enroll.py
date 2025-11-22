import sounddevice as sd
import soundfile as sf
import os

# ----------------------------
# Paths
# ----------------------------
project_root = os.path.dirname(os.path.dirname(__file__))  # Go up one level from src/
recordings_dir = os.path.join(project_root, "recordings", "my_voice_samples")  # Subfolder for samples
os.makedirs(recordings_dir, exist_ok=True)

enroll_filename = os.path.join(recordings_dir, "enroll30.wav")

# ----------------------------
# Recording settings
# ----------------------------
samplerate = 16000  # 16 kHz
duration = 5        # seconds

# ----------------------------
# Record audio
# ----------------------------
print("🎤 Speak now to enroll your voice...")
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
sd.wait()  # Wait until recording is finished

# Save recording
sf.write(enroll_filename, audio, samplerate)
print(f"✅ Enrollment recording saved: {enroll_filename}")
