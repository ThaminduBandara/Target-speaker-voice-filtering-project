import torchaudio

def load_audio(path):
    signal, fs = torchaudio.load(path)
    return signal, fs
