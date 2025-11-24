import torch
from speechbrain.inference import EncoderClassifier
from src.utils import load_audio
import os
import torchaudio

# Initialize SpeechBrain model
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa"
)

# Path to enrollment audio
enroll_path = "recordings/my_voice_samples/enroll1.wav"

# Load audio
signal, fs = load_audio(enroll_path)

# Convert to mono if needed
if signal.shape[0] > 1:
    signal = signal.mean(dim=0, keepdim=True)

# Resample to 16kHz if needed
if fs != 16000:
    signal = torchaudio.functional.resample(signal, fs, 16000)

#  Fix: shape should be [batch, time]
signal = signal.squeeze(0).unsqueeze(0)

# Extract embedding
embeddings = classifier.encode_batch(signal)

# Save embedding as voice print
os.makedirs("recordings", exist_ok=True)
torch.save(embeddings, "recordings/enroll_embedding.pt")

print(" Enrollment complete. Voice print saved as enroll_embedding.pt")




# import torch
# from speechbrain.inference import EncoderClassifier
# from src.utils import load_audio
# import torchaudio
# import os

# # ----------------------------
# # Initialize SpeechBrain model
# # ----------------------------
# classifier = EncoderClassifier.from_hparams(
#     source="speechbrain/spkrec-ecapa-voxceleb",
#     savedir="pretrained_models/spkrec-ecapa"
# )

# # ----------------------------
# # Paths
# # ----------------------------
# recordings_dir = "recordings/my_voice_samples"  # your 30 recordings
# embedding_dir = "recordings/enroll_embedding"   # new folder to save output
# embedding_path = os.path.join(embedding_dir, "enroll_embedding.pt")

# # Create folders if not exist
# os.makedirs(recordings_dir, exist_ok=True)
# os.makedirs(embedding_dir, exist_ok=True)

# # ----------------------------
# # Prepare embeddings list
# # ----------------------------
# embeddings = []

# # Loop through your 30 voice samples
# for i in range(1, 31):
#     file_path = os.path.join(recordings_dir, f"enroll{i}.wav")

#     if not os.path.exists(file_path):
#         print(f"⚠️ File not found: {file_path}")
#         continue

#     signal, fs = load_audio(file_path)

#     # Convert to mono if stereo
#     if signal.shape[0] > 1:
#         signal = signal.mean(dim=0, keepdim=True)

#     # Resample to 16kHz if required
#     if fs != 16000:
#         signal = torchaudio.functional.resample(signal, fs, 16000)

#     # Shape: [batch, time]
#     signal = signal.squeeze(0).unsqueeze(0)

#     # Extract embedding
#     emb = classifier.encode_batch(signal)
#     embeddings.append(emb)

# # ----------------------------
# # Average and save embedding
# # ----------------------------
# if len(embeddings) > 0:
#     enroll_embedding = torch.mean(torch.stack(embeddings), dim=0)
#     torch.save(enroll_embedding, embedding_path)
#     print(f" Enrollment complete! Voice print saved at: {embedding_path}")
# else:
#     print(" No embeddings were created. Please check your files.")


