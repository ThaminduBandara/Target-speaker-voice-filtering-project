import os
import torch
import torchaudio
import sounddevice as sd
from datetime import datetime
from speechbrain.inference.separation import SepformerSeparation
from speechbrain.inference import EncoderClassifier

# ============================================================
# CONFIG
# ============================================================
SAMPLE_RATE = 16000     # Recording sample rate (ECAPA works at 16k)
RECORD_SECONDS = 5       # Length of mixture recording

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "recordings")
ENROLL_EMBED_PATH = os.path.join(BASE_DIR, "enroll_embedding", "enroll_embedding.pt")

OUTPUT_DIR = os.path.join(BASE_DIR, "step3_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# STEP 1 — RECORD MIXTURE
# ============================================================
def record_mixture(output_path):
    print("🎤 Recording mixture... Speak now!")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    torchaudio.save(output_path, torch.tensor(audio).transpose(0, 1), SAMPLE_RATE)
    print(f"✅ Recorded mixture saved: {output_path}")

# ============================================================
# STEP 2 — LOAD MODELS
# ============================================================
print("🧠 Loading SepFormer model...")
separator = SepformerSeparation.from_hparams(
    source="speechbrain/sepformer-whamr",
    savedir="pretrained_models/sepformer-whamr"
)

print("🧠 Loading ECAPA speaker encoder...")
encoder = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa"
)

# ============================================================
# STEP 3 — LOAD ENROLLED EMBEDDING
# ============================================================
enroll_embedding = torch.load(ENROLL_EMBED_PATH).squeeze(0)

# ============================================================
# STEP 4 — SEPARATE VOICES WITH SEPFORMER
# ============================================================
def separate_voices(input_path):
    print("🔄 Separating voices...")
    est_sources = separator.separate_file(path=input_path)  # [1, T, N_src]

    batch, T, num_sources = est_sources.shape
    print(f"→ Separated into {num_sources} speakers")

    separated_paths = []

    for i in range(num_sources):
        waveform_8k = est_sources[0, :, i].unsqueeze(0).cpu()  # [1, T]

        # Upsample to 16 kHz for ECAPA
        waveform_16k = torchaudio.functional.resample(waveform_8k, orig_freq=8000, new_freq=16000)

        out_path = os.path.join(OUTPUT_DIR, f"speaker_{i}.wav")
        torchaudio.save(out_path, waveform_16k, 16000)
        separated_paths.append(out_path)

        print(f"   → Saved separated file (16kHz): {out_path}")

    return separated_paths

# ============================================================
# STEP 5 — COMPUTE EMBEDDING FOR EACH SEPARATED SPEAKER
# ============================================================
def compute_embedding(path):
    wav, fs = torchaudio.load(path)

    if fs != 16000:
        wav = torchaudio.functional.resample(wav, fs, 16000)

    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)

    wav = wav.unsqueeze(0)
    feats = encoder.audio_normalizer(wav, 16000)

    with torch.no_grad():
        emb = encoder.encode_batch(feats)

    return emb.squeeze(0)

# ============================================================
# STEP 6 — CHOOSE BEST MATCH USING COSINE SIMILARITY
# ============================================================
def select_correct_voice(separated_paths):
    cos = torch.nn.CosineSimilarity(dim=-1)
    scores = []

    print("\n🔍 Comparing embeddings...")
    for i, spk_path in enumerate(separated_paths):
        test_emb = compute_embedding(spk_path)
        score = cos(enroll_embedding, test_emb).item()
        scores.append(score)
        print(f"   Speaker {i} → similarity = {score:.4f}")

    best_index = int(torch.tensor(scores).argmax())
    print(f"\n✅ BEST MATCH = Speaker {best_index}")

    return separated_paths[best_index]

# ============================================================
# STEP 7 — PLAY SELECTED AUDIO
# ============================================================
def play_audio(path):
    wav, fs = torchaudio.load(path)
    wav = wav.squeeze().numpy()
    print(f"🔊 Playing selected audio: {path}")
    sd.play(wav, fs)
    sd.wait()

# ============================================================
# MAIN PIPELINE (Step 3)
# ============================================================
def run_step3():

    mixture_path = os.path.join(OUTPUT_DIR, "mixture.wav")
    # mixture_path = os.path.join(
    #     OUTPUT_DIR,
    #     f"mixture_{datetime.now().strftime('%H%M%S')}.wav"
    # )

    record_mixture(mixture_path)
    separated_paths = separate_voices(mixture_path)
    chosen_voice_path = select_correct_voice(separated_paths)
    play_audio(chosen_voice_path)

    print("🎉 Step-3 Completed Successfully!")

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    run_step3()
