import os
import torchaudio

# ============================================================
# OPTIONAL: display info
# ============================================================
print("Using torchaudio backend:", torchaudio.get_audio_backend())

from speechbrain.inference.separation import SepformerSeparation

# ============================================================
# CONFIG
# ============================================================
input_file  = "recordings/test_noisy/test_noisy.wav"
output_dir  = "recordings/filtered_output"
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# STEP 1 — Load model
# ============================================================
print("\n Loading SepFormer WHAMR model...")
model = SepformerSeparation.from_hparams(
    source="speechbrain/sepformer-whamr",
    savedir="pretrained_models/sepformer-whamr"
)

# ============================================================
# STEP 2 — Separate sources
# Output shape: [B, T, N_src]
# ============================================================
print("🔄 Separating sources... (please wait)")
est_sources = model.separate_file(path=input_file)

print("→ est_sources shape:", est_sources.shape)
# Example shape: [1, 24000, 2]

# Unpack
batch, T, num_sources = est_sources.shape

# ============================================================
# STEP 3 — Save each separated speaker
# ============================================================
print("\n💾 Saving separated speakers...")

# SepFormer WHAMR ALWAYS uses 8000 Hz
sample_rate = 8000

for i in range(num_sources):
    # est_sources: [1, T, N_src]
    waveform = est_sources[0, :, i].unsqueeze(0).cpu()   # [1, T]

    out_path = os.path.join(output_dir, f"speaker_{i}.wav")
    torchaudio.save(out_path, waveform, sample_rate)

    print(f"   → Saved: {out_path}")

print("\n DONE — Separation successful!")

