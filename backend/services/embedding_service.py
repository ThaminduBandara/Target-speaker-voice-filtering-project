import os
import torch
import torchaudio

from backend.services.model_loader import encoder   # shared ECAPA model

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

VOICE_DIR = os.path.join(BASE_DIR, "recordings", "my_voice_samples")
EMB_DIR = os.path.join(BASE_DIR, "recordings", "enroll_embedding")

os.makedirs(EMB_DIR, exist_ok=True)

# Must match record_service.py output file name
ENROLL_WAV = os.path.join(VOICE_DIR, "clean_voice.wav")
EMB_PATH = os.path.join(EMB_DIR, "enroll_embedding.pt")


# ------------------------------------------------------------
# EXTRACT EMBEDDING
# ------------------------------------------------------------
def extract_embedding():
    # Load WAV
    wav, fs = torchaudio.load(ENROLL_WAV)

    # Convert stereo → mono
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)

    # Resample → 16 kHz (ECAPA requirement)
    if fs != 16000:
        wav = torchaudio.functional.resample(wav, fs, 16000)

    # Shape → [batch, time]
    wav = wav.unsqueeze(0)

    # REQUIRED preprocessing for ECAPA
    feats = encoder.audio_normalizer(wav, 16000)

    with torch.no_grad():
        emb = encoder.encode_batch(feats)

    # Save embedding
    torch.save(emb, EMB_PATH)

    print(f"🔑 Embedding saved at: {EMB_PATH}")
    return EMB_PATH


