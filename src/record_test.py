# import sounddevice as sd
# import soundfile as sf
# import os

# # Directory for recordings
# save_dir = "recordings"
# os.makedirs(save_dir, exist_ok=True)

# filename = os.path.join(save_dir, "test_noisy.wav")

# samplerate = 16000
# duration = 5  # seconds

# print("🎤 Speak now (with some background noise)...")
# audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
# sd.wait()
# sf.write(filename, audio, samplerate)
# print("✅ Test recording saved:", filename)

import sounddevice as sd
import soundfile as sf
import os

# Directory for recordings
# We use os.path.join to create the nested path 'recordings/test_noisy'
save_dir = os.path.join("recordings", "test_noisy")
os.makedirs(save_dir, exist_ok=True)

# The filename will now be inside the 'save_dir'
filename = os.path.join(save_dir, "test_noisy.wav")

samplerate = 16000
duration = 5  # seconds

print(f"🎤 Speak now (saving to {filename})...")
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
sd.wait()
sf.write(filename, audio, samplerate)
print("✅ Test recording saved:", filename)
