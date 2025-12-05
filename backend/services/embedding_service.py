import os
import torch
import torchaudio
from src.utils import load_audio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

VOICE_DIR = os.path.join(BASE_DIR, "recordings", "my_voice_samples")
EMB_DIR = os.path.join(BASE_DIR, "recordings", "enroll_embedding")

os.makedirs(EMB_DIR, exist_ok=True)

ENROLL_WAV = os.path.join(VOICE_DIR, "enroll.wav")
EMB_PATH = os.path.join(EMB_DIR, "enroll_embedding.pt")

from .model_loader import encoder   # use shared model

def extract_embedding():
    signal, fs = load_audio(ENROLL_WAV)

    if signal.shape[0] > 1:
        signal = signal.mean(dim=0, keepdim=True)

    if fs != 16000:
        signal = torchaudio.functional.resample(signal, fs, 16000)

    signal = signal.squeeze(0).unsqueeze(0)

    emb = encoder.encode_batch(signal)
    torch.save(emb, EMB_PATH)

    print("✅ Embedding saved:", EMB_PATH)
    return EMB_PATH
