import os
import torch
import torchaudio
import sounddevice as sd

from backend.services.model_loader import separator, encoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "recordings/step3_output")
EMB_PATH = os.path.join(BASE_DIR, "recordings/enroll_embedding/enroll_embedding.pt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


def record_mixture():
    out = os.path.join(OUTPUT_DIR, "mixture.wav")
    print("🎤 Recording mixture...")
    audio = sd.rec(int(SAMPLE_RATE * RECORD_SECONDS), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    torchaudio.save(out, torch.tensor(audio).transpose(0, 1), SAMPLE_RATE)
    return out


# ⭐ Fade replacement: compatible everywhere
def apply_fade(wav, length=200):
    wav = wav.clone()
    ramp = torch.linspace(0.0, 1.0, length)

    wav[:, :length] *= ramp          # fade-in
    wav[:, -length:] *= torch.flip(ramp, dims=[0])  # fade-out

    return wav


def enhance_audio(wav_8k):
    # Smooth the edges (click removal)
    wav_8k = apply_fade(wav_8k, length=200)

    # Light denoise — reduce metallic noise
    wav_8k = torchaudio.functional.lowpass_biquad(
        wav_8k, sample_rate=8000, cutoff_freq=3600
    )

    # High-quality upsampling
    wav_16k = torchaudio.functional.resample(
        wav_8k, orig_freq=8000, new_freq=16000, lowpass_filter_width=6
    )

    return wav_16k


def separate_sources(mix_path):
    est = separator.separate_file(mix_path)
    batch, T, num_src = est.shape

    out_paths = []
    for i in range(num_src):
        wav_8k = est[0, :, i].unsqueeze(0)
        wav_16k = enhance_audio(wav_8k)

        out_path = os.path.join(OUTPUT_DIR, f"speaker_{i}.wav")
        torchaudio.save(out_path, wav_16k, 16000)
        out_paths.append(out_path)

    return out_paths


def compute_embedding(path):
    wav, fs = torchaudio.load(path)
    if fs != 16000:
        wav = torchaudio.functional.resample(wav, fs, 16000)
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)
    feats = encoder.audio_normalizer(wav.unsqueeze(0), 16000)
    with torch.no_grad():
        emb = encoder.encode_batch(feats)
    return emb.squeeze(0)


def choose_best(paths):
    enroll_emb = torch.load(EMB_PATH).squeeze(0)
    cos = torch.nn.CosineSimilarity(dim=-1)
    best_file = max(paths, key=lambda p: cos(enroll_emb, compute_embedding(p)).item())
    print(f"🎯 Best speaker: {best_file}")
    return best_file


def run_full_pipeline():
    mixture = record_mixture()
    separated = separate_sources(mixture)
    best = choose_best(separated)

    return {
        "mixture": os.path.basename(mixture),
        "cleaned": os.path.basename(best)
    }


# import os
# import torch
# import torchaudio
# import sounddevice as sd

# from backend.services.model_loader import separator, encoder

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# OUTPUT_DIR = os.path.join(BASE_DIR, "recordings/step3_output")
# EMB_PATH = os.path.join(BASE_DIR, "recordings/enroll_embedding/enroll_embedding.pt")

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# SAMPLE_RATE = 16000
# RECORD_SECONDS = 5

# def record_mixture():
#     out = os.path.join(OUTPUT_DIR, "mixture.wav")

#     print("🎤 Recording mixture...")
#     audio = sd.rec(int(SAMPLE_RATE * RECORD_SECONDS), samplerate=SAMPLE_RATE, channels=1)
#     sd.wait()

#     torchaudio.save(out, torch.tensor(audio).transpose(0, 1), SAMPLE_RATE)
#     return out


# def separate_sources(mix_path):
#     est = separator.separate_file(mix_path)
#     batch, T, num_src = est.shape

#     out_paths = []
#     for i in range(num_src):
#         wav_8k = est[0, :, i].unsqueeze(0)
#         wav_16k = torchaudio.functional.resample(wav_8k, 8000, 16000)

#         out_path = os.path.join(OUTPUT_DIR, f"speaker_{i}.wav")
#         torchaudio.save(out_path, wav_16k, 16000)

#         out_paths.append(out_path)

#     return out_paths


# def compute_embedding(path):
#     wav, fs = torchaudio.load(path)

#     if fs != 16000:
#         wav = torchaudio.functional.resample(wav, fs, 16000)

#     if wav.shape[0] > 1:
#         wav = wav.mean(dim=0, keepdim=True)

#     wav = wav.unsqueeze(0)

#     feats = encoder.audio_normalizer(wav, 16000)

#     with torch.no_grad():
#         emb = encoder.encode_batch(feats)

#     return emb.squeeze(0)


# def choose_best(paths):
#     print("🔍 Choosing best matching speaker...")
#     enroll_emb = torch.load(EMB_PATH).squeeze(0)
#     cos = torch.nn.CosineSimilarity(dim=-1)

#     best_score = -999
#     best_file = None

#     for path in paths:
#         emb = compute_embedding(path)
#         score = cos(enroll_emb, emb).item()

#         if score > best_score:
#             best_score = score
#             best_file = path

#     print(f"✅ Best speaker: {best_file}")
#     return best_file


# def run_full_pipeline():
#     # Step 1: Record mixture
#     mixture = record_mixture()

#     # Step 2: Separate speakers
#     separated = separate_sources(mixture)

#     # Step 3: Best speaker
#     best = choose_best(separated)

#     # Return BOTH audio files

#     # return {
#     #     "mixture": mixture,
#     #     "cleaned": best
#     # }
#     return {
#     "mixture": os.path.basename(mixture),
#     "cleaned": os.path.basename(best)
# }




