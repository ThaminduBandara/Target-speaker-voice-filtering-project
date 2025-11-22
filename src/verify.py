import torch
import torchaudio
import os
from speechbrain.inference import EncoderClassifier

# ----------------------------
# Paths
# ----------------------------
recordings_dir = os.path.join(os.path.dirname(__file__), "..", "recordings")
# enroll_embedding_path = os.path.join(recordings_dir, "enroll_embedding.pt")
enroll_embedding_path = os.path.join(recordings_dir, "enroll_embedding", "enroll_embedding.pt")
# test_audio_path = os.path.join(recordings_dir, "test_noisy.wav")
test_audio_path = os.path.join(recordings_dir, "test_noisy", "test_noisy.wav")


# ----------------------------
# Load SpeechBrain speaker encoder
# ----------------------------
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa"
)

# ----------------------------
# Load enrolled embedding
# ----------------------------
enroll_embedding = torch.load(enroll_embedding_path)

# ----------------------------
# Load and prepare test audio
# ----------------------------
signal, fs = torchaudio.load(test_audio_path)

# Convert to mono if needed
if signal.shape[0] > 1:
    signal = signal.mean(dim=0, keepdim=True)

# Resample to 16 kHz if needed
if fs != 16000:
    signal = torchaudio.functional.resample(signal, fs, 16000)
    fs = 16000

# Add batch dimension
signal = signal.unsqueeze(0)  # [1, 1, time]

# ----------------------------
# Normalize audio (pass sample rate!)
# ----------------------------
features = classifier.audio_normalizer(signal, fs)

# ----------------------------
# Extract embedding
# ----------------------------
with torch.no_grad():
    test_embedding = classifier.encode_batch(features)

# ----------------------------
# Cosine similarity
# ----------------------------
cos = torch.nn.CosineSimilarity(dim=-1)
score = cos(enroll_embedding, test_embedding).item()

print(f"🔍 Similarity score: {score:.4f}")

# ----------------------------
# Decision threshold
# ----------------------------
threshold = 0.7
if score >= threshold:
    print("✅ It's YOU THAMINDU! Voice verified.")
else:
    print("❌ Not your voice THAMINDU.")
