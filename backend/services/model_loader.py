import torch
from speechbrain.inference.separation import SepformerSeparation
from speechbrain.inference import EncoderClassifier

# Load SepFormer once
print("🧠 Loading SepFormer...")
separator = SepformerSeparation.from_hparams(
    source="speechbrain/sepformer-whamr",
    savedir="pretrained_models/sepformer-whamr"
)

# Load ECAPA once
print("🧠 Loading ECAPA...")
encoder = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa"
)
