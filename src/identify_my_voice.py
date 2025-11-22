import os
import torch
import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier

# -----------------------------------------------
# Load your enrolled voice embedding (your voice print)
# -----------------------------------------------
enroll_embedding = torch.load("recordings/enroll_embedding/enroll_embedding.pt")

# -----------------------------------------------
# Load SpeechBrain ECAPA pretrained speaker encoder
# -----------------------------------------------
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa"
)

# -----------------------------------------------
# Directory where SepFormer saved separated voices
# -----------------------------------------------
separated_dir = "recordings/filtered_output"

# Get all separated WAV files
files = [f for f in os.listdir(separated_dir) if f.endswith(".wav")]

best_score = -1
best_file = None

cos = torch.nn.CosineSimilarity(dim=-1)

print("\n🔍 Checking separated files...\n")

for f in files:
    filepath = os.path.join(separated_dir, f)

    # Load separated audio file
    signal, fs = torchaudio.load(filepath)

    # Convert to mono if stereo
    if signal.shape[0] > 1:
        signal = signal.mean(dim=0, keepdim=True)

    # Resample to 16 kHz
    if fs != 16000:
        signal = torchaudio.functional.resample(signal, fs, 16000)

    signal = signal.unsqueeze(0)  # Add batch dimension

    # Extract embedding from model
    with torch.no_grad():
        test_embedding = classifier.encode_batch(signal)

    # Compare with your voice print
    score = cos(enroll_embedding, test_embedding).item()

    print(f"{f} → similarity score = {score:.4f}")

    # Track best match
    if score > best_score:
        best_score = score
        best_file = filepath


print("\n=====================================")
print(f"🥇 Best match for YOUR voice: {os.path.basename(best_file)}")
print(f"🔢 Highest similarity score = {best_score:.4f}")
print("=====================================\n")

print("➡ You can now use this file as your CLEAN filtered voice!")
