## Target Speaker Voice Filtering Project

This project filters a target speaker from a mixed recording using:

- SepFormer (speech separation)
- ECAPA (speaker embedding and matching)
- FastAPI (backend API)

The backend workflow is:

1. Record your clean enrollment voice (5 seconds)
2. Extract and save your speaker embedding
3. Record a noisy/multi-speaker sample and return the best matched speaker audio

---

## Project Layout

```text
backend/
	main.py                       # FastAPI app
	services/
		model_loader.py             # Loads SepFormer + ECAPA
		record_service.py           # Step 1: record enrollment audio
		embedding_service.py        # Step 2: extract enrollment embedding
		separation_service.py       # Step 3: record mixture, separate, choose best match

recordings/
	my_voice_samples/clean_voice.wav
	enroll_embedding/enroll_embedding.pt
	step3_output/
		mixture.wav
		speaker_0.wav
		speaker_1.wav
```

---

## Prerequisites

- macOS, Linux, or Windows
- Python 3.10+ (recommended: 3.10 or 3.11)
- Working microphone
- Internet connection for first model download

Notes:

- On first run, SpeechBrain may download pretrained model files into `pretrained_models/`.
- On macOS, give Terminal/VS Code microphone permission in System Settings.

---

## Setup

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt fastapi uvicorn
```

Why install `fastapi` and `uvicorn` explicitly?

- They are required by the backend app but are not listed in `requirements.txt` yet.

---

## Run the Backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

---

## API Workflow

Call endpoints in this order.

### 1) Record Enrollment Audio

```bash
curl -X POST http://127.0.0.1:8000/record-enroll
```

Expected output file:

- `recordings/my_voice_samples/clean_voice.wav`

### 2) Extract Enrollment Embedding

```bash
curl -X POST http://127.0.0.1:8000/extract-embedding
```

Expected output file:

- `recordings/enroll_embedding/enroll_embedding.pt`

### 3) Record Mixture and Filter Target Speaker

```bash
curl -X POST http://127.0.0.1:8000/separate
```

The response returns two URLs:

- `mixture_url`
- `cleaned_url`

These point to files served from `recordings/step3_output/`.

Example:

```json
{
	"mixture_url": "/file/mixture.wav",
	"cleaned_url": "/file/speaker_1.wav"
}
```

You can download the final output in browser:

- `http://127.0.0.1:8000/file/speaker_1.wav`

---

## What the Backend Does Internally

- `record-enroll`: records 5 seconds at 16 kHz
- `extract-embedding`: computes ECAPA embedding for enrollment audio
- `separate`:
	- records a 5-second mixed audio sample
	- separates multiple sources using SepFormer
	- post-processes audio (fade + low-pass + resample)
	- computes similarity with enrollment embedding
	- returns the best-matching speaker file

---

## Common Issues

### Microphone permission denied

- macOS: System Settings -> Privacy & Security -> Microphone
- Enable access for Terminal and/or Visual Studio Code

### `ModuleNotFoundError: fastapi` or `uvicorn`

Install missing packages:

```bash
pip install fastapi uvicorn
```

### First run is slow

- Expected behavior.
- Pretrained models are loaded/downloaded on first use.

### No `cleaned_url` file found

- Ensure you completed enrollment first:
	1. `/record-enroll`
	2. `/extract-embedding`
	3. `/separate`

---

## Optional Script-Based Files in `src/`

The `src/` folder contains earlier standalone experiments and helper scripts.
The recommended runtime path for this project is the FastAPI backend in `backend/`.

