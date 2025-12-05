import os
import torch
import torchaudio

from .model_loader import separator, encoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "recordings", "step3_output")
EMB_PATH = os.path.join(BASE_DIR, "recordings/enroll_embedding/enroll_embedding.pt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

import sounddevice as sd

def record_mixture():
    mixture_path = os.path.join(OUTPUT_DIR, "mixture.wav")
    audio = sd.rec(int(SAMPLE_RATE * RECORD_SECONDS), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    torchaudio.save(mixture_path, torch.tensor(audio).transpose(0, 1), SAMPLE_RATE)
    return mixture_path


def separate_sources(mixture_path):
    est = separator.separate_file(mixture_path)

    batch, T, num_sources = est.shape
    out_paths = []

    for i in range(num_sources):
        wav_8k = est[0, :, i].unsqueeze(0)
        wav_16k = torchaudio.functional.resample(wav_8k, 8000, 16000)

        out_path = os.path.join(OUTPUT_DIR, f"speaker_{i}.wav")
        torchaudio.save(out_path, wav_16k, 16000)
        out_paths.append(out_path)

    return out_paths


def choose_best(out_paths):
    enroll_emb = torch.load(EMB_PATH).squeeze(0)
    cos = torch.nn.CosineSimilarity(dim=-1)

    best_score = -999
    best_file = None

    for path in out_paths:
        wav, fs = torchaudio.load(path)
        if fs != 16000:
            wav = torchaudio.functional.resample(wav, fs, 16000)
        wav = wav.mean(dim=0, keepdim=True)
        wav = wav.unsqueeze(0)

        emb = encoder.encode_batch(wav).squeeze(0)
        score = cos(enroll_emb, emb).item()

        if score > best_score:
            best_score = score
            best_file = path

    return best_file


def run_full_pipeline():
    mixture = record_mixture()
    separated = separate_sources(mixture)
    best = choose_best(separated)
    return best
